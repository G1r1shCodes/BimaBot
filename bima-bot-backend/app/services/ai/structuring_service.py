"""
AI Structuring Service - Nova Lite Integration

Converts raw OCR text into structured JSON matching BimaBot schemas.

This implements the reference backend's structuring layer:
- Schema-aware prompting
- Category classification BEFORE rules
- Temperature = 0.0 for determinism
- No guessing - returns None on failure

Architecture Principle:
AI is used ONLY for understanding and structuring.
Rules remain deterministic and handle all decision logic.
"""

import boto3
import json
import os
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

load_dotenv()

# Bedrock configuration
REGION = os.getenv('AWS_REGION', 'us-east-1')
NOVA_LITE_MODEL_ID = "amazon.nova-lite-v1:0"  # Fast, cost-effective for data entry

bedrock = boto3.client('bedrock-runtime', region_name=REGION)


# Category mapping from AI categories to BimaBot ChargeCategory enum
CATEGORY_MAPPING = {
    "ROOM_RENT": "room_rent",
    "ICU_CHARGES": "icu",
    "CONSUMABLES": "consumables",
    "DOCTOR_FEES": "professional_fees",
    "SURGERY_CHARGES": "surgery",
    "MEDICINE": "pharmacy",
    "INVESTIGATION": "diagnostics",
    "OTHER": "misc"
}


def structure_bill_from_text(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    Convert raw OCR text into structured hospital bill data.
    
    Uses Nova Lite to:
    - Extract bill metadata (ID, hospital, patient, diagnosis)
    - Parse line items with amounts and categories
    - Classify each charge category
    
    Args:
        raw_text: Raw OCR text from hospital bill
        
    Returns:
        Structured bill dict matching HospitalBill schema, or None if parsing fails
        
    Example output:
        {
            "bill_id": "BILL-123",
            "hospital_name": "Apollo Hospital",
            "patient_name": "John Doe",
            "diagnosis": ["Appendicitis"],
            "charges": [
                {"description": "Room Rent", "amount": 5000, "category": "room_charges"},
                {"description": "Gloves", "amount": 500, "category": "consumables"}
            ],
            "stated_total_amount": 5500,
            "currency": "INR"
        }
    """
    
    # Use simplified prompt matching reference implementation
    prompt = f"""You are an AI Medical Biller.

TASK 1: STRUCTURE
Extract all billable items from the text below.

TASK 2: CATEGORY DECISION
For each item, assign one of these exact categories:
[ROOM_RENT, ICU_CHARGES, CONSUMABLES, DOCTOR_FEES, SURGERY_CHARGES, MEDICINE, INVESTIGATION, OTHER]

INPUT TEXT:
{raw_text}

OUTPUT FORMAT (JSON ONLY):
{{
  "items": [
    {{"description": "Gloves", "amount": 500, "category": "CONSUMABLES"}},
    {{"description": "Consultation", "amount": 1000, "category": "DOCTOR_FEES"}}
  ],
  "total_claimed": 1500
}}
"""

    try:
        print(f"📤 Sending bill to Nova Lite for structuring...")
        response = bedrock.converse(
            modelId=NOVA_LITE_MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.0}  # Deterministic
        )
        
        response_text = response['output']['message']['content'][0]['text']
        print(f"📥 Received AI response ({len(response_text)} chars)")
        
        # Clean markdown code blocks if present
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        
        structured_data = json.loads(clean_json)
        
        # Transform simplified response to full BimaBot schema
        if "items" in structured_data and "total_claimed" in structured_data:
            # Nova Lite returned simplified format - enrich with metadata
            items = structured_data["items"]
            
            # Normalize categories to BimaBot schema
            for item in items:
                if "category" in item:
                    ai_category = item["category"]
                    item["category"] = CATEGORY_MAPPING.get(ai_category, "other")
            
            # Extract basic metadata from raw text
            lines = raw_text.split('\n')
            hospital_name = "Unknown Hospital"
            for line in lines[:10]:  # Check first 10 lines for hospital name
                if line.strip() and len(line) > 3:
                    hospital_name = line.strip()
                    break
            
            # Build full schema
            full_schema = {
                "bill_id": f"BILL-AI-{hash(raw_text[:100]) % 10000:04d}",
                "hospital_name": hospital_name,
                "patient_name": "Patient",  # Will be enriched by rules if needed
                "diagnosis": [],  # Will be extracted by rules if needed
                "charges": items,  # AI-extracted line items
                "stated_total_amount": structured_data["total_claimed"],
                "currency": "INR"
            }
            
            print(f"✅ Structured bill with {len(items)} line items, total: ₹{structured_data['total_claimed']:,.2f}")
            return full_schema
        
        # Legacy format (if AI returned full schema directly - shouldn't happen now)
        elif "charges" in structured_data:
            for charge in structured_data["charges"]:
                if "category" in charge:
                    ai_category = charge["category"]
                    charge["category"] = CATEGORY_MAPPING.get(ai_category, "other")
            
            print(f"✅ Structured bill with {len(structured_data.get('charges', []))} line items")
            return structured_data
        
        else:
            print(f"❌ AI returned unexpected format: {list(structured_data.keys())}")
            return None
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse AI response as JSON: {e}")
        print(f"   Response was: {response_text[:200]}...")
        return None
    except Exception as e:
        print(f"❌ Bill structuring failed: {e}")
        return None


def structure_policy_from_text(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    Convert raw OCR text into structured policy data.
    
    Uses Nova Lite to extract:
    - Policy metadata (ID, holder, insurer)
    - Coverage amounts
    - PED list
    - Important clauses
    
    Args:
        raw_text: Raw OCR text from policy document
        
    Returns:
        Structured policy dict matching PolicyData schema, or None if parsing fails
        
    Example output:
        {
            "policy_id": "POL-456",
            "policy_holder_name": "John Doe",
            "insurer_name": "Star Health",
            "coverage_amount": 500000,
            "ped_list": ["Diabetes", "Hypertension"],
            "room_limit_type": "percentage",
            "room_limit_value": "1.0",
            "copay_percentage": 10
        }
    """
    
    prompt = f"""You are an AI Insurance Policy Analyst.

TASK: Extract all key information from this insurance policy document.

INPUT TEXT:
{raw_text}

OUTPUT FORMAT (MUST BE VALID JSON):
{{
  "policy_id": "string or null",
  "policy_holder_name": "string or null",
  "insurer_name": "string or null",
  "coverage_amount": number or null,
  "ped_list": ["Diabetes", "Hypertension"],
  "room_limit_type": "percentage" or "amount" or null,
  "room_limit_value": "1.0" or "5000" or null,
  "copay_percentage": number or null,
  "general_waiting_period_months": number or null,
  "specific_waiting_period_months": number or null
}}

CRITICAL RULES:
- Output ONLY valid JSON, no markdown
- Extract Pre-Existing Diseases (PED) as a list
- Room limit can be either percentage (e.g., "1.0" for 1% of sum insured) or fixed amount
- If a field is missing, use null or []
- Do NOT invent information
"""

    try:
        response = bedrock.converse(
            modelId=NOVA_LITE_MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.0}  # Deterministic
        )
        
        response_text = response['output']['message']['content'][0]['text']
        
        # Clean markdown code blocks if present
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        
        structured_data = json.loads(clean_json)
        
        print(f"✅ Structured policy with {len(structured_data.get('ped_list', []))} PEDs")
        return structured_data
        
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse AI response as JSON: {e}")
        print(f"   Response was: {response_text[:200]}...")
        return None
    except Exception as e:
        print(f"❌ Policy structuring failed: {e}")
        return None


def structure_and_categorize(bill_text: str, policy_text: str) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Structure both bill and policy documents in a single call.
    
    This is the main entry point for the structuring layer.
    
    Args:
        bill_text: Raw OCR text from hospital bill
        policy_text: Raw OCR text from policy document
        
    Returns:
        Dictionary with 'bill' and 'policy' keys, each containing structured data or None
        
    Example:
        >>> result = structure_and_categorize(bill_text, policy_text)
        >>> if result['bill'] and result['policy']:
        ...     # Feed to validation + rule engine
        ...     pass
    """
    return {
        "bill": structure_bill_from_text(bill_text),
        "policy": structure_policy_from_text(policy_text)
    }
