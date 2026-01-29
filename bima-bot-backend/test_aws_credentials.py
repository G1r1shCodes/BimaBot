"""
AWS Credentials Test Script

Run this script after updating your AWS credentials in .env file.
It will verify:
1. Credentials are valid
2. S3 bucket is accessible
3. Textract API permissions are correct

Usage:
    python test_aws_credentials.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

# Colors for terminal output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header(text):
    """Print a formatted header"""
    print(f"\n{BLUE}{BOLD}{'=' * 80}{RESET}")
    print(f"{BLUE}{BOLD}{text}{RESET}")
    print(f"{BLUE}{BOLD}{'=' * 80}{RESET}")

def print_success(text):
    """Print success message"""
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    """Print error message"""
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    """Print warning message"""
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    """Print info message"""
    print(f"   {text}")


def test_environment_variables():
    """Test 1: Check environment variables are loaded"""
    print_header("TEST 1: Environment Variables")
    
    load_dotenv()
    
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_REGION')
    s3_bucket = os.getenv('S3_BUCKET_NAME')
    
    all_present = True
    
    if aws_access_key:
        print_success(f"AWS_ACCESS_KEY_ID: {aws_access_key[:10]}... ({len(aws_access_key)} chars)")
    else:
        print_error("AWS_ACCESS_KEY_ID not found in .env file")
        all_present = False
    
    if aws_secret_key:
        print_success(f"AWS_SECRET_ACCESS_KEY: {aws_secret_key[:10]}... ({len(aws_secret_key)} chars)")
    else:
        print_error("AWS_SECRET_ACCESS_KEY not found in .env file")
        all_present = False
    
    if aws_region:
        print_success(f"AWS_REGION: {aws_region}")
    else:
        print_error("AWS_REGION not found in .env file")
        all_present = False
    
    if s3_bucket:
        print_success(f"S3_BUCKET_NAME: {s3_bucket}")
    else:
        print_error("S3_BUCKET_NAME not found in .env file")
        all_present = False
    
    if not all_present:
        print_error("FAILED: Missing required environment variables")
        print_info("Please ensure .env file exists with all required variables")
        return False
    
    return True, aws_access_key, aws_secret_key, aws_region, s3_bucket


def test_credentials_validity(aws_region):
    """Test 2: Verify AWS credentials are valid"""
    print_header("TEST 2: AWS Credentials Validity")
    
    try:
        sts = boto3.client('sts', region_name=aws_region)
        identity = sts.get_caller_identity()
        
        print_success("AWS credentials are VALID and ACTIVE")
        print_info(f"Account ID: {identity['Account']}")
        print_info(f"User ARN: {identity['Arn']}")
        print_info(f"User ID: {identity['UserId']}")
        
        return True
        
    except NoCredentialsError:
        print_error("FAILED: No AWS credentials found")
        print_info("Make sure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set")
        return False
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        
        print_error("FAILED: AWS credentials are INVALID")
        print_info(f"Error Code: {error_code}")
        print_info(f"Error Message: {error_msg}")
        
        if error_code == 'SignatureDoesNotMatch':
            print("\n" + YELLOW + "Possible causes:" + RESET)
            print_info("1. Access Key ID or Secret Access Key is incorrect")
            print_info("2. Credentials have expired")
            print_info("3. There are extra spaces or special characters in .env file")
        elif error_code == 'InvalidClientTokenId':
            print("\n" + YELLOW + "Possible causes:" + RESET)
            print_info("1. Access Key ID does not exist")
            print_info("2. IAM user has been deleted")
        
        return False


def test_s3_access(aws_region, s3_bucket):
    """Test 3: Verify S3 bucket access"""
    print_header("TEST 3: S3 Bucket Access")
    
    try:
        s3 = boto3.client('s3', region_name=aws_region)
        
        # Check bucket exists
        s3.head_bucket(Bucket=s3_bucket)
        print_success(f"S3 bucket '{s3_bucket}' is ACCESSIBLE")
        
        # Test read permission
        response = s3.list_objects_v2(Bucket=s3_bucket, MaxKeys=1)
        print_success("Read permission: OK")
        
        # Test write permission by uploading a tiny test file
        test_key = 'test/credentials_test.txt'
        s3.put_object(Bucket=s3_bucket, Key=test_key, Body=b'test')
        print_success("Write permission: OK")
        
        # Clean up test file
        s3.delete_object(Bucket=s3_bucket, Key=test_key)
        print_success("Delete permission: OK")
        
        return True
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        
        print_error("FAILED: Cannot access S3 bucket")
        print_info(f"Error Code: {error_code}")
        
        if error_code == '404' or error_code == 'NoSuchBucket':
            print_info(f"Bucket '{s3_bucket}' does not exist")
            print_info("Please create the bucket or update S3_BUCKET_NAME in .env")
        elif error_code == '403' or error_code == 'AccessDenied':
            print_info(f"Access denied to bucket '{s3_bucket}'")
            print_info("Your IAM user needs s3:GetObject, s3:PutObject, s3:DeleteObject permissions")
        
        return False


def test_textract_permissions(aws_region, s3_bucket):
    """Test 4: Verify Textract API permissions"""
    print_header("TEST 4: Textract Service Permissions")
    
    textract = boto3.client('textract', region_name=aws_region)
    sync_ok = False
    async_ok = False
    
    # Test sync API
    try:
        textract.detect_document_text(
            Document={'S3Object': {'Bucket': s3_bucket, 'Name': '__nonexistent_test__.pdf'}}
        )
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        
        if error_code == 'AccessDeniedException':
            print_error("Sync API: No permission for textract:DetectDocumentText")
            print_info("Add 'textract:DetectDocumentText' permission to your IAM user")
        elif error_code in ['InvalidS3ObjectException', 'InvalidParameterException']:
            print_success("Sync API: textract:DetectDocumentText permission OK")
            sync_ok = True
        else:
            print_warning(f"Sync API: Unexpected error: {error_code}")
    
    # Test async API
    try:
        textract.start_document_text_detection(
            DocumentLocation={'S3Object': {'Bucket': s3_bucket, 'Name': '__nonexistent_test__.pdf'}}
        )
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        
        if error_code == 'AccessDeniedException':
            print_error("Async API: No permission for textract:StartDocumentTextDetection")
            print_info("Add the following permissions to your IAM user:")
            print_info("  - textract:StartDocumentTextDetection")
            print_info("  - textract:GetDocumentTextDetection")
        elif error_code in ['InvalidS3ObjectException', 'InvalidParameterException']:
            print_success("Async API: textract:Start/GetDocumentTextDetection permissions OK")
            async_ok = True
        else:
            print_warning(f"Async API: Unexpected error: {error_code}")
    
    return sync_ok and async_ok


def main():
    """Run all tests"""
    print(f"\n{BOLD}{'=' * 80}{RESET}")
    print(f"{BOLD}{'AWS CREDENTIALS TEST SUITE'.center(80)}{RESET}")
    print(f"{BOLD}{'=' * 80}{RESET}")
    
    # Test 1: Environment variables
    result = test_environment_variables()
    if not result:
        sys.exit(1)
    
    _, aws_access_key, aws_secret_key, aws_region, s3_bucket = result
    
    # Test 2: Credentials validity
    if not test_credentials_validity(aws_region):
        print_header("TEST FAILED")
        print_error("Please update your AWS credentials in .env file and try again")
        sys.exit(1)
    
    # Test 3: S3 access
    if not test_s3_access(aws_region, s3_bucket):
        print_header("TEST FAILED")
        print_error("S3 access issue - check IAM permissions")
        sys.exit(1)
    
    # Test 4: Textract permissions
    textract_ok = test_textract_permissions(aws_region, s3_bucket)
    
    # Final summary
    print_header("TEST SUMMARY")
    
    if textract_ok:
        print(f"\n{GREEN}{BOLD}{'🎉 ALL TESTS PASSED! 🎉'.center(80)}{RESET}\n")
        print_success("AWS credentials are valid")
        print_success("S3 bucket is accessible")
        print_success("Textract API permissions are correct")
        print(f"\n{GREEN}You can now use AWS Textract for document processing!{RESET}")
        print(f"{BLUE}{'=' * 80}{RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{YELLOW}{BOLD}{'⚠️  PARTIAL SUCCESS ⚠️'.center(80)}{RESET}\n")
        print_success("AWS credentials are valid")
        print_success("S3 bucket is accessible")
        print_warning("Some Textract permissions are missing")
        print(f"\n{YELLOW}Add the missing Textract permissions to your IAM user to enable full functionality{RESET}")
        print(f"{BLUE}{'=' * 80}{RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Test interrupted by user{RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{RED}Unexpected error: {str(e)}{RESET}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
