"""
Schema Validator - Phase 4
Ensures AI-parsed objects meet business requirements before Engine execution.
"""

from typing import List, Optional
from app.models.bill import HospitalBill
from app.models.policy import PolicyData
from app.models.audit import AuditFlag, FlagType, FlagSeverity

def validate_bill_structure(bill: HospitalBill) -> List[AuditFlag]:
    """
    Validates structural integrity of the bill.
    Returns ERROR flags if critical data is missing.
    """
    flags = []
    
    if not bill.charges:
        flags.append(AuditFlag(
            flag_type=FlagType.MISC,
            severity=FlagSeverity.ERROR,
            reason="Bill contains no charge items.",
            policy_clause="Data Integrity"
        ))
        
    if bill.stated_total_amount <= 0:
        flags.append(AuditFlag(
            flag_type=FlagType.MISC,
            severity=FlagSeverity.ERROR,
            reason="Bill total amount is zero or negative.",
            policy_clause="Data Integrity"
        ))
        
    return flags

def validate_policy_structure(policy: PolicyData) -> List[AuditFlag]:
    """
    Validates structural integrity of the policy.
    """
    flags = []
    
    if not policy.policy_id:
         flags.append(AuditFlag(
            flag_type=FlagType.MISC,
            severity=FlagSeverity.ERROR,
            reason="Policy ID is missing.",
            policy_clause="Data Integrity"
        ))
        
    return flags
