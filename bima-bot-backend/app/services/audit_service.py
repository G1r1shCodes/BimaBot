"""
Audit Service - Nova AI Architecture

Integrates:
1. OCR (Reading)
2. Nova Lite (Structuring)
3. Nova Pro + RAG (Auditing)
4. Nova Pro (Letter Generation)
"""

import uuid
from datetime import datetime
from typing import Dict, Optional, List
import json
import shutil
from pathlib import Path

# Models
from app.models.audit import AuditResult, AuditStatus, AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill, ChargeCategory
from app.models.policy import PolicyData

# Services
from app.services.ocr.ocr_service import extract_text_from_document
from app.services.ai.structuring_service import structure_and_categorize, extract_header_details, parse_policy_limits
from app.services.ai.rag_service import audit_claim
from app.services.reporting.letter_generator import write_dispute_letter
from app.services.aws_service import delete_multiple_files_from_s3

# In-memory audit store
# In-memory audit store
AUDIT_STORE: Dict[str, dict] = {}

def log_debug(msg):
    with open("debug_audit.log", "a", encoding="utf-8") as f:
        f.write(f"[{datetime.now()}] {msg}\n")

def generate_audit_id() -> str:
    return f"AUD-{uuid.uuid4().hex[:8].upper()}"

def update_audit_progress(audit_id: str, step: str, message: str):
    if audit_id in AUDIT_STORE:
        AUDIT_STORE[audit_id]["progress_step"] = step
        AUDIT_STORE[audit_id]["progress_message"] = message
def log_debug(msg):
    try:
        with open("debug_audit.log", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now()}] {msg}\n")
    except:
        pass

def _map_category(raw_cat: str) -> str:
    """Safe mapping of AI category strings to Pydantic Enum"""
    val = raw_cat.lower().strip().replace(' ', '_')
    
    # Direct matches
    if val in ["room_rent", "consumables", "pharmacy", "diagnostics", "surgery", "icu", "misc"]:
        return val
        
    # Fuzzy matches
    if "doctor" in val or "consultation" in val or "fee" in val:
        return "professional_fees"
    if "admin" in val or "registration" in val or "admission" in val:
        return "misc"
    if "lab" in val or "scan" in val or "x-ray" in val:
        return "diagnostics"
    if "medicine" in val or "drug" in val:
        return "pharmacy"
    if "implant" in val:
        return "surgery"
        
    return "misc"

def process_audit_pipeline(
    audit_id: str, 
    bill_path: str, 
    policy_path: str,
    bill_s3_key: str = None,
    policy_s3_key: str = None
) -> AuditResult:
    """
    Executes the new AI-First pipeline:
    OCR -> Nova Lite Structuring -> Nova Pro Audit (RAG) -> Nova Pro Letter
    """
    
    # 1. OCR STEP
    update_audit_progress(audit_id, "ocr", "Reading documents with OCR...")
    print(f"📄 Starting OCR extraction for audit {audit_id}...")
    
    from concurrent.futures import ThreadPoolExecutor
    
    try:
        # Run OCR in parallel to save time
        with ThreadPoolExecutor(max_workers=2) as executor:
            future_bill = executor.submit(extract_text_from_document, bill_path, bill_s3_key)
            future_policy = executor.submit(extract_text_from_document, policy_path, policy_s3_key)
            
            bill_text = future_bill.result()
            policy_text = future_policy.result()
        
        # Validate OCR
        if not bill_text or len(bill_text) < 50:
            return _create_error_result(audit_id, "OCR failed: Bill text empty or too short. Check if document is readable.")
        if not policy_text or len(policy_text) < 50:
            return _create_error_result(audit_id, "OCR failed: Policy text empty or too short. Check if document is readable.")
        
        # 2. AI STRUCTURING STEP (Nova Lite)
        update_audit_progress(audit_id, "structuring", "Structuring data with Nova Lite...")
        print("🧠 Nova Lite: Structuring documents...")
        
        print("🧠 Nova Lite: Structuring documents...")
        
        # Structure Bill
        bill_struct = structure_and_categorize(bill_text)
        log_debug(f"Bill Struct: {json.dumps(bill_struct, indent=2)}")
        
        # Structure Policy
        print("📄 Nova Lite: Extracting Specific Policy Limits...")
        policy_struct = parse_policy_limits(policy_text)
        log_debug(f"Policy Struct: {json.dumps(policy_struct, indent=2)}")
        
        if not bill_struct:
            return _create_error_result(audit_id, "AI failed to structure bill data")
            
        # 2b. EXTRACT HEADER METADATA (New Step)
        print("🔍 Nova Lite: Extracting Header Metadata...")
        header_metadata = extract_header_details(bill_text, policy_text)
            
        # 3. AI AUDIT STEP (Nova Pro + RAG)
        update_audit_progress(audit_id, "auditing", "Auditing claim with Nova Pro & RAG...")
        print("⚖️ Nova Pro: Running RAG Audit...")
        
        # Use fallback policy limits if policy struct failed (safeguard)
        clean_policy = policy_struct if policy_struct else {"error": "Policy parsing failed, using default rules"}
        
        audit_json = audit_claim(bill_struct, clean_policy)
        log_debug(f"RAG Audit Response: {json.dumps(audit_json, indent=2)}")
        
        # 4. MAPPING STEP (JSON -> Object Models)
        # We need to convert the flexible JSON from LLM into strict objects for Frontend
        
        # Map Bill Object
        # The audit_json['structured_bill'] might be a dict with 'items' or a direct list
        sb_data = audit_json.get('structured_bill', {})
        if isinstance(sb_data, list):
            audit_bill_items = sb_data
        else:
            audit_bill_items = sb_data.get('items', [])
            
        print(f"DEBUG: audit_bill_items count = {len(audit_bill_items)}")
        
        # Convert to HospitalBill.charges format with line_item_ids
        charges_list = []
        flags_list = []
        
        for idx, item in enumerate(audit_bill_items):
            print(f"DEBUG: Processing item {idx}: {item.get('description')} Status={item.get('status')}")
            # Generate ID
            line_item_id = f"LI-{idx+1:03d}"
            
            # Map Charge (using Amount as number if possible)
            amount = 0.0
            try:
                amt_val = item.get('amount', '0')
                if isinstance(amt_val, (int, float)):
                    amount = float(amt_val)
                else:
                    amt_str = str(amt_val).replace('₹', '').replace(',', '')
                    amount = float(amt_str)
            except:
                amount = 0.0
                
            # Handle category mapping safely
            cat_str = _map_category(item.get('category', 'misc'))
            
            charges_list.append({
                "line_item_id": line_item_id,
                "label": item.get('description', 'Unknown'),
                "description": item.get('description', 'Unknown'),
                "amount": amount,
                "category": cat_str 
            })
            
            # Map Flags based on Status
            status = item.get('status', 'Covered')
            
            # --- RULE BASED OVERRIDES (Hybrid Approach) ---
            # We enforce strict IRDAI rules regardless of what the LLM says for these specific categories
            
            desc_lower = item.get('description', '').lower()
            cat_lower = item.get('category', '').lower()
            
            override_severity = None
            override_reason = None
            
            # Rule 1: Bio-Medical Waste / Waste Disposal
            if "waste" in desc_lower or "disposal" in desc_lower:
                status = "May Not Comply"
                override_severity = FlagSeverity.ERROR
                # override_reason = "IRDAI Non-Payable list..." -> REMOVED to let AI explain
                
            # Rule 2: OT Consumables (or just 'Consumables' category if not explicitly allowed)
            elif "consumables" in desc_lower or "consumables" in cat_lower:
                # Exclude legitimate medical consumables if any, but usually 'Consumables' category is non-payable
                 status = "May Not Comply"
                 override_severity = FlagSeverity.ERROR
                 # override_reason = "IRDAI Non-Payable list..." -> REMOVED

            # Rule 3: Physiotherapy (Non-medical/Consumable context)
            elif "physiotherapy" in desc_lower:
                 status = "May Not Comply"
                 override_severity = FlagSeverity.ERROR
                 # override_reason = "IRDAI Non-Payable list..." -> REMOVED

            # Rule 4: Admission / Admin / Registration
            elif "admission" in desc_lower or "admin" in desc_lower or "registration" in desc_lower:
                 status = "Subject to Review"
                 override_severity = FlagSeverity.WARNING # Display as Orange
                 # override_reason = "Policy Annexure A..." -> REMOVED

            # --- End Rules ---

            # Normalize status for other items
            status_lower = status.lower()
            if "may not comply" in status_lower or "non-payable" in status_lower:
                serverity = FlagSeverity.ERROR
                msg_status = "May Not Comply"
            elif "subject to review" in status_lower or "review" in status_lower:
                serverity = FlagSeverity.WARNING
                msg_status = "Subject to Review"
            elif "partial" in status_lower or "denied" in status_lower:
                serverity = FlagSeverity.ERROR
                msg_status = "May Not Comply"
            else:
                msg_status = "Covered"
                serverity = None
            
            # Apply Override if exists
            if override_severity:
                serverity = override_severity
                msg_status = status # Propagate the overridden status string
            
            if msg_status != "Covered" or override_severity:
                # Use override reason if available, else prioritize unique AI reason, then fallback to reference
                reason_text = override_reason if override_reason else (item.get('reason') or item.get('reference', 'Policy Rule'))
                
                flags_list.append(AuditFlag(
                    flag_type=FlagType.MISC, 
                    severity=serverity,
                    flag_scope=FlagScope.CHARGE,
                    line_item_id=line_item_id,
                    amount_affected=amount,
                    reason=reason_text,
                    policy_clause=item.get('reference', ''),
                    charge_description=item.get('description', '')
                ))
        
        # Create Bill Object
        hospital_bill = HospitalBill(
            bill_id=bill_struct.get('bill_id', 'Unknown'),
            hospital_name=bill_struct.get('hospital_name', 'Unknown'),
            patient_name=bill_struct.get('patient_name', 'Unknown'),
            diagnosis=bill_struct.get('diagnosis', []),
            charges=charges_list,
            stated_total_amount=bill_struct.get('stated_total_amount', 0),
            currency="INR"
        )
        
        # Create Policy Object
        policy_data = PolicyData(
            policy_id=clean_policy.get('policy_id', 'Unknown'),
            policy_holder_name=clean_policy.get('policy_holder_name', 'Unknown'),
            insurer_name=clean_policy.get('insurer_name', 'Unknown'),
            coverage_amount=clean_policy.get('coverage_amount', 0),
            ped_list=clean_policy.get('ped_list', [])
        )
        
        # Enrich Flags with Detailed Explanations
        # REMOVED: We now rely on item-specific 'reason'
        # explanations = audit_json.get('explanations', [])
        # expl_lookup = ...
        # for flag in flags_list: ...
        
        # Calculate totals from audit summary
        summary = audit_json.get('audit_summary', {})
        try:
            total_val = summary.get('total_bill_amount', 0)
            if isinstance(total_val, (int, float)):
                 total = float(total_val)
            else:
                 total = float(str(total_val).replace('₹', '').replace(',', ''))
            
            review_val = summary.get('amount_requiring_review', 0)
            if isinstance(review_val, (int, float)):
                 under_review = float(review_val)
            else:
                 under_review = float(str(review_val).replace('₹', '').replace(',', ''))
        except:
            total = hospital_bill.stated_total_amount
            under_review = sum(f.amount_affected for f in flags_list)
            
        fully_covered = max(0, total - under_review)
        
        # 5. LETTER GENERATION
        update_audit_progress(audit_id, "reporting", "Generating dispute letter...")
        
        # New Metadata Construction
        # Merge structured header data with fallback from other sources
        letter_metadata = {
            "patient_name": header_metadata.get('patient_name') or bill_struct.get('patient_name', 'Unknown'),
            "policy_number": header_metadata.get('policy_number') or clean_policy.get('policy_id', 'Unknown'),
            "insurer_name": header_metadata.get('insurer_name') or clean_policy.get('insurer_name', 'Insurance Company'),
            "insurer_address": header_metadata.get('insurer_address', "Claims Department, Registered Office"),
            "bill_number": header_metadata.get('bill_number') or bill_struct.get('bill_id', 'NA'),
            "bill_date": header_metadata.get('bill_date') or datetime.now().strftime("%d-%b-%Y")
        }
        
        # Pass full audit_json (which contains structured_bill)
        letter_content = write_dispute_letter(audit_json, letter_metadata)
        
        return AuditResult(
            audit_id=audit_id,
            bill=hospital_bill,
            policy=policy_data,
            flags=flags_list,
            total_billed=total,
            amount_under_review=under_review,
            fully_covered_amount=fully_covered,
            dispute_letter_content=letter_content,
            created_at=datetime.now().isoformat(),
            status=AuditStatus.COMPLETED
        )
        
    except Exception as e:
        print(f"❌ Pipeline Exception: {e}")
        return _create_error_result(audit_id, str(e))
        
    finally:
        _cleanup_audit_files(audit_id, bill_s3_key, policy_s3_key, bill_path, policy_path)


def _cleanup_audit_files(audit_id, bill_s3, policy_s3, bill_local, policy_local):
    """Secure cleaning of files"""
    try:
        s3_keys = [k for k in [bill_s3, policy_s3] if k]
        if s3_keys:
            delete_multiple_files_from_s3(s3_keys)
        
        if bill_local and Path(bill_local).exists():
            Path(bill_local).unlink()
        if policy_local and Path(policy_local).exists():
            Path(policy_local).unlink()
            
        # Cleanup dir
        if bill_local:
            d = Path(bill_local).parent
            if audit_id in str(d) and d.exists():
                shutil.rmtree(d)
    except Exception as e:
        print(f"Cleanup warning: {e}")


def _create_error_result(audit_id: str, error_msg: str) -> AuditResult:
    """Helper to return a safe error state result"""
    
    # We create a dummy bill with empty charges to avoid complex validation
    dummy_bill = HospitalBill(
        bill_id="ERROR", 
        hospital_name="Unknown", 
        patient_name="Unknown", 
        diagnosis=[], 
        charges=[], 
        stated_total_amount=0, 
        currency="INR"
    )
    
    dummy_policy = PolicyData(
        policy_id="ERROR", 
        policy_holder_name="Unknown", 
        insurer_name="Unknown", 
        coverage_amount=0, 
        ped_list=[]
    )
    
    return AuditResult(
        audit_id=audit_id,
        bill=dummy_bill,
        policy=dummy_policy,
        flags=[AuditFlag(
            flag_type=FlagType.MISC, 
            severity=FlagSeverity.ERROR, 
            reason=error_msg,
            charge_description="System Error"
        )],
        total_billed=0,
        amount_under_review=0,
        fully_covered_amount=0,
        dispute_letter_content="Audit failed due to technical error.",
        status=AuditStatus.FAILED,
        created_at=datetime.now().isoformat()
    )

# --- API Functions ---
def start_audit() -> dict:
    audit_id = generate_audit_id()
    AUDIT_STORE[audit_id] = {
        "audit_id": audit_id, "status": AuditStatus.CREATED, 
        "bill_path": None, "policy_path": None, "created_at": datetime.now().isoformat(), "result": None
    }
    return {"audit_id": audit_id, "status": AuditStatus.CREATED, "message": "Session created."}

def get_audit_status(audit_id: str) -> Optional[dict]:
    s = AUDIT_STORE.get(audit_id)
    return {"audit_id": audit_id, "status": s["status"], "progress_step": s.get("progress_step"), "progress_message": s.get("progress_message")} if s else None

def get_audit_result(audit_id: str) -> Optional[AuditResult]:
    session = AUDIT_STORE.get(audit_id)
    # Check if session exists and is completed
    if not session: return None
    if session["status"] == AuditStatus.PROCESSING: return None
    
    if session["result"] is None:
        bill_path, policy_path = session.get("bill_path"), session.get("policy_path")
        if not bill_path or not policy_path: return None
        
        try:
            session["result"] = process_audit_pipeline(
                audit_id, bill_path, policy_path, 
                session.get("bill_s3_key"), session.get("policy_s3_key")
            )
        except Exception as e:
            print(f"Pipeline error: {e}")
            raise
            
    return session["result"]

def manually_complete_audit(audit_id: str) -> bool:
    session = AUDIT_STORE.get(audit_id)
    if not session: return False
    session["status"] = AuditStatus.COMPLETED
    return True
