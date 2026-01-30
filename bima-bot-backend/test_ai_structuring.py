"""
Diagnostic test for AWS Bedrock AI Structuring
"""
import boto3
import os
from dotenv import load_dotenv

load_dotenv()

print("AWS BEDROCK AI STRUCTURING DIAGNOSTIC")
print("=" * 70)

# 1. Check environment variables
print("\nStep 1: Environment Variables")
print("-" * 70)
region = os.getenv('AWS_REGION', 'NOT SET')
access_key = os.getenv('AWS_ACCESS_KEY_ID', 'NOT SET')

print(f"AWS_REGION: {region}")
print(f"AWS_ACCESS_KEY_ID: {'SET' if access_key != 'NOT SET' else 'NOT SET'}")

# 2. Test AWS credentials
print("\nStep 2: AWS Credentials Test")
print("-" * 70)
try:
    sts = boto3.client('sts', region_name=region)
    identity = sts.get_caller_identity()
    print(f"SUCCESS - AWS Credentials Valid")
    print(f"   Account: {identity['Account']}")
except Exception as e:
    print(f"FAILED - AWS Credentials Test: {e}")
    exit(1)

# 3. Test Bedrock client connection
print("\nStep 3: Bedrock Client Connection")
print("-" * 70)
try:
    bedrock = boto3.client('bedrock-runtime', region_name=region)
    print("SUCCESS - Bedrock client created")
except Exception as e:
    print(f"FAILED - Bedrock client: {e}")
    exit(1)

# 4. Test Nova Lite model access
print("\nStep 4: Nova Lite Model Test")
print("-" * 70)
model_id = "amazon.nova-lite-v1:0"
test_prompt = "Extract the total amount: Total Rs. 15000"

try:
    response = bedrock.converse(
        modelId=model_id,
        messages=[{"role": "user", "content": [{"text": test_prompt}]}],
        inferenceConfig={"temperature": 0.0}
    )
    
    response_text = response['output']['message']['content'][0]['text']
    print(f"SUCCESS - Nova Lite working!")
    print(f"   Response: {response_text[:80]}...")
    
except Exception as e:
    print(f"FAILED - Nova Lite test: {e}")
    print("\nSOLUTION:")
    print("   1. Go to AWS Console -> Bedrock")
    print("   2. Click 'Model access'")
    print("   3. Enable 'Amazon Nova Lite'")
    exit(1)

# 5. Test full structuring
print("\nStep 5: Full Structuring Pipeline")
print("-" * 70)
try:
    from app.services.ai.structuring_service import structure_bill_from_text
    
    sample_bill = "Apollo Hospital\nRoom Charges: Rs. 5000\nTotal: Rs. 10000"
    
    result = structure_bill_from_text(sample_bill)
    
    if result:
        print("SUCCESS - AI structuring working!")
        print(f"   Hospital: {result.get('hospital_name', 'N/A')}")
        print(f"   Charges: {len(result.get('charges', []))}")
    else:
        print("WARNING - AI structuring returned None")
        print("   Fallback parser will be used")
        
except Exception as e:
    print(f"FAILED - Structuring test: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("DIAGNOSTIC COMPLETE")
print("=" * 70)
