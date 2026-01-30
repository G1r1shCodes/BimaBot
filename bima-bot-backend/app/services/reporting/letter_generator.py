import boto3
import json
import os
from typing import Dict, Any, List

REGION = os.getenv('AWS_REGION', 'us-east-1')
# Nova Pro is smarter and better for legal writing
MODEL_ID = "amazon.nova-pro-v1:0"

bedrock = boto3.client('bedrock-runtime', region_name=REGION)

def write_dispute_letter(audit_json, metadata):
    """
    Writes a formal dispute letter using extracted metadata.
    """
    # --- SAFETY FIX: Check Input Type ---
    if not isinstance(audit_json, dict):
        print(f"⚠️ Warning: write_dispute_letter received {type(audit_json)} instead of dict.")
        return "Error: Could not generate letter due to audit format issue."

    # Now it is safe to use .get()
    structured_bill = audit_json.get('structured_bill', {})
    if not isinstance(structured_bill, dict):
        structured_bill = {"items": []}

    items = structured_bill.get('items', [])
    if not isinstance(items, list):
        items = []

    # Extract denied items
    denied_items = [
        item for item in items
        if isinstance(item, dict) and item.get('status') != 'Covered'
    ]
    
    if not denied_items:
        return "No dispute necessary. All items appear to be covered under the policy."

    prompt = f"""
    You are a Senior Legal Advocate for Insurance Claims in India.
    
    TASK:
    Write a formal Dispute Letter to the TPA/Insurer.
    
    [SENDER DETAILS]
    Name: {metadata.get('patient_name', '[Patient Name]')}
    Policy No: {metadata.get('policy_number', '[Policy Number]')}
    
    [RECIPIENT DETAILS]
    To: The Claims Manager
    Company: {metadata.get('insurer_name', '[Insurer Name]')}
    Address: {metadata.get('insurer_address', '[Address]')}
    
    [CONTEXT]
    We are disputing the following deductions made on Bill No: {metadata.get('bill_number', 'N/A')}, dated {metadata.get('bill_date', 'N/A')}.
    
    [DISPUTED ITEMS & GROUNDS]
    {json.dumps(denied_items)}
    
    [INSTRUCTIONS]
    1. Start with the Date.
    2. Subject: "Formal Dispute of Claim Deductions"
    3. Use a firm, professional, legal tone.
    4. Cite "IRDAI Master Circular 2024".
    5. Demand a re-assessment within 15 days.
    6. Sign off as the Patient.
    
    OUTPUT:
    Return ONLY the Markdown text of the letter.
    """
    
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.7}
        )
        
        return response['output']['message']['content'][0]['text']

    except Exception as e:
        return f"Error generating letter: {str(e)}"
