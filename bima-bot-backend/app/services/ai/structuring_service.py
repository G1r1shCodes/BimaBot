import boto3
import json
import os

REGION = os.getenv('AWS_REGION', 'us-east-1')
# Nova Lite is fast and perfect for extraction
MODEL_ID = "amazon.nova-lite-v1:0" 

bedrock = boto3.client('bedrock-runtime', region_name=REGION)

def structure_and_categorize(raw_text):
    print(f"🧠 Nova Lite: Structuring Bill Data...")
    prompt = f"""
    You are a Medical Bill Data Entry Expert.
    
    TASK:
    Convert the raw OCR text below into a structured JSON list of line items.
    
    RULES:
    1. Extract 'description' (Item Name).
    2. Extract 'amount' (Price).
    3. Assign a 'category' from: [Room Rent, Pharmacy, Consumables, Surgery, Doctor Fees, Diagnostics, Admin, Other].
    
    RAW TEXT:
    {raw_text[:15000]}
    
    OUTPUT FORMAT (JSON ONLY):
    {{
      "items": [
        {{ "description": "Gloves", "amount": 500, "category": "Consumables" }},
        {{ "description": "Consultation", "amount": 1000, "category": "Doctor Fees" }}
      ]
    }}
    """
    
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.0}
        )
        
        response_text = response['output']['message']['content'][0]['text']
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        
        # --- SAFETY FIX 1: Handle List Return ---
        if isinstance(data, list):
            return {"items": data}
            
        # --- SAFETY FIX 2: Handle Empty/Bad Dict ---
        if isinstance(data, dict):
            if "items" not in data:
                return {"items": []}
            return data
            
        return {"items": []}

    except Exception as e:
        print(f"❌ Structuring Failed: {e}")
        return {"items": []}

def parse_policy_limits(policy_text: str) -> dict:
    """
    Extracts policy limits and entities from policy text using Nova Lite.
    """
    print(f"🧠 Nova Lite: Structuring Policy Data...")
    prompt = f"""
    You are an Insurance Policy Analyst.
    
    TASK:
    Extract key policy limits and entity details from the text below.
    
    RULES:
    1. Extract 'policy_id' (Policy Number).
    2. Extract 'patient_name' (Policy Holder Name).
    3. Extract 'insurer_name' (Insurance Company).
    4. Extract 'coverage_amount' (Sum Insured).
    5. Extract 'ped_list' (Pre-existing Diseases if any).
    
    RAW TEXT:
    {policy_text[:15000]}
    
    OUTPUT FORMAT (JSON ONLY):
    {{
      "policy_id": "P-12345",
      "patient_name": "John Doe",
      "insurer_name": "Health Insurer Ltd",
      "coverage_amount": 500000,
      "ped_list": ["Diabetes", "Hypertension"]
    }}
    """
    
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.0}
        )
        
        response_text = response['output']['message']['content'][0]['text']
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        
        if isinstance(data, dict):
            return data
        return {}
        
    except Exception as e:
        print(f"❌ Policy Structuring Failed: {e}")
        return {}

def extract_header_details(bill_text, policy_text):
    print(f"🔍 Nova Lite: Extracting Entity Metadata...")
    prompt = f"""
    You are a Data Extraction Specialist.
    
    TASK:
    Extract the following entities from the texts provided.
    
    SOURCES:
    1. BILL TEXT: {bill_text[:5000]}
    2. POLICY TEXT: {policy_text[:5000]}
    
    OUTPUT JSON format:
    {{
      "patient_name": "Full Name",
      "policy_number": "Policy Number",
      "insurer_name": "Insurance Company",
      "insurer_address": "City/Branch",
      "bill_number": "Invoice No",
      "bill_date": "Date"
    }}
    """
    
    try:
        response = bedrock.converse(
            modelId=MODEL_ID,
            messages=[{"role": "user", "content": [{"text": prompt}]}],
            inferenceConfig={"temperature": 0.0}
        )
        
        response_text = response['output']['message']['content'][0]['text']
        clean_json = response_text.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        
        # Safety check
        if isinstance(data, dict):
            return data
        return {} 

    except Exception as e:
        print(f"❌ Entity Extraction Failed: {e}")
        return {}
