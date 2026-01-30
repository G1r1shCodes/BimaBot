"""
Co-pay Rule

Calculates co-payment amount if policy has co-pay clause.

Rule Logic (deterministic):
- IF policy has co-pay percentage
- THEN calculate co-pay on total bill
- Flag as INFO (not a deduction, just information)
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill
from app.models.policy import PolicyData


def check_copay(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Calculate co-payment amount.
    
    Returns:
        List with co-pay flag (empty if no co-pay)
    """
    flags: List[AuditFlag] = []
    
    # If no co-pay percentage, no rule to apply
    if not policy.copay_percentage or policy.copay_percentage <= 0:
        return flags
    
    # Calculate total bill amount
    total_bill = sum(charge.amount for charge in bill.charges)
    
    # Calculate co-pay amount
    copay_amount = total_bill * (policy.copay_percentage / 100)
    
    flags.append(
        AuditFlag(
            flag_type=FlagType.COPAY,
            severity=FlagSeverity.INFO,
            flag_scope=FlagScope.INFORMATIONAL,
            line_item_id=None,  # Applies to entire claim
            amount_affected=copay_amount,
            reason=f"Policy has {policy.copay_percentage}% co-payment clause. Patient pays ₹{copay_amount:,.0f}.",
            policy_clause="Co-payment terms",
            irdai_reference=None,
        )
    )
    
    return flags
