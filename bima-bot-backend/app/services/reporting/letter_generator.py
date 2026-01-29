"""
Letter Generator Service - Phase 5
Responsible for rendering professional dispute letters from Audit Results.
Template-based. No AI.
"""

from app.models.bill import HospitalBill
from app.models.policy import PolicyData
from app.models.audit import AuditFlag, FlagSeverity

def generate_dispute_letter(bill: HospitalBill, policy: PolicyData, flags: list[AuditFlag]) -> str:
    """
    Generates a formal dispute / query letter based on audit findings.
    """
    
    # Header
    letter = f"""To
The Claims Department
{policy.insurer_name}

Subject: Query regarding Claim for Patient {bill.patient_name} (Policy: {policy.policy_id})

Dear Sir/Madam,

We are writing to proactively address potential queries regarding the hospital bill for {bill.patient_name} (Admission Date: {bill.admission_date}).

Based on our internal audit against the policy terms, we have identified the following items that may require clarification or specific processing:

"""

    # Body (Flags)
    if not flags:
        letter += "No specific discrepancies were found. The claim appears to be fully compliant with policy terms.\n"
    else:
        for idx, flag in enumerate(flags, 1):
            severity_icon = "(!)" if flag.severity == FlagSeverity.ERROR else "(*)"
            letter += f"{idx}. {severity_icon} [{flag.flag_type.upper()}] {flag.reason}\n"
            if flag.amount_affected:
                letter += f"   Potential Impact: INR {flag.amount_affected:,.2f}\n"
            if flag.policy_clause:
                letter += f"   Reference: {flag.policy_clause}\n"
            letter += "\n"

    # Footer
    letter += f"""
Total Bill Amount: INR {bill.stated_total_amount:,.2f}

We request you to process the admissible amount at the earliest.

Sincerely,
Admissions Desk
{bill.hospital_name}
"""

    return letter
