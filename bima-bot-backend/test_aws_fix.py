"""Quick test to verify AWS credentials are working"""
from dotenv import load_dotenv
import os
import boto3

# Force reload .env
load_dotenv(override=True)

print("=" * 60)
print("🧪 TESTING FIXED AWS CREDENTIALS")
print("=" * 60)

# Test 1: Check environment variables are loaded
print("\n1️⃣  Checking .env file loading...")
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION')
bucket = os.getenv('S3_BUCKET_NAME')

print(f"   AWS_ACCESS_KEY_ID: {access_key}")
print(f"   AWS_SECRET_ACCESS_KEY: {secret_key[:10]}...{secret_key[-4:]}")
print(f"   AWS_REGION: {region}")
print(f"   S3_BUCKET_NAME: {bucket}")

# Test 2: Test S3 connection
print("\n2️⃣  Testing S3 connection...")
try:
    s3 = boto3.client('s3', region_name=region)
    response = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
    print(f"   ✅ SUCCESS! Found {response.get('KeyCount', 0)} objects")
    
    if response.get('Contents'):
        print("   Files in bucket:")
        for obj in response['Contents'][:5]:
            print(f"      - {obj['Key']}")
except Exception as e:
    print(f"   ❌ FAILED: {str(e)}")
    exit(1)

# Test 3: Test Textract client
print("\n3️⃣  Testing Textract client...")
try:
    textract = boto3.client('textract', region_name=region)
    print(f"   ✅ Textract client initialized: {textract}")
except Exception as e:
    print(f"   ❌ FAILED: {str(e)}")
    exit(1)

# Test 4: Test importing from aws_service
print("\n4️⃣  Testing aws_service.py module...")
try:
    from app.services.aws_service import list_s3_files, BUCKET_NAME
    files = list_s3_files()
    print(f"   ✅ Module imported successfully!")
    print(f"   Bucket: {BUCKET_NAME}")
    print(f"   Files found: {len(files)}")
except Exception as e:
    print(f"   ❌ FAILED: {str(e)}")
    exit(1)

print("\n" + "=" * 60)
print("✅ ALL TESTS PASSED - AWS INTEGRATION IS WORKING!")
print("=" * 60)
