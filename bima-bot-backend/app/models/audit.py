from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from app.models.bill import HospitalBill
from app.models.policy import PolicyData


class FlagType(str, Enum):
    """Controlled flag types"""
    PED = "ped"
    WAITING_PERIOD = "waiting_period"
    CONSUMABLES = "consumables"
    ROOM_RENT = "room_rent"
    SUB_LIMIT = "sub_limit"
    COPAY = "copay"
    EXCLUSION = "exclusion"
    MISC = "misc"


class FlagSeverity(str, Enum):
    """Impact severity"""
    ERROR = "error"        # Claim likely rejected
    WARNING = "warning"    # Needs review
    INFO = "info"          # Informational only


class AuditStatus(str, Enum):
    """Audit processing status"""
    CREATED = "created"        # After /start, before /upload
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class AuditFlag(BaseModel):
    flag_type: FlagType
    severity: FlagSeverity
    line_item_id: Optional[str] = None    # References LineItem.line_item_id
    amount_affected: Optional[float] = None
    reason: str                           # Human-readable explanation
    policy_clause: Optional[str] = None   # Section reference
    irdai_reference: Optional[str] = None


class AuditResult(BaseModel):
    audit_id: str
    bill: HospitalBill
    policy: PolicyData
    flags: List[AuditFlag]
    
    # Summary (computed by backend)
    total_billed: float               # Sum of all charges
    amount_under_review: float        # Sum of flagged amounts
    fully_covered_amount: float       # Total - flagged
    
    # Reporting
    dispute_letter_content: Optional[str] = None  # Generated text for the user
    
    # Metadata
    created_at: str
    status: AuditStatus
