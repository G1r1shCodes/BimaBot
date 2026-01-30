"""
Room Rent Rule

Checks if room charges exceed policy limits.

Rule Logic (deterministic):
- IF room rent line items exist
- AND policy has room limit
- AND charged amount > limit
- THEN calculate proportionate deduction
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill, ChargeCategory
from app.models.policy import PolicyData


def check_room_rent(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for room rent limit violations.
    
    Returns:
        List of room rent flags (empty if no issues)
    """
    flags: List[AuditFlag] = []
    
    # Find all room rent charges
    room_charges = [
        charge for charge in bill.charges
        if charge.category == ChargeCategory.ROOM_RENT
    ]
    
    if not room_charges:
        return flags
    
    # If policy has no room limit, no rule to enforce
    if not policy.room_limit_type or not policy.room_limit_value:
        return flags
    
    # For Phase 3: Handle amount-based limits
    if policy.room_limit_type == "amount":
        try:
            limit_per_day = float(policy.room_limit_value)
        except (ValueError, TypeError):
            # Cannot parse limit, skip rule
            return flags
        
        for charge in room_charges:
            # Calculate daily rate
            if charge.quantity and charge.quantity > 0:
                daily_rate = charge.unit_price if charge.unit_price else (charge.amount / charge.quantity)
                days = charge.quantity
            else:
                # Cannot determine daily rate
                continue
            
            if daily_rate > limit_per_day:
                # Calculate excess amount
                excess_per_day = daily_rate - limit_per_day
                total_excess = excess_per_day * days
                
                flags.append(
                    AuditFlag(
                        flag_type=FlagType.ROOM_RENT,
                        severity=FlagSeverity.WARNING,
                        flag_scope=FlagScope.CHARGE,
                        line_item_id=charge.line_item_id,
                        amount_affected=total_excess,
                        reason=f"Room rent exceeds policy limit. Charged: ₹{daily_rate}/day, Limit: ₹{limit_per_day}/day.",
                        policy_clause="Room rent limit clause",
                        irdai_reference="IRDAI/HLT/MISC/039/03/2020",
                    )
                )
    
    # For category-based limits (e.g., "single private")
    elif policy.room_limit_type == "category":
        # Would need room category in bill to compare
        # For Phase 3: flag for manual review
        for charge in room_charges:
            flags.append(
                AuditFlag(
                    flag_type=FlagType.ROOM_RENT,
                    severity=FlagSeverity.INFO,
                    flag_scope=FlagScope.CHARGE,
                    line_item_id=charge.line_item_id,
                    amount_affected=None,
                    reason=f"Room category verification needed. Policy limit: {policy.room_limit_value}.",
                    policy_clause="Room rent limit clause",
                    irdai_reference=None,
                )
            )
    
    return flags
