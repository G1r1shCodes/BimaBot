"""
AWS Environment Variable Tester - For debugging backend .env loading
Run this from the backend directory to verify credentials are loaded
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

print("=" * 70)
print("Testing .env Loading from Backend Context")
print("=" * 70)

# Check current directory
cwd = Path.cwd()
print(f"\n📁 Current Working Directory: {cwd}")

# Check if .env exists
env_path = cwd / ".env"
print(f"📄 .env file path: {env_path}")
print(f"   Exists: {env_path.exists()}")

if env_path.exists():
    print(f"   Size: {env_path.stat().st_size} bytes")
    
# Load .env
print("\n🔄 Loading .env file...")
load_dotenv()

# Check environment variables
print("\n🔑 Environment Variables After Load:")
print("-" * 70)

vars_to_check = [
    'AWS_ACCESS_KEY_ID',
    'AWS_SECRET_ACCESS_KEY', 
    'AWS_REGION',
    'S3_BUCKET_NAME'
]

all_found = True
for var in vars_to_check:
    value = os.getenv(var)
    if value:
        if 'KEY' in var or 'SECRET' in var:
            display_value = f"{value[:10]}...{value[-4:]}" if len(value) > 14 else "***"
        else:
            display_value = value
        print(f"  ✅ {var}: {display_value}")
    else:
        print(f"  ❌ {var}: NOT FOUND")
        all_found = False

if not all_found:
    print("\n⚠️  Some environment variables are missing!")
    print("   Check your .env file in the backend directory")
    sys.exit(1)

# Test boto3 initialization
print("\n🔧 Testing boto3 Client Initialization:")
print("-" * 70)

try:
    import boto3
    
    # This mimics how aws_service.py creates clients
    region = os.getenv('AWS_REGION', 'us-east-1')
    
    s3 = boto3.client('s3', region_name=region)
    textract = boto3.client('textract', region_name=region)
    
    print(f"  ✅ S3 client created (region: {region})")
    print(f" ✅ Textract client created (region: {region})")
    
    # Test STS to verify credentials
    sts = boto3.client('sts', region_name=region)
    identity = sts.get_caller_identity()
    print(f"\n  ✅ Credentials validated via STS")
    print(f"     Account: {identity['Account']}")
    print(f"     User ARN: {identity['Arn']}")
    
except Exception as e:
    print(f"  ❌ Error: {e}")
    sys.exit(1)

# Test S3 bucket access
print("\n🪣 Testing S3 Bucket Access:")
print("-" * 70)

bucket = os.getenv('S3_BUCKET_NAME')
print(f"   Bucket: {bucket}")

try:
    s3.head_bucket(Bucket=bucket)
    print(f"  ✅ Bucket '{bucket}' is accessible!")
    
except Exception as e:
    error_str = str(e)
    print(f"  ❌ Cannot access bucket: {error_str}")
    
    if '404' in error_str or 'NoSuchBucket' in error_str:
        print(f"\n  💡 Bucket doesn't exist. Create it with:")
        print(f"     aws s3 mb s3://{bucket} --region {region}")
    elif '403' in error_str or 'Forbidden' in error_str:
        print(f"\n  💡 Permission denied. Your IAM user needs S3 permissions.")
        print(f"     See aws_diagnostic.md for the IAM policy to apply")
    
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ All checks passed! Backend should be able to use AWS services.")
print("=" * 70)
