"""
Quick AWS verification script - Run this to check if AWS is configured correctly
"""

import sys

def check_aws_credentials():
    """Check if AWS credentials are available"""
    print("🔍 Checking AWS Configuration...")
    print("=" * 60)
    
    # Check environment variables
    import os
    has_env_creds = bool(
        os.getenv('AWS_ACCESS_KEY_ID') and 
        os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    
    if has_env_creds:
        print("✅ AWS credentials found in environment variables")
        print(f"   AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')[:10]}...")
        print(f"   AWS_REGION: {os.getenv('AWS_REGION', 'us-east-1')}")
    else:
        print("ℹ️  No AWS credentials in environment variables")
    
    # Try boto3
    try:
        import boto3
        print("✅ boto3 is installed")
        
        # Try to get credentials
        try:
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials:
                print(f"✅ boto3 found credentials (Access Key: {credentials.access_key[:10]}...)")
            else:
                print("⚠️  boto3 couldn't find credentials")
        except Exception as e:
            print(f"⚠️  boto3 credentials check failed: {e}")
        
    except ImportError:
        print("❌ boto3 is not installed")
        print("   Install with: pip install boto3")
        return False
    
    # Try S3 connection
    print("\n🔗 Testing S3 Connection...")
    try:
        s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        bucket_name = os.getenv('S3_BUCKET_NAME', 'bima-bot-hackathon-2026')
        
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=1)
        print(f"✅ S3 connection successful!")
        print(f"   Bucket '{bucket_name}' is accessible")
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ S3 connection failed: {error_msg}")
        
        if "NoCredentialsError" in error_msg or "Unable to locate credentials" in error_msg:
            print("\n💡 Solution: Configure AWS credentials")
            print("   Option 1: Set environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)")
            print("   Option 2: Run 'aws configure' (requires AWS CLI)")
            print("   Option 3: Use .env file with python-dotenv")
        elif "NoSuchBucket" in error_msg:
            print(f"\n💡 Solution: Create S3 bucket '{bucket_name}'")
            print(f"   Run: aws s3 mb s3://{bucket_name} --region us-east-1")
        elif "AccessDenied" in error_msg or "InvalidAccessKeyId" in error_msg:
            print("\n💡 Solution: Check your AWS credentials")
            print("   - Verify Access Key ID and Secret Access Key")
            print("   - Check IAM permissions for S3 access")
        
        return False
    
    # Try Textract
    print("\n📄 Testing Textract Access...")
    try:
        textract = boto3.client('textract', region_name=os.getenv('AWS_REGION', 'us-east-1'))
        # Just verify the client was created (actual call would need a document)
        print("✅ Textract client initialized successfully")
        print("   (Full test requires a document to process)")
        
    except Exception as e:
        print(f"⚠️  Textract client creation failed: {e}")
    
    print("\n" + "=" * 60)
    print("✨ AWS Configuration Check Complete!\n")
    
    return True


if __name__ == "__main__":
    success = check_aws_credentials()
    
    if success:
        print("🎉 You're ready to use AWS services with BimaBot!")
        print("\nNext step: Run the audit workflow to test end-to-end")
    else:
        print("⚠️  AWS configuration incomplete")
        print("\nSee AWS_SETUP.md for detailed setup instructions")
        sys.exit(1)
