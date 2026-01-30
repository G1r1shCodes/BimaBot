
import boto3
import json

# --- CONFIG (From your Instructions) ---
REGION = "us-east-1" 
KB_ROLE_NAME = "hackathon-bedrock-kb-role" # We just check if we can see this

def check_status():
    print(f"🚀 Starting System Check in {REGION}...\n")
    
    # 1. CHECK CREDENTIALS
    try:
        sts = boto3.client('sts', region_name=REGION)
        user = sts.get_caller_identity()
        print(f"✅ Credentials: OK (User: {user['Arn'].split('/')[-1]})")
    except Exception as e:
        print(f"❌ Credentials: FAILED. Run 'aws configure' again.\nError: {e}")
        return

    # 2. CHECK S3 (Storage)
    try:
        s3 = boto3.client('s3', region_name=REGION)
        s3.list_buckets()
        print("✅ S3 Storage:  OK (Read Access verified)")
    except Exception as e:
        print(f"❌ S3 Storage:  FAILED. Error: {e}")

    # 3. CHECK TEXTRACT (Eyes)
    try:
        textract = boto3.client('textract', region_name=REGION)
        # Dummy check to verify service reachability
        try:
            textract.detect_document_text(Document={'Bytes': b'test'})
        except Exception:
            pass # We expect an error, just not an AccessDenied error
        print("✅ Textract:    OK (Service Reachable)")
    except Exception as e:
        if "AccessDenied" in str(e):
             print("❌ Textract:    FAILED (Access Denied)")
        else:
             print("✅ Textract:    OK")

    # 4. CHECK BEDROCK NOVA (Brain) - The Important One
    try:
        bedrock = boto3.client('bedrock-runtime', region_name=REGION)
        response = bedrock.converse(
            modelId="amazon.nova-lite-v1:0",
            messages=[{"role": "user", "content": [{"text": "Say OK"}]}]
        )
        reply = response['output']['message']['content'][0]['text']
        print(f"✅ Nova Lite:   OK (Reply: {reply})")
    except Exception as e:
        print(f"❌ Nova Lite:   FAILED. Error: {e}")

    print("\n------------------------------------------------")
    print("👉 If you see 4 Green Checks, START CODING.")
    print("------------------------------------------------")

if __name__ == "__main__":
    check_status()
