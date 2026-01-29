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
    Simulates AI extracting bill details from raw OCR text.
    Strictly follows schema.
    Returns None if text is unrecognizable.
    """
    if "Apollo Hospitals" not in raw_text:
        return None
        
    # LOGIC: The AI "sees" the text and maps it to the schema.
    # Note: AI handles the typo correction (Rm Chrg -> Room Rent)
    
    charges = [
        LineItem(
            line_item_id="LI-AI-001",
            label="Rm Chrg ( Pvt )",
            category=ChargeCategory.ROOM_RENT,
            amount=25000.0,
            quantity=5,
            unit_price=5000.0,
            raw_text="1. Rm Chrg ( Pvt )  5000 x 5  = 25000"
        ),
        LineItem(
            line_item_id="LI-AI-002",
            label="ICU Chrgs",
            category=ChargeCategory.ICU,
            amount=80000.0,
            quantity=2,
            unit_price=40000.0,
            raw_text="2. ICU Chrgs        40000 x 2 = 80000"
        ),
        LineItem(
            line_item_id="LI-AI-003",
            label="Consumbls",
            category=ChargeCategory.CONSUMABLES,
            amount=15000.0,
            raw_text="3. Consumbls        15000"
        ),
        LineItem(
            line_item_id="LI-AI-004",
            label="Pharmacy",
            category=ChargeCategory.PHARMACY,
            amount=12000.0,
            raw_text="4. Pharmacy         12000"
        ),
        LineItem(
            line_item_id="LI-AI-005",
            label="Diagnostics",
            category=ChargeCategory.DIAGNOSTICS,
            amount=8000.0,
            raw_text="5. Diagnostics      8000"
        ),
        LineItem(
            line_item_id="LI-AI-006",
            label="Doc Fees",
            category=ChargeCategory.PROFESSIONAL_FEES,
            amount=10000.0,
            raw_text="6. Doc Fees         10000"
        ),
    ]
    
    return HospitalBill(
        bill_id="BILL-AI-2026",
        hospital_name="Apollo Hospitals",
        patient_name="John Doe",
        admission_date="2026-01-20",
        discharge_date="2026-01-25",
        diagnosis=["Diabetes Mellitus Type 2", "Hypertension"], # Normalized by AI
        charges=charges,
        stated_total_amount=150000.0,
        currency="INR"
    )
