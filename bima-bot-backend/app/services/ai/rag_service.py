"""
RAG Retrieval Service - Nova Pro Audit Integration

Performs full claim audit using AWS Bedrock Knowledge Base and Nova Pro.
This replaces generic RAG retrieval with a specialized "Audit" agent.
"""

import boto3
import os
import json
from typing import Optional, Dict, Any
from dotenv import load_dotenv

load_dotenv()

# Bedrock Knowledge Base configuration
REGION = os.getenv('AWS_REGION', 'us-east-1')
KB_ID = os.getenv('BEDROCK_KB_ID', 'OIAANDNCSY')  # Default from user request
MODEL_ARN = os.getenv('BEDROCK_MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0')

agent = boto3.client('bedrock-agent-runtime', region_name=REGION)

def audit_claim(bill_data: Dict[str, Any], policy_limits: Dict[str, Any]) -> Dict[str, Any]:
    print(f"⚖️  Nova Pro: Running Deep Audit with Specific Explanations...")
 
    prompt = f"""
    You are a Senior Insurance Auditor AI.
 
    [INPUT DATA]
    1. HOSPITAL BILL ITEMS: {json.dumps(bill_data)}
    2. POLICY LIMITS: {json.dumps(policy_limits)}
 
    [TASK]
    Audit every single line item individually. Do not generalize.
 
    [RULES FOR AUDIT]
    1. **Room Rent:** Compare item amount vs Policy Room Rent Limit. If bill > limit, mark 'Partial Denial' and calculate the difference.
    2. **Consumables:** (Gloves, Masks, Syringes) -> Mark 'May Not Comply' (cite IRDAI List I).
    3. **Admin Charges:** (Registration, Admission) -> Mark 'Subject to Review' (cite IRDAI List IV).
    4. **Medical Items:** (Consultation, Medicine, Surgery) -> Mark 'Covered'.
 
    [REQUIRED OUTPUT FORMAT]
    Output valid JSON only. Structure:
    {{
      "audit_summary": {{
        "total_bill_amount": "Sum of all items",
        "charges_reviewed": "Count of items",
        "amount_requiring_review": "Sum of denied/flagged items",
        "status": "Potential Policy Discrepancies"
      }},
      "structured_bill": {{
        "items": [
          {{
            "description": "Exact Item Name",
            "category": "Category",
            "amount": "Amount",
            "status": "Covered" OR "May Not Comply" OR "Partial Denial",
            "reference": "Specific Policy Clause or IRDAI List",
            "reason": "Detailed explanation specific to THIS item. Do NOT match generic category explanation. Explain WHY it is flagged."
          }}
        ]
      }}
    }}
    
    IMPORTANT: 
    - The 'explanations' list must NOT contain duplicates. 
    - Do NOT give a 'Consumables' explanation for a 'Room Rent' error.
    - Ensure 'reason' in 'items' is specific to that item, do not repeat the same explanation for multiple items.
    """
 
    try:
        response = agent.retrieve_and_generate(
            input={'text': prompt},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': MODEL_ARN
                }
            }
        )
 
        raw_text = response['output']['text']
        json_str = raw_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(json_str)
 
        # --- THE SAFETY FIX ---
        # If AI returns a list (e.g., just the items), we wrap it to prevent the crash
        if isinstance(data, list):
            print("⚠️ Warning: AI returned a list. Wrapping in default structure.")
            return {
                "audit_summary": {"status": "Format Warning", "total_bill_amount": "Unknown", "amount_requiring_review": 0},
                "structured_bill": {"items": data}, # Assuming the list is the items list
                "explanations": []
            }
 
        # If AI returns a dict but missed the keys, we add safe defaults
        if isinstance(data, dict):
            if "structured_bill" not in data:
                data["structured_bill"] = {"items": []}
            if "audit_summary" not in data:
                data["audit_summary"] = {"status": "Processed", "total_bill_amount": 0, "amount_requiring_review": 0}
            return data
 
        return {
            "audit_summary": {"status": "Error", "total_bill_amount": 0, "amount_requiring_review": 0},
            "structured_bill": {"items": []},
            "explanations": []
        }
 
    except Exception as e:
        print(f"❌ Audit JSON Generation Failed: {e}")
        return {
            "audit_summary": {"status": "Error", "message": str(e), "total_bill_amount": 0, "amount_requiring_review": 0},
            "structured_bill": {"items": []},
            "explanations": []
        }

# Keep original function for backward compatibility if needed, or redirect
def get_rag_explanation(query: str) -> Optional[str]:
    print("⚠️ get_rag_explanation is deprecated. Use audit_claim instead.")
    return None
