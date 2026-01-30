"""
Exclusions Rule

Checks for specific non-payable items based on Policy Annexures (IRDAI Non-Payable List).
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity, FlagScope
from app.models.bill import HospitalBill
from app.models.policy import PolicyData

def check_exclusions(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for specific excluded line items like Admin charges, Waste disposal, etc.
    """
    flags: List[AuditFlag] = []
    
    for charge in bill.charges:
        description = charge.label.lower() if charge.label else ""
        
        # 1. Admission / Admin Charges
        if "admin" in description or "admission" in description or "registration" in description:
            # Check if this is truly an admin charge (not "administration of drug")
            if "drug" not in description and "medicine" not in description:
                flags.append(AuditFlag(
                    flag_type=FlagType.MISC,
                    severity=FlagSeverity.ERROR, # "Subject to Review" usually Warning/Error
                    flag_scope=FlagScope.CHARGE,
                    line_item_id=charge.line_item_id,
                    amount_affected=charge.amount,
                    reason="Policy Annexure A (List IV) - Admin",
                    policy_clause="Annexure A List IV (Non-Payable)",
                    irdai_reference="IRDAI/HLT/REG/CIR/003/01/2013"
                ))

        # 2. Bio-Medical Waste
        if "waste" in description or "bio-medical" in description:
            flags.append(AuditFlag(
                flag_type=FlagType.CONSUMABLES, # Changed to CONSUMABLES type for clarity
                severity=FlagSeverity.ERROR,
                flag_scope=FlagScope.CHARGE,
                line_item_id=charge.line_item_id,
                amount_affected=charge.amount,
                reason="Policy Annexure A (List I) - Optional Items",
                policy_clause="Annexure A List I (Optional)",
                irdai_reference="IRDAI/HLT/REG/CIR/003/01/2013"
            ))

        # 3. OT Consumables / General Consumables (Annexure A List III)
        # Explicit check to ensure these are flagged even if Policy Sublimit isn't detected
        if ("consumables" in description or "gloves" in description or "gauze" in description) and "ot" in description:
            flags.append(AuditFlag(
                flag_type=FlagType.CONSUMABLES,
                severity=FlagSeverity.ERROR,
                flag_scope=FlagScope.CHARGE,
                line_item_id=charge.line_item_id,
                amount_affected=charge.amount,
                reason="Policy Annexure A (List III) - Procedure Charges",
                policy_clause="Annexure A List III (Non-Payable)",
                irdai_reference="IRDAI Guidelines 2016"
            ))

    return flags
