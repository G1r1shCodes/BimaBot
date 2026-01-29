"""
Waiting Period Rule

Checks if claim is within general waiting period after policy inception.

Rule Logic (deterministic):
- IF general waiting period exists
- AND cannot verify policy age
- THEN flag for verification

Note: Full implementation requires policy inception date in schema.
For Phase 3, we flag for manual verification.
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity
from app.models.bill import HospitalBill
from app.models.policy import PolicyData


def check_waiting_period(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for general waiting period violations.
    
    Returns:
        List of waiting period flags (empty if no issues)
    """
    flags: List[AuditFlag] = []
    
    # If no general waiting period defined, no rule to enforce
    if not policy.general_waiting_period_months:
        return flags
    
    # For Phase 3: We don't have policy inception date in schema yet
    # Rule: If required data is missing -> Unable to verify (INFO), never ERROR
    
    # Mocking check for missing date (since it's not in schema yet)
    policy_inception_date = None
    
    if not policy_inception_date:
        flags.append(
            AuditFlag(
                flag_type=FlagType.WAITING_PERIOD,
                severity=FlagSeverity.INFO,
                line_item_id=None,
                amount_affected=None,
                reason=f"Unable to verify {policy.general_waiting_period_months}-month waiting period (Policy inception date missing).",
                policy_clause="General waiting period clause",
                irdai_reference=None,
            )
        )
        return flags
        
    # Real logic would go here:
    # if admission_date < policy_inception_date + waiting_period:
    #     flag ERROR
    
    return flags
