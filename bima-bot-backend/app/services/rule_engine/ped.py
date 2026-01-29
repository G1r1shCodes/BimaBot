"""
Pre-Existing Disease (PED) Rule

Checks if diagnosed conditions are in PED list and whether
waiting period has been satisfied.

Rule Logic (deterministic):
- IF diagnosis in PED list
- AND policy age < PED waiting period
- THEN flag as PED issue
"""

from typing import List
from app.models.audit import AuditFlag, FlagType, FlagSeverity
from app.models.bill import HospitalBill
from app.models.policy import PolicyData


def check_ped(bill: HospitalBill, policy: PolicyData) -> List[AuditFlag]:
    """
    Check for Pre-Existing Disease violations.
    
    Returns:
        List of PED flags (empty if no issues)
    """
    flags: List[AuditFlag] = []
    
    # If no diagnosis, cannot check PED
    if not bill.diagnosis:
        return flags
    
    # If no PED list in policy, cannot enforce
    if not policy.ped_list:
        return flags
    
    # Normalize for comparison (case-insensitive strip)
    # Ideally should use a standard medical ontology code (e.g., ICD-10) in Phase 4
    ped_list_normalized = {ped.lower().strip() for ped in policy.ped_list}
    
    # Find diagnoses that match PED list
    matching_peds: List[str] = []
    for diagnosis in bill.diagnosis:
        diagnosis_normalized = diagnosis.lower().strip()
        
        # STRICT MATCHING ONLY
        # No "if 'dia' in diagnosis" guessing
        # Check if the diagnosis appears in the PED list OR if any PED appears in the diagnosis string
        # but only if it matches a complete concept 
        
        # For Phase 3, we allow containment if it matches a full PED string
        # e.g. "Diabetes" in "Diabetes Mellitus Type 2" is acceptable
        # but "Dia" in "Diabetes" is NOT.
        
        match_found = False
        if diagnosis_normalized in ped_list_normalized:
            match_found = True
        else:
            # Check if any defined PED is a substring of the diagnosis
            for ped in ped_list_normalized:
                # Ensure we don't match short random strings. 
                # Minimum length check or token matching would be better.
                if len(ped) > 3 and ped in diagnosis_normalized:
                    match_found = True
                    break
        
        if match_found:
            matching_peds.append(diagnosis)
    
    # If no PED conditions found, no flag
    if not matching_peds:
        return flags
    
    # PED found - now check waiting period
    # For Phase 3, we cannot determine policy age from admission date alone
    # We would need policy inception date, which is not in our schema yet
    
    # For hackathon: flag as ERROR since we detected PED
    # In production: would check actual dates
    
    total_billed = sum(charge.amount for charge in bill.charges)
    
    flags.append(
        AuditFlag(
            flag_type=FlagType.PED,
            severity=FlagSeverity.ERROR,
            line_item_id=None,  # Affects entire claim
            amount_affected=total_billed,
            reason=f"Pre-existing conditions detected: {', '.join(matching_peds)}. Waiting period verification required.",
            policy_clause="PED waiting period clause",
            irdai_reference=None,
        )
    )
    
    return flags
