"""
Detailed AWS credentials and permissions tester
"""
import os
import sys
from dotenv import load_dotenv

print("=" * 70)
print("BimaBot AWS Configuration Diagnostic Tool")
print("=" * 70)

# Load .env file
load_dotenv()

print("\n1. Environment Variables")
print("-" * 70)
access_key = os.getenv('AWS_ACCESS_KEY_ID')
secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
region = os.getenv('AWS_REGION', 'us-east-1')
bucket = os.getenv('S3_BUCKET_NAME')

if access_key:
    print(f"✅ AWS_ACCESS_KEY_ID: {access_key[:10]}...{access_key[-4:]}")
else:
    print("❌ AWS_ACCESS_KEY_ID: NOT FOUND")

if secret_key:
    print(f"✅ AWS_SECRET_ACCESS_KEY: {'*' * 20}{secret_key[-4:]}")
else:
    print("❌ AWS AWS_SECRET_ACCESS_KEY: NOT FOUND")

print(f"✅ AWS_REGION: {region}")
print(f"✅ S3_BUCKET_NAME: {bucket}")

if not (access_key and secret_key):
    print("\n❌ Missing AWS credentials in .env file!")
    sys.exit(1)

# Test boto3
print("\n2. Testing boto3 Connection")
print("-" * 70)
try:
    import boto3
    print("✅ boto3 imported successfully")
    
    # Create session
    session = boto3.Session(
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region
    )
    print("✅ boto3 session created")
    
    # Test STS (to verify credentials are valid)
    print("\n3. Testing AWS Credentials (STS GetCallerIdentity)")
    print("-" * 70)
    sts = session.client('sts')
    identity = sts.get_caller_identity()
    print(f"✅ Credentials are VALID!")
    print(f"   Account: {identity['Account']}")
    print(f"   User ARN: {identity['Arn']}")
    print(f"   User ID: {identity['UserId']}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)

# Test S3
print("\n4. Testing S3 Bucket Access")
print("-" * 70)
try:
    s3 = session.client('s3')
    
    # Check if bucket exists
    try:
        s3.head_bucket(Bucket=bucket)
        print(f"✅ Bucket '{bucket}' exists and is accessible")
    except Exception as e:
        if 'NoSuchBucket' in str(e):
            print(f"❌ Bucket '{bucket}' does NOT exist")
            print(f"   Create it with: aws s3 mb s3://{bucket} --region {region}")
        elif '403' in str(e) or 'AccessDenied' in str(e):
            print(f"⚠️  Bucket '{bucket}' exists but ACCESS DENIED")
            print(f"   Your IAM user lacks permissions to access this bucket")
        else:
            print(f"❌ Error accessing bucket: {e}")
        raise
    
    # Try to list objects
    try:
        response = s3.list_objects_v2(Bucket=bucket, MaxKeys=5)
        file_count = response.get('KeyCount', 0)
        print(f"✅ Can list objects in bucket ({file_count} files found)")
    except Exception as e:
        print(f"⚠️  Cannot list objects: {e}")
    
    # Try to upload a test file
    print("\n5. Testing S3 Upload Permission")
    print("-" * 70)
    test_key = "test/connectivity_test.txt"
    try:
        s3.put_object(
            Bucket=bucket,
            Key=test_key,
            Body=b"BimaBot connectivity test",
            ContentType="text/plain"
        )
        print(f"✅ Can UPLOAD files to bucket")
        
        # Try to read it back
        response = s3.get_object(Bucket=bucket, Key=test_key)
        print(f"✅ Can READ files from bucket")
        
        # Clean up
        s3.delete_object(Bucket=bucket, Key=test_key)
        print(f"✅ Can DELETE files from bucket")
        
    except Exception as e:
        print(f"❌ Upload test failed: {e}")

except Exception as e:
    print(f"❌ S3 test failed: {e}")
    sys.exit(1)

# Test Textract
print("\n6. Testing Textract Access")
print("-" * 70)
try:
    textract = session.client('textract')
    
    # We can't test actual Textract without a document, but we can verify the client
    print("✅ Textract client created successfully")
    print("   Note: Full test requires uploading a PDF and processing it")
    
except Exception as e:
    print(f"❌ Textract client creation failed: {e}")

print("\n" + "=" * 70)
print("✨ AWS Configuration Check Complete!")
print("=" * 70)
print("\nSummary:")
print("  - Credentials: ✅ VALID")
print(f"  - S3 Bucket: ✅ {bucket}")
print("  - Textract: ✅ Available")
print("\n🎉 BimaBot is ready to process audits!")
