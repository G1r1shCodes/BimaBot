"""
Simple S3 bucket test - Check if bucket exists or if we have permission issues
"""
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

region = os.getenv('AWS_REGION', 'us-east-1')
bucket = os.getenv('S3_BUCKET_NAME')

print(f"Testing bucket: {bucket}")
print(f"Region: {region}")
print("-" * 60)

# Create S3 client
s3 = boto3.client('s3', region_name=region)

# Test 1: Check if bucket exists (from our account perspective)
print("\n1. Testing HeadBucket (check if bucket exists)...")
try:
    response = s3.head_bucket(Bucket=bucket)
    print(f"✅ Bucket exists and is accessible!")
except ClientError as e:
    error_code = e.response['Error']['Code']
    print(f"❌ Error Code: {error_code}")
    print(f"   Message: {e.response['Error']['Message']}")
    
    if error_code == '404' or error_code == 'NoSuchBucket':
        print(f"\n💡 Solution: Bucket doesn't exist. Create it:")
        print(f"   aws s3 mb s3://{bucket} --region {region}")
    elif error_code == '403' or error_code == 'Forbidden':
        print(f"\n💡 Bucket may exist but you don't have permission.")
        print(f"   OR the bucket doesn't exist (AWS returns 403 instead of 404 for security)")
        print(f"\n   Try creating it anyway:")
        print(f"   aws s3 mb s3://{bucket} --region {region}")
    exit(1)

# Test 2: Try to list objects
print("\n2. Testing ListObjectsV2...")
try:
    response = s3.list_objects_v2(Bucket=bucket, MaxKeys=1)
    print(f"✅ Can list objects! Found {response.get('KeyCount', 0)} objects")
except ClientError as e:
    print(f"❌ Cannot list objects: {e.response['Error']['Code']}")
    print(f"   {e.response['Error']['Message']}")
    exit(1)

# Test 3: Try to upload a test file
print("\n3. Testing PutObject (upload permission)...")
try:
    test_key = "_test/connection_test.txt"
    s3.put_object(
        Bucket=bucket, 
        Key=test_key,
        Body=b"Connection test from BimaBot"
    )
    print(f"✅ Upload successful!")
    
    # Clean up
    s3.delete_object(Bucket=bucket, Key=test_key)
    print(f"✅ Delete successful!")
    
except ClientError as e:
    print(f"❌ Upload failed: {e.response['Error']['Code']}")
    print(f"   {e.response['Error']['Message']}")
    exit(1)

print("\n" + "=" * 60)
print("🎉 All S3 tests passed! BimaBot can use this bucket.")
print("=" * 60)
