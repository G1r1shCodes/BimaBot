"""
AWS Integration Test Script (No Real AWS Required)

This script tests BimaBot's AWS integration using mock services.
Perfect for development and testing without AWS credentials.
"""

import os
os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
os.environ['AWS_REGION'] = 'us-east-1'
os.environ['S3_BUCKET_NAME'] = 'bima-bot-hackathon-2026'

from moto import mock_s3, mock_textract
import boto3
from pathlib import Path

@mock_s3
@mock_textract
def test_aws_integration():
    """Test S3 and Textract integration with mock services"""
    
    print("🧪 Testing AWS Integration (Mock Mode)")
    print("=" * 50)
    
    # Create mock S3 bucket
    s3 = boto3.client('s3', region_name='us-east-1')
    s3.create_bucket(Bucket='bima-bot-hackathon-2026')
    print("✅ Created mock S3 bucket: bima-bot-hackathon-2026")
    
    # Create test file
    test_file = Path("test_document.txt")
    test_file.write_text("Sample hospital bill\nTotal: $1000\nDate: 2026-01-29")
    print(f"✅ Created test file: {test_file}")
    
    # Test upload
    try:
        s3.upload_file(str(test_file), 'bima-bot-hackathon-2026', 'audits/TEST-001/bill.txt')
        print("✅ Upload to S3: PASSED")
    except Exception as e:
        print(f"❌ Upload to S3: FAILED - {e}")
        return
    
    # Test list files
    try:
        response = s3.list_objects_v2(Bucket='bima-bot-hackathon-2026', Prefix='audits/')
        files = [obj['Key'] for obj in response.get('Contents', [])]
        print(f"✅ List S3 files: PASSED - Found {len(files)} file(s)")
        for file in files:
            print(f"   📄 {file}")
    except Exception as e:
        print(f"❌ List S3 files: FAILED - {e}")
    
    # Test Textract (mock returns empty for detect_document_text)
    try:
        textract = boto3.client('textract', region_name='us-east-1')
        response = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': 'bima-bot-hackathon-2026',
                    'Name': 'audits/TEST-001/bill.txt'
                }
            }
        )
        print(f"✅ Textract OCR: PASSED - Got response with {len(response.get('Blocks', []))} blocks")
    except Exception as e:
        print(f"❌ Textract OCR: FAILED - {e}")
    
    # Test delete
    try:
        s3.delete_object(Bucket='bima-bot-hackathon-2026', Key='audits/TEST-001/bill.txt')
        print("✅ Delete from S3: PASSED")
    except Exception as e:
        print(f"❌ Delete from S3: FAILED - {e}")
    
    # Cleanup
    test_file.unlink()
    print("✅ Cleaned up test file")
    
    print("=" * 50)
    print("✨ All mock AWS tests completed!\n")
    print("Next steps:")
    print("1. Configure real AWS credentials (see AWS_SETUP.md)")
    print("2. Run full integration test with BimaBot frontend")


if __name__ == "__main__":
    # Check if moto is installed
    try:
        import moto
        test_aws_integration()
    except ImportError:
        print("❌ moto not installed")
        print("\nInstall with: pip install moto[s3,textract]")
        print("Then run this script again.")
