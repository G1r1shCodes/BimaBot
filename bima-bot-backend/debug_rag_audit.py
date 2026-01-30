import boto3
import os
import json
from dotenv import load_dotenv

# Load env but we might override
load_dotenv()

REGION = os.getenv('AWS_REGION', 'us-east-1')
bedrock_agent = boto3.client('bedrock-agent', region_name=REGION)
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime', region_name=REGION)

MODEL_ARN = "arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0"

def list_knowledge_bases():
    print("🔍 Listing Knowledge Bases...")
    try:
        response = bedrock_agent.list_knowledge_bases(maxResults=10)
        summaries = response.get('knowledgeBaseSummaries', [])
        print(f"Found {len(summaries)} KBs.")
        for kb in summaries:
            print(f" - Name: {kb['name']}, ID: {kb['knowledgeBaseId']}, Status: {kb['status']}")
            
        # Return the first active one if any
        for kb in summaries:
            if kb['status'] == 'ACTIVE':
                return kb['knowledgeBaseId']
        return None
    except Exception as e:
        print(f"❌ Failed to list KBs: {e}")
        return None

def test_audit_claim(kb_id):
    print(f"\n🧪 Testing audit_claim with KB ID: {kb_id}")
    
    # Mock Data
    bill_data = {
        "items": [
            {"description": "Room Rent", "amount": 5000, "category": "Room Rent"},
            {"description": "Gloves", "amount": 200, "category": "Consumables"}
        ]
    }
    policy_limits = {"room_rent_limit": 3000, "consumables_covered": False}
    
    prompt = f"""
    You are a Senior Insurance Auditor AI.
    [INPUT]
    Bill: {json.dumps(bill_data)}
    Policy: {json.dumps(policy_limits)}
    [TASK]
    Audit these items. Output JSON.
    """
    
    try:
        response = bedrock_agent_runtime.retrieve_and_generate(
            input={'text': prompt},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': kb_id,
                    'modelArn': MODEL_ARN
                }
            }
        )
        print("✅ RAG Response received!")
        print(response['output']['text'][:500])
        return True
    except Exception as e:
        print(f"❌ RAG Execution Failed: {e}")
        return False

if __name__ == "__main__":
    kb_id = "OIAANDNCSY" # Hardcoded from .env to verify
    print(f"Force testing KB ID: {kb_id}")
    if kb_id:
        test_audit_claim(kb_id)
    else:
        print("⚠️ No Active Knowledge Base found. RAG will fail.")
