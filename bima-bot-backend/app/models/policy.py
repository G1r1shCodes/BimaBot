from typing import List, Optional
from pydantic import BaseModel


class SubLimit(BaseModel):
    category: str                     # "ICU", "consumables", "pharmacy"
    limit_amount: Optional[float] = None
    limit_percentage: Optional[float] = None


class PolicyClause(BaseModel):
    """Structured policy clause for RAG retrieval"""
    clause_id: str                    # "4.1", "exclusion_3"
    clause_type: str                  # "PED", "ROOM_RENT", "EXCLUSION", "GENERAL"
    text: str                         # Full clause text
    page_number: Optional[int] = None


class PolicyData(BaseModel):
    policy_id: str
    policy_holder_name: str
    insurer_name: str
    coverage_amount: float
    
    # Exclusions & waiting periods
    ped_list: List[str]               # Pre-existing diseases (normalized names)
    general_waiting_period_months: Optional[int] = None
    ped_waiting_period_months: Optional[int] = None
    
    # Room rent limit structure
    room_limit_type: Optional[str] = None      # "category" | "amount"
    room_limit_value: Optional[str] = None     # "single private" or "5000"
    
    # Sub-limits
    sub_limits: List[SubLimit] = []
    
    # Co-pay
    copay_percentage: Optional[float] = None
    
    # Structured clauses for RAG
    clauses: List[PolicyClause] = []
