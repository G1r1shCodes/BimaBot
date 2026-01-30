"""
Sub-Limits Rule

Checks if charges exceed category-specific sub-limits.

Rule Logic (deterministic):
- FOR each sub-limit in policy
- Calculate total charges in that category
- IF total > limit
- THEN flag excess amount
"""

from typing import List, Dict
from app.models.audit import AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill, ChargeCategory
from app.models.policy import PolicyData, SubLimit


def check_sub_limits(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for sub-limit violations.
    
    Returns:
        List of sub-limit flags (empty if no issues)
    """
    flags: List[AuditFlag] = []
    
    # If no sub-limits defined, no rule to enforce
    if not policy.sub_limits:
        return flags
    
    # Group charges by category
    category_totals: Dict[str, float] = {}
    category_charges: Dict[str, List] = {}
    
    for charge in bill.charges:
        cat = charge.category.value
        category_totals[cat] = category_totals.get(cat, 0) + charge.amount
        if cat not in category_charges:
            category_charges[cat] = []
        category_charges[cat].append(charge)
    
    # Check each sub-limit
    for sub_limit in policy.sub_limits:
        # Normalize category for matching
        limit_category = sub_limit.category.lower().replace(" ", "_")
        
        # Find matching charges
        total_in_category = 0
        matching_charges = []
        
        for cat_key, cat_total in category_totals.items():
            # Flexible matching (e.g., "ICU" matches "icu")
            if limit_category in cat_key.lower() or cat_key.lower() in limit_category:
                total_in_category += cat_total
                matching_charges.extend(category_charges[cat_key])
        
        if total_in_category == 0:
            continue
        
        # Determine the limit amount
        limit_amount = None
        
        if sub_limit.limit_amount:
            limit_amount = sub_limit.limit_amount
        elif sub_limit.limit_percentage and policy.coverage_amount:
            limit_amount = policy.coverage_amount * (sub_limit.limit_percentage / 100)
        
        if not limit_amount:
            continue
        
        # Check if exceeded
        if total_in_category > limit_amount:
            excess = total_in_category - limit_amount
            
            # Use the largest charge as reference
            primary_charge = max(matching_charges, key=lambda c: c.amount) if matching_charges else None
            
            flags.append(
                AuditFlag(
                    flag_type=FlagType.SUB_LIMIT,
                    severity=FlagSeverity.WARNING,
                    flag_scope=FlagScope.CHARGE,
                    line_item_id=primary_charge.line_item_id if primary_charge else None,
                    amount_affected=excess,
                    reason=f"Sub-limit exceeded for {sub_limit.category}. Charged: ₹{total_in_category:,.0f}, Limit: ₹{limit_amount:,.0f}.",
                    policy_clause=f"{sub_limit.category} sub-limit clause",
                    irdai_reference=None,
                )
            )
    
    return flags
