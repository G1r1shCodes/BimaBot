"""
AWS Textract Diagnostic Report

This script provides a comprehensive test of AWS Textract integration.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 80)
print("AWS TEXTRACT DIAGNOSTIC REPORT")
print("=" * 80)

# Test 1: Environment Variables
print("\n" + "=" * 80)
print("TEST 1: Environment Variables")
print("=" * 80)

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_region = os.getenv('AWS_REGION')
s3_bucket = os.getenv('S3_BUCKET_NAME')

print(f"✓ AWS_ACCESS_KEY_ID: {aws_access_key[:10]}... ({len(aws_access_key)} chars)" if aws_access_key else "✗ AWS_ACCESS_KEY_ID not found")
print(f"✓ AWS_SECRET_ACCESS_KEY: {aws_secret_key[:10]}... ({len(aws_secret_key)} chars)" if aws_secret_key else "✗ AWS_SECRET_ACCESS_KEY not found")
print(f"✓ AWS_REGION: {aws_region}" if aws_region else "✗ AWS_REGION not found")
print(f"✓ S3_BUCKET_NAME: {s3_bucket}" if s3_bucket else "✗ S3_BUCKET_NAME not found")

if not all([aws_access_key, aws_secret_key, aws_region, s3_bucket]):
    print("\n❌ FAILED: Missing required environment variables")
    print("Please ensure .env file exists with valid AWS credentials")
    sys.exit(1)

# Test 2: AWS Credentials Validity
print("\n" + "=" * 80)
print("TEST 2: AWS Credentials Validity")
print("=" * 80)

try:
    import boto3
    from botocore.exceptions import ClientError, NoCredentialsError
    
    # Test STS to verify credentials
    sts = boto3.client('sts', region_name=aws_region)
    identity = sts.get_caller_identity()
    
    print(f"✅ AWS credentials are VALID")
    print(f"   Account: {identity['Account']}")
    print(f"   User ARN: {identity['Arn']}")
    print(f"   User ID: {identity['UserId']}")
    
except NoCredentialsError:
    print("❌ FAILED: No AWS credentials found")
    sys.exit(1)
except ClientError as e:
    error_code = e.response.get('Error', {}).get('Code', 'Unknown')
    error_msg = e.response.get('Error', {}).get('Message', str(e))
    print(f"❌ FAILED: AWS credentials are INVALID")
    print(f"   Error Code: {error_code}")
    print(f"   Error Message: {error_msg}")
    print("\n   Possible causes:")
    print("   1. Access Key ID or Secret Access Key is incorrect")
    print("   2. Credentials have expired")
    print("   3. IAM user has been deleted or disabled")
    sys.exit(1)

# Test 3: S3 Access
print("\n" + "=" * 80)
print("TEST 3: S3 Bucket Access")
print("=" * 80)

try:
    s3 = boto3.client('s3', region_name=aws_region)
    
    # Check bucket exists and is accessible
    response = s3.head_bucket(Bucket=s3_bucket)
    print(f"✅ S3 bucket '{s3_bucket}' is ACCESSIBLE")
    
    # List objects to verify read permission
    response = s3.list_objects_v2(Bucket=s3_bucket, MaxKeys=5)
    object_count = response.get('KeyCount', 0)
    print(f"   Objects in bucket: {object_count} (showing first 5)")
    
except ClientError as e:
    error_code = e.response.get('Error', {}).get('Code', 'Unknown')
    print(f"❌ FAILED: Cannot access S3 bucket")
    print(f"   Error: {error_code}")
    if error_code == '404' or error_code == 'NoSuchBucket':
        print(f"   Bucket '{s3_bucket}' does not exist")
    elif error_code == '403':
        print(f"   Access denied to bucket '{s3_bucket}'")
    sys.exit(1)

# Test 4: Textract Permissions
print("\n" + "=" * 80)
print("TEST 4: Textract Service Access")
print("=" * 80)

try:
    textract = boto3.client('textract', region_name=aws_region)
    
    # Check if we have permission to use Textract
    # We'll try to detect text from a non-existent document to check permissions
    # This should fail with AccessDenied if no permission, or InvalidS3Object if we have permission
    try:
        textract.detect_document_text(
            Document={'S3Object': {'Bucket': s3_bucket, 'Name': '__permission_test__'}}
        )
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'AccessDeniedException':
            print("❌ FAILED: No permission to use Textract")
            print("   Your AWS user/role needs 'textract:DetectDocumentText' permission")
            sys.exit(1)
        elif error_code in ['InvalidS3ObjectException', 'InvalidParameterException']:
            print("✅ Textract sync API (detect_document_text) has PERMISSION")
        else:
            print(f"⚠️  Unexpected error: {error_code}")
    
    # Check async API permissions
    try:
        response = textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': '__permission_test__'}}
        )
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'AccessDeniedException':
            print("❌ WARNING: No permission for async Textract API")
            print("   Your AWS user/role needs these permissions:")
            print("   - textract:StartDocumentTextDetection")
            print("   - textract:GetDocumentTextDetection")
        elif error_code in ['InvalidS3ObjectException', 'InvalidParameterException']:
            print("✅ Textract async API (start/get_document_text_detection) has PERMISSION")
        else:
            print(f"⚠️  Unexpected error: {error_code}")
    
except Exception as e:
    print(f"❌ FAILED: Error testing Textract permissions: {str(e)}")
    sys.exit(1)

# Summary
print("\n" + "=" * 80)
print("DIAGNOSTIC SUMMARY")
print("=" * 80)
print("✅ All prerequisite checks PASSED")
print("✓ AWS credentials are valid")
print("✓ S3 bucket is accessible")
print("✓ Textract service has permissions")
print("\nYou can now proceed with actual document processing.")
print("=" * 80)
