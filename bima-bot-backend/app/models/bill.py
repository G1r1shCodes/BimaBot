from enum import Enum
from typing import List, Optional
from pydantic import BaseModel


class ChargeCategory(str, Enum):
    """Controlled vocabulary for charge classification"""
    ROOM_RENT = "room_rent"
    CONSUMABLES = "consumables"
    PHARMACY = "pharmacy"
    DIAGNOSTICS = "diagnostics"
    PROFESSIONAL_FEES = "professional_fees"
    ICU = "icu"
    SURGERY = "surgery"
    MISC = "misc"


class LineItem(BaseModel):
    line_item_id: str                 # Unique ID for this charge
    label: str                        # "Room Rent", "Consumables"
    category: ChargeCategory          # Controlled enum
    amount: float
    raw_text: Optional[str] = None    # Original OCR text for traceability
    quantity: Optional[int] = None
    unit_price: Optional[float] = None


class HospitalBill(BaseModel):
    bill_id: str
    hospital_name: str
    patient_name: str
    admission_date: Optional[str] = None
    discharge_date: Optional[str] = None
    
    # Normalized disease names (ICD-style or canonical)
    # AI must normalize before passing to rule engine
    diagnosis: List[str]
    
    charges: List[LineItem]
    
    # Hospital's stated total (may not match sum of charges)
    stated_total_amount: float
    
    currency: str = "INR"
