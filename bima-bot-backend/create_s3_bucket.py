"""
S3 Bucket Creator - Creates the BimaBot S3 bucket if it doesn't exist
"""
import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError

load_dotenv()

region = os.getenv('AWS_REGION', 'us-east-1')
bucket = os.getenv('S3_BUCKET_NAME')

print("=" * 70)
print("BimaBot S3 Bucket Setup")
print("=" * 70)
print(f"\nBucket name: {bucket}")
print(f"Region: {region}\n")

s3 = boto3.client('s3', region_name=region)

# Try to create the bucket
print("Attempting to create bucket...")
try:
    if region == 'us-east-1':
        # us-east-1 doesn't use LocationConstraint
        s3.create_bucket(Bucket=bucket)
    else:
        s3.create_bucket(
            Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
    print(f"✅ Bucket '{bucket}' created successfully!")
    
except ClientError as e:
    error_code = e.response['Error']['Code']
    
    if error_code == 'BucketAlreadyOwnedByYou':
        print(f"✅ Bucket already exists and you own it!")
    elif error_code == 'BucketAlreadyExists':
        print(f"❌ Bucket name is taken by another AWS account")
        print(f"   Choose a different bucket name in .env")
        exit(1)
    elif error_code == 'AccessDenied':
        print(f"❌ Permission denied - you cannot create buckets")
        print(f"   Your IAM user needs 's3:CreateBucket' permission")
        exit(1)
    else:
        print(f"❌ Error: {error_code}")
        print(f"   {e.response['Error']['Message']}")
        exit(1)

# Verify we can access it now
print("\nVerifying bucket access...")
try:
    s3.head_bucket(Bucket=bucket)
    print(f"✅ Bucket is accessible!")
    
    # Try upload/delete test
    print("\nTesting upload permissions...")
    test_key = "_test/setup_test.txt"
    s3.put_object(Bucket=bucket, Key=test_key, Body=b"Setup test")
    print(f"✅ Upload works!")
    
    s3.delete_object(Bucket=bucket, Key=test_key)
    print(f"✅ Delete works!")
    
except ClientError as e:
    print(f"❌ Still cannot access bucket: {e}")
    exit(1)

print("\n" + "=" * 70)
print("🎉 S3 bucket is ready for BimaBot!")
print("=" * 70)
print("\nNext: Restart your backend server and try the audit flow!")
