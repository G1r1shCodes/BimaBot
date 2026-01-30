"""
Audit Service - Phase 4 Integration

Integrates:
1. OCR (Reading)
2. Ingestion/AI (Understanding)
3. Validation (Safety)
4. Rule Engine (Logic)
"""

import uuid
from datetime import datetime
from typing import Dict, Optional, List

from app.models.audit import AuditResult, AuditStatus, AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill
from app.models.policy import PolicyData

# Phase 4 Imports
from app.services.ocr.ocr_service import extract_text_from_document
from app.services.ingestion.bill_parser import parse_bill_from_text, parse_bill_from_structured
from app.services.ingestion.policy_parser import parse_policy_from_text, parse_policy_from_structured
from app.services.validation.schema_validator import validate_bill_structure, validate_policy_structure
from app.services.rule_engine import run_audit_rules

# AI Services (New - Reference Backend Pattern)
from app.services.ai.structuring_service import structure_and_categorize


# In-memory audit store
AUDIT_STORE: Dict[str, dict] = {}


def generate_audit_id() -> str:
    """Generate unique audit ID"""
    return f"AUD-{uuid.uuid4().hex[:8].upper()}"


from app.services.reporting.letter_generator import generate_dispute_letter

# ============================================================================
# ORCHESTRATION PIPELINE
# ============================================================================

def process_audit_pipeline(
    audit_id: str, 
    bill_path: str, 
    policy_path: str,
    bill_s3_key: str = None,
    policy_s3_key: str = None
) -> AuditResult:
    """
    Executes the full Phase 4 pipeline with real PDF files:
    Document -> OCR -> Text -> AI Parser -> Object -> Validation -> Rules -> Flags
    
    Args:
        audit_id: Unique audit identifier
        bill_path: Absolute path to hospital bill PDF (local)
        policy_path: Absolute path to insurance policy PDF (local)
        bill_s3_key: S3 key for bill (e.g., 'audits/AUD-123/bill.pdf')
        policy_s3_key: S3 key for policy (e.g., 'audits/AUD-123/policy.pdf')
    """
    
    # 1. OCR STEP (Read from S3 via Textract - OPTIMIZED 1s polling)
    # Pass S3 keys to OCR service for multi-user safe processing
    print(f"📄 Starting OCR extraction for audit {audit_id}...")
    bill_text = extract_text_from_document(bill_path, bill_s3_key)
    policy_text = extract_text_from_document(policy_path, policy_s3_key)
    
    # Log OCR results for debugging
    print(f"   Bill OCR: {len(bill_text) if bill_text else 0} characters")
    print(f"   Policy OCR: {len(policy_text) if policy_text else 0} characters")
    
    if not bill_text or len(bill_text) < 50:
        print(f"❌ CRITICAL: Bill OCR text is empty or too short!")
        print(f"   Bill path: {bill_path}")
        print(f"   Bill S3 key: {bill_s3_key}")
        return _create_error_result(audit_id, "OCR failed to extract text from bill. Please ensure the document is readable and properly formatted.")
    
    if not policy_text or len(policy_text) < 50:
        print(f"❌ CRITICAL: Policy OCR text is empty or too short!")
        return _create_error_result(audit_id, "OCR failed to extract text from policy document.")
    
    # 2. AI STRUCTURING STEP (Nova Lite for schema-aware structuring)
    # AI converts raw text → structured JSON with category classification
    # Categories are assigned BEFORE rules run (AI understands, Rules decide)
    print("🧠 AI Structuring: Converting text to structured data...")
    structured_data = structure_and_categorize(bill_text, policy_text)
    
    # 3. VALIDATION & OBJECT CREATION
    # Use AI-structured data if available, otherwise fallback to raw text parsing
    bill: Optional[HospitalBill] = None
    policy: Optional[PolicyData] = None
    
    if structured_data.get('bill'):
        # PRIMARY PATH: Use AI-structured data (preferred)
        print("✅ Using AI-structured bill data")
        bill = parse_bill_from_structured(structured_data['bill'])
    
    if not bill:
        # FALLBACK: Parse from raw text if AI structuring failed
        print("⚠️ Falling back to text-based parsing for bill")
        bill = parse_bill_from_text(bill_text)
    
    if structured_data.get('policy'):
        # PRIMARY PATH: Use AI-structured data (preferred)
        print("✅ Using AI-structured policy data")
        policy = parse_policy_from_structured(structured_data['policy'])
    
    if not policy:
        # FALLBACK: Parse from raw text if AI structuring failed
        print("⚠️ Falling back to text-based parsing for policy")
        policy = parse_policy_from_text(policy_text)
    
    # Handle OCR/Parsing Failures (Safety Rule: No guessing)
    pipeline_flags: List[AuditFlag] = []
    
    if not bill:
        # Fallback if bill is unreadable
        return _create_error_result(audit_id, "Unable to parse hospital bill text.")
        
    if not policy:
        # Fallback if policy is unreadable
        return _create_error_result(audit_id, "Unable to parse policy document.")

    # 4. VALIDATION STEP (Structural Integrity)
    pipeline_flags.extend(validate_bill_structure(bill))
    pipeline_flags.extend(validate_policy_structure(policy))
    
    # 5. RULE ENGINE STEP (The Brain - Deterministic Logic)
    # Rules receive AI-classified categories and structured data
    # Rules make ALL decisions (eligibility, amounts, deductions)
    # AI classification ensures consistent categorization before rule evaluation
    rule_flags = run_audit_rules(bill, policy)
    pipeline_flags.extend(rule_flags)
    
    # 6. SUMMARY CALCULATION WITH DOMINANT RULE LOGIC
    total_billed = sum(item.amount for item in bill.charges) if bill.charges else 0.0
    
    # CRITICAL FIX: Implement dominant rule logic to prevent double-counting
    # 
    # Problem: Multiple rules can flag the SAME money (e.g., PED affects entire bill,
    # but room rent, consumables, copay also affect portions of that same bill).
    # Naive sum of all amounts leads to double/triple counting.
    #
    # Solution: Use rule priority hierarchy
    #   1. DOMINANT RULES (PED, waiting period) → block entire claim
    #   2. DEDUCTIVE RULES (sub-limits, room rent, consumables, copay) → specific amounts
    #
    # If a dominant rule applies, it takes precedence and other rules become
    # "supporting reasons" rather than additional amounts to sum.
    
    # Check for dominant flags (PED or waiting period with severity ERROR)
    has_ped_blocker = any(
        flag.flag_type == FlagType.PED and flag.severity == FlagSeverity.ERROR
        for flag in pipeline_flags
    )
    
    has_waiting_period_blocker = any(
        flag.flag_type == FlagType.WAITING_PERIOD and flag.severity == FlagSeverity.ERROR
        for flag in pipeline_flags
    )
    
    if has_ped_blocker or has_waiting_period_blocker:
        # DOMINANT RULE CASE: Entire claim is under dispute
        # All other flags become supporting justification, not separate amounts
        amount_under_review = total_billed
        
    else:
        # STANDARD CASE: Sum specific deductions (room rent, consumables, copay, etc.)
        # These rules don't overlap significantly, so summation is appropriate
        amount_under_review = sum(
            flag.amount_affected for flag in pipeline_flags 
            if flag.amount_affected is not None
        )
        
        # Safety cap: amount under review can NEVER exceed total bill
        # (Protects against edge cases where rules might still overlap)
        amount_under_review = min(amount_under_review, total_billed)
    
    fully_covered_amount = max(0, total_billed - amount_under_review)
    
    # 7. REPORTING STEP (Letter Generation with AI)
    # Letter generator will be enhanced to use RAG for IRDAI citations
    letter_text = generate_dispute_letter(bill, policy, pipeline_flags)
    
    return AuditResult(
        audit_id=audit_id,
        bill=bill,
        policy=policy,
        flags=pipeline_flags,
        total_billed=total_billed,
        amount_under_review=amount_under_review,
        fully_covered_amount=fully_covered_amount,
        dispute_letter_content=letter_text,
        created_at=datetime.now().isoformat(),
        status=AuditStatus.COMPLETED,
    )


def _create_error_result(audit_id: str, error_msg: str) -> AuditResult:
    """Helper to return a safe error state result"""
    # Create empty dummy objects to satisfy schema if parsing fails totally
    # In production, we might handle this differently (e.g. 422 Error)
    # But to satisfy AuditResult return type:
    from app.models.bill import ChargeCategory
    dummy_bill = HospitalBill(
        bill_id="ERROR", hospital_name="Unknown", patient_name="Unknown", 
        diagnosis=[], charges=[], stated_total_amount=0, currency="INR"
    )
    dummy_policy = PolicyData(
        policy_id="ERROR", policy_holder_name="Unknown", insurer_name="Unknown", 
        coverage_amount=0, ped_list=[]
    )
    
    return AuditResult(
        audit_id=audit_id,
        bill=dummy_bill,
        policy=dummy_policy,
        flags=[AuditFlag(
            flag_type=FlagType.MISC, 
            severity=FlagSeverity.ERROR, 
            reason=error_msg
        )],
        total_billed=0,
        amount_under_review=0,
        fully_covered_amount=0,
        created_at=datetime.now().isoformat(),
        status=AuditStatus.FAILED
    )


# ============================================================================
# API SERVICE FUNCTIONS
# ============================================================================

def start_audit() -> dict:
    """Start new audit session with CREATED status."""
    audit_id = generate_audit_id()

    # Store session in memory
    AUDIT_STORE[audit_id] = {
        "audit_id": audit_id,
        "status": AuditStatus.CREATED,  # Changed from PROCESSING
        "bill_path": None,              # Added for file upload
        "policy_path": None,            # Added for file upload
        "created_at": datetime.now().isoformat(),
        "result": None,
    }

    return {
        "audit_id": audit_id,
        "status": AuditStatus.CREATED,  # Fixed: Match the stored status
        "message": "Audit session created. Upload documents next."
    }


def get_audit_status(audit_id: str) -> Optional[dict]:
    """Get audit processing status."""
    session = AUDIT_STORE.get(audit_id)
    if not session:
        return None

    return {
        "audit_id": audit_id,
        "status": session["status"],
    }


def get_audit_result(audit_id: str) -> Optional[AuditResult]:
    """
    Get audit result.
    Triggers the Phase 4 pipeline on demand if not ready.
    """
    session = AUDIT_STORE.get(audit_id)
    if not session:
        return None

    if session["status"] == AuditStatus.PROCESSING:
        return None

    # On first retrieval, run the full pipeline
    if session["result"] is None:
        # Phase 4: Run the Full Pipeline with file paths from session
        bill_path = session.get("bill_path")
        policy_path = session.get("policy_path")
        
        if not bill_path or not policy_path:
            # Files not uploaded yet - return None
            return None
        
        # Pass S3 keys for multi-user safe OCR processing
        session["result"] = process_audit_pipeline(
            audit_id=audit_id,
            bill_path=bill_path,
            policy_path=policy_path,
            bill_s3_key=session.get("bill_s3_key"),
            policy_s3_key=session.get("policy_s3_key")
        )

    return session["result"]


def manually_complete_audit(audit_id: str) -> bool:
    """
    Helper function to manually mark audit as completed.
    """
    session = AUDIT_STORE.get(audit_id)
    if not session:
        return False

    session["status"] = AuditStatus.COMPLETED
    return True
