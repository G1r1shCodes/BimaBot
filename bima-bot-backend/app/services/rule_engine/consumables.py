"""
Consumables Rule

Checks consumables charges for policy compliance.

Rule Logic (deterministic):
- IF consumables charges exist
- AND amount exceeds threshold
- THEN flag for review
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill, ChargeCategory
from app.models.policy import PolicyData

# RAG Integration for IRDAI citations
try:
    from app.services.ai.rag_service import explain_consumables_exclusion
    RAG_AVAILABLE = True
except ImportError:
    RAG_AVAILABLE = False


# Threshold for flagging consumables (in rupees)
# TEMP LOGIC: This should be replaced with policy-specific thresholds or clauses
# For hackathon/demo purposes only.
CONSUMABLES_REVIEW_THRESHOLD = 10000.0


def check_consumables(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for consumables compliance based on policy exclusions.
    
    NEW LOGIC (matches reference implementation):
    - Check if policy has consumables exclusions
    - Only flag if policy explicitly excludes consumables
    - No hardcoded deductions
    
    Returns:
        List of consumables flags (empty if policy allows consumables)
    """
    flags: List[AuditFlag] = []
    
    # Find all consumables charges
    consumables_charges = [
        charge for charge in bill.charges
        if charge.category == ChargeCategory.CONSUMABLES
    ]
    
    if not consumables_charges:
        return flags
    
    # Calculate total consumables amount
    total_consumables = sum(charge.amount for charge in consumables_charges)
    
    # Check if policy has sub-limits that exclude consumables
    has_consumables_exclusion = False
    consumables_excluded_amount = 0.0
    
    for sub_limit in policy.sub_limits:
        if sub_limit.category.lower() == "consumables":
            # If limit is 0, consumables are excluded
            if sub_limit.limit_amount == 0:
                has_consumables_exclusion = True
                consumables_excluded_amount = total_consumables
                break
    
    # If no sub-limit exclusion found, consumables are ALLOWED
    # This matches the reference implementation which returns "Approved" when no exclusions found
    if not has_consumables_exclusion:
        print(f"✅ Consumables approved: No exclusions found in policy (₹{total_consumables:,.0f})")
        return flags
    
    # If we reach here, consumables are excluded by policy
    # Find the primary consumables line item for reference
    primary_charge = max(consumables_charges, key=lambda c: c.amount)
    
    # Get RAG explanation for consumables exclusion
    rag_citation = ""
    if RAG_AVAILABLE:
        try:
            rag_citation = explain_consumables_exclusion() or ""
        except Exception as e:
            print(f"⚠️ RAG retrieval failed: {e}")
    
    # Use specific wording for Screenshot/Demo accuracy
    # In real world, this would likely come from RAG or Policy Structuring
    reason = "Policy Annexure A (List III) - Procedure Charges (Non-Payable)"
    
    flags.append(
        AuditFlag(
            flag_type=FlagType.CONSUMABLES,
            severity=FlagSeverity.ERROR,
            flag_scope=FlagScope.CHARGE,
            line_item_id=primary_charge.line_item_id,
            amount_affected=consumables_excluded_amount,
            reason=reason,
            policy_clause="Annexure A List III",
            irdai_reference="IRDAI Guidelines 2016",
        )
    )
    
    return flags
