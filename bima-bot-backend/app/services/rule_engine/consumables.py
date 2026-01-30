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
    Check for consumables compliance.
    
    Returns:
        List of consumables flags (empty if no issues)
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
    
    # Flag if exceeds threshold (for manual review)
    if total_consumables > CONSUMABLES_REVIEW_THRESHOLD:
        # Find the primary consumables line item for reference
        primary_charge = max(consumables_charges, key=lambda c: c.amount)
        
        # TEMP LOGIC: 30% deduction is a heuristic for demonstration.
        # In reality, this requires line-by-line verification against non-payable list.
        estimated_deduction = total_consumables * 0.3
    
    # Only flag if consumables exceed threshold
    if total_consumables > CONSUMABLES_REVIEW_THRESHOLD:
        # Get RAG explanation for why consumables are excluded
        rag_citation = ""
        if RAG_AVAILABLE:
            try:
                rag_citation = explain_consumables_exclusion() or ""
            except Exception as e:
                print(f"⚠️ RAG retrieval failed: {e}")
        
        reason_base = f"High consumables charges detected (₹{total_consumables:,.0f}). Itemization review recommended."
        reason = f"{reason_base} {rag_citation}" if rag_citation else reason_base
        
        flags.append(
            AuditFlag(
                flag_type=FlagType.CONSUMABLES,
                severity=FlagSeverity.WARNING,
                flag_scope=FlagScope.CHARGE,
                line_item_id=primary_charge.line_item_id,
                amount_affected=estimated_deduction,
                reason=reason,
                policy_clause="Consumables exclusion clause",
                irdai_reference=None,
            )
        )
    
    return flags
