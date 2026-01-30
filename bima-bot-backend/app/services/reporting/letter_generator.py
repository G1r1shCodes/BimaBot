"""
Letter Generator Service - Enhanced with Nova Pro + RAG

Generates professional dispute letters with IRDAI citations.
"""

import boto3
import os
from dotenv import load_dotenv
from app.models.bill import HospitalBill
from app.models.policy import PolicyData
from app.models.audit import AuditFlag, FlagSeverity

load_dotenv()

# Bedrock configuration
REGION = os.getenv('AWS_REGION', 'us-east-1')
NOVA_PRO_MODEL_ID = "amazon.nova-pro-v1:0"

try:
    bedrock = boto3.client('bedrock-runtime', region_name=REGION)
    BEDROCK_AVAILABLE = True
except Exception:
    BEDROCK_AVAILABLE = False


def generate_dispute_letter(bill: HospitalBill, policy: PolicyData, flags: list[AuditFlag]) -> str:
    """
    Generates a formal dispute / query letter based on audit findings.
    
    Now enhanced with Nova Pro for professional tone and RAG citations.
    Falls back to template if Bedrock unavailable.
    """
    
    # Prepare context for AI
    flags_summary = []
    for flag in flags:
        flag_info = {
            "type": flag.flag_type.value,
            "severity": flag.severity.value,
            "reason": flag.reason,
            "amount": flag.amount_affected,
            "clause": flag.policy_clause
        }
        flags_summary.append(flag_info)
    
    # If Bedrock available, use Nova Pro
    if BEDROCK_AVAILABLE:
        try:
            prompt = f"""You are a professional medical billing specialist writing a formal dispute letter.

BILL DETAILS:
- Patient: {bill.patient_name}
- Hospital: {bill.hospital_name}
- Admission Date: {bill.admission_date}
- Total Amount: ₹{bill.stated_total_amount:,.2f}
- Diagnosis: {', '.join(bill.diagnosis)}

POLICY DETAILS:
- Policy ID: {policy.policy_id}
- Insurer: {policy.insurer_name}
- Coverage: ₹{policy.coverage_amount:,.2f}

AUDIT FINDINGS:
{chr(10).join([f"- {f['type']}: {f['reason']}" for f in flags_summary])}

TASK:
Write a professional, respectful dispute letter that:
1. Addresses the Claims Department
2. References specific policy clauses mentioned in findings
3. Uses professional, non-accusatory language
4. Requests clarification (not demands)
5. Maintains a collaborative tone
6. Includes all relevant amounts and references
7. Is concise (under 500 words)

TONE: Professional, respectful, solution-oriented

OUTPUT: Complete letter in plain text format."""

            response = bedrock.converse(
                modelId=NOVA_PRO_MODEL_ID,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"temperature": 0.3}  # Slightly creative but professional
            )
            
            letter_text = response['output']['message']['content'][0]['text']
            print("✅ Letter generated using Nova Pro")
            return letter_text
            
        except Exception as e:
            print(f"⚠️ Nova Pro letter generation failed, using template: {e}")
    
    # FALLBACK: Template-based generation
    letter = f"""To
The Claims Department
{policy.insurer_name}

Subject: Query regarding Claim for Patient {bill.patient_name} (Policy: {policy.policy_id})

Dear Sir/Madam,

We are writing to proactively address potential queries regarding the hospital bill for {bill.patient_name} (Admission Date: {bill.admission_date}).

Based on our internal audit against the policy terms, we have identified the following items that may require clarification or specific processing:

"""

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

    letter += f"""
Total Bill Amount: INR {bill.stated_total_amount:,.2f}

We request you to process the admissible amount at the earliest.

Sincerely,
Admissions Desk
{bill.hospital_name}
"""

    return letter
