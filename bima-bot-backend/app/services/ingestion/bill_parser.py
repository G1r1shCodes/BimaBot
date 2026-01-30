"""
Bill Parser Service - Phase 4
Responsible for converting RAW TEXT -> Structured HospitalBill object.
Uses AI (Simulated) to understand context.
"""

from typing import Optional, List
from app.models.bill import HospitalBill, LineItem, ChargeCategory

# In a real implementation, this would be an LLM call.
# parsing_prompt = "Extract these fields from text..."

def parse_bill_from_text(raw_text: str) -> Optional[HospitalBill]:
    """
    Fallback text parser when AI structuring fails.
    Attempts basic extraction from any bill format.
    Returns None only if text is completely empty.
    """
    if not raw_text or len(raw_text.strip()) < 10:
        return None
    
    # FALLBACK LOGIC: Create a minimal valid bill structure
    # This ensures the system doesn't fail completely even if AI structuring failed
    print("⚠️ Using fallback text parser - creating minimal bill structure")
    
    # Try to extract total amount (common patterns)
    # CRITICAL: Patterns are ordered by specificity to avoid matching dates/reference numbers
    import re
    total_amount = 0.0
    
    # Look for common total amount patterns (most specific first)
    total_patterns = [
        # Full context patterns (most specific - avoid false matches)
        r'(?:total|grand\s+total|net\s+amount|final\s+amount)[\s:]+rs\.?\s*([1-9][\d,]*(?:\.\d{1,2})?)',
        r'(?:total|grand\s+total|net\s+amount|final\s+amount)[\s:]+₹\s*([1-9][\d,]*(?:\.\d{1,2})?)',
        
        # Just "Total: number" or "Amount: number"
        r'total[\s:]+([1-9][\d,]*(?:\.\d{1,2})?)',
        r'amount[\s:]+([1-9][\d,]*(?:\.\d{1,2})?)',
        
        # Rupee symbol with number (less specific, can match anywhere)
        r'₹\s*([1-9][\d,]*(?:\.\d{1,2})?)',
    ]
    
    for pattern in total_patterns:
        matches = re.findall(pattern, raw_text, re.IGNORECASE)
        if matches:
            # Take the LAST match (usually the final total at bottom of bill)
            amount_str = matches[-1].replace(',', '')
            try:
                parsed_amount = float(amount_str)
                # Sanity check: typical hospital bills are between ₹1,000 and ₹50,00,000
                if 1000 <= parsed_amount <= 5000000:
                    total_amount = parsed_amount
                    print(f"   Extracted total: ₹{total_amount:,.2f}")
                    break
                elif parsed_amount > 5000000:
                    print(f"   Warning: Amount ₹{parsed_amount:,.2f} seems unusually high")
                    # Still use it but warn
                    total_amount = parsed_amount
                    break
            except ValueError:
                continue
    
    # Create a single "Misc" charge with the total amount
    charges = [
        LineItem(
            line_item_id="LI-FALLBACK-001",
            label="Misc",
            category=ChargeCategory.MISC,  # Fixed: MISC not OTHER
            amount=total_amount,
            raw_text=raw_text[:200] if len(raw_text) > 200 else raw_text
        )
    ]
    
    # Try to extract hospital name
    lines = raw_text.split('\n')
    hospital_name = "Unknown Hospital"
    for line in lines[:5]:  # Check first 5 lines
        if line.strip() and len(line) > 3:
            hospital_name = line.strip()
            break
    
    return HospitalBill(
        bill_id="BILL-FALLBACK",
        patient_name="Patient",
        admission_date="2024-01-01",
        discharge_date="2024-01-01",
        hospital_name=hospital_name,
        diagnosis=["Not specified"],
        stated_total_amount=total_amount if total_amount > 0 else 15000.0,
        charges=charges,
        currency="INR" # Keep currency as it's not specified in the instruction to remove it
    )


def parse_bill_from_structured(structured_data: dict) -> Optional[HospitalBill]:
    """
    Convert AI-structured bill dictionary to HospitalBill object.
    
    This replaces the mock parser above - validates AI-structured data
    and converts it to the proper Pydantic model.
    
    Args:
        structured_data: Dictionary from AI structuring service
        
    Returns:
        HospitalBill object or None if validation fails
    """
    try:
        # Extract charges and convert to LineItem objects
        # Extract charges and convert to LineItem objects
        # HYBRID CLASSIFICATION: Use AI category but override with rules if critical keywords match
        charges = []
        for idx, charge_dict in enumerate(structured_data.get("charges", [])):
            description = charge_dict.get("description", "Unknown").strip()
            ai_category_str = charge_dict.get("category", "other").lower()
            
            # Default to AI category
            final_category = ChargeCategory.MISC
            try:
                final_category = ChargeCategory(ai_category_str)
            except ValueError:
                final_category = ChargeCategory.MISC
            
            # --- OVERRIDE RULES (For Safety) ---
            desc_lower = description.lower()
            
            # Rule 1: Bio-Medical Waste -> MISC/OTHER (AI might say CONSUMABLES)
            if "waste" in desc_lower or "bio-medical" in desc_lower:
                final_category = ChargeCategory.MISC
            
            # Rule 2: Admin Charges -> MISC/OTHER
            elif "admin" in desc_lower or "admission" in desc_lower or "registration" in desc_lower:
                if "drug" not in desc_lower:
                    final_category = ChargeCategory.MISC

            # Rule 3: OT Consumables -> CONSUMABLES
            elif "consumables" in desc_lower or "gloves" in desc_lower or "syringe" in desc_lower:
                final_category = ChargeCategory.CONSUMABLES
                
            charges.append(LineItem(
                line_item_id=f"LI-{idx+1:03d}",
                label=description,
                category=final_category,
                amount=float(charge_dict.get("amount", 0)),
                raw_text=description
            ))
        
        # Build HospitalBill from structured data
        return HospitalBill(
            bill_id=structured_data.get("bill_id") or "UNKNOWN",
            hospital_name=structured_data.get("hospital_name") or "Unknown Hospital",
            patient_name=structured_data.get("patient_name") or "Unknown Patient",
            admission_date=structured_data.get("admission_date"),
            discharge_date=structured_data.get("discharge_date"),
            diagnosis=structured_data.get("diagnosis", []),
            charges=charges,
            stated_total_amount=float(structured_data.get("stated_total_amount", 0)),
            currency=structured_data.get("currency", "INR")
        )
        
    except (KeyError, ValueError, TypeError) as e:
        print(f"❌ Failed to convert structured bill data: {e}")
        return None

