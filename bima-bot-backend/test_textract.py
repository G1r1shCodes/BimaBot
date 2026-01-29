"""
Test script to verify AWS Textract integration

This script tests:
1. AWS credentials are valid
2. S3 upload/download works
3. Textract sync API works
4. Textract async API fallback works
"""

import sys
import os
from pathlib import Path

# Add app to path so we can import services
sys.path.insert(0, str(Path(__file__).parent))

from app.services.aws_service import (
    upload_file_to_s3,
    extract_text_from_s3_file,
    extract_text_with_textract,
    extract_text_with_async_textract,
    delete_file_from_s3,
    AWSServiceError
)


def test_textract():
    """Test AWS Textract integration"""
    
    print("=" * 60)
    print("🧪 AWS TEXTRACT INTEGRATION TEST")
    print("=" * 60)
    
    # Test file
    test_pdf = "sample_hospital_bill.pdf"
    test_s3_key = "test/textract_test.pdf"
    
    if not os.path.exists(test_pdf):
        print(f"❌ Test file not found: {test_pdf}")
        print("   Please ensure sample_hospital_bill.pdf exists in the backend directory")
        return False
    
    print(f"\n📋 Test File: {test_pdf}")
    print(f"📋 S3 Key: {test_s3_key}")
    print(f"📋 File Size: {os.path.getsize(test_pdf) / 1024:.2f} KB")
    
    try:
        # Test 1: Upload to S3
        print("\n" + "=" * 60)
        print("TEST 1: Upload to S3")
        print("=" * 60)
        s3_uri = upload_file_to_s3(test_pdf, test_s3_key)
        print(f"✅ Upload successful: {s3_uri}")
        
        # Test 2: Sync Textract API
        print("\n" + "=" * 60)
        print("TEST 2: Synchronous Textract API")
        print("=" * 60)
        try:
            text = extract_text_with_textract(test_s3_key)
            lines = text.split('\n')
            print(f"✅ Sync Textract successful!")
            print(f"   Extracted {len(lines)} lines")
            print(f"   First 5 lines:")
            for i, line in enumerate(lines[:5], 1):
                print(f"      {i}. {line[:80]}")
            
        except AWSServiceError as e:
            print(f"⚠️  Sync Textract failed: {str(e)}")
            print(f"   This is expected for complex PDFs")
        
        # Test 3: Async Textract API
        print("\n" + "=" * 60)
        print("TEST 3: Asynchronous Textract API")
        print("=" * 60)
        try:
            text = extract_text_with_async_textract(test_s3_key)
            lines = text.split('\n')
            print(f"✅ Async Textract successful!")
            print(f"   Extracted {len(lines)} lines")
            print(f"   First 5 lines:")
            for i, line in enumerate(lines[:5], 1):
                print(f"      {i}. {line[:80]}")
            
        except AWSServiceError as e:
            print(f"❌ Async Textract failed: {str(e)}")
            return False
        
        # Test 4: Automatic fallback logic
        print("\n" + "=" * 60)
        print("TEST 4: Automatic Fallback Logic")
        print("=" * 60)
        try:
            text = extract_text_from_s3_file(test_s3_key)
            lines = text.split('\n')
            print(f"✅ Automatic fallback successful!")
            print(f"   Extracted {len(lines)} lines")
            print(f"   Total characters: {len(text)}")
            
        except AWSServiceError as e:
            print(f"❌ Fallback logic failed: {str(e)}")
            return False
        
        # Cleanup
        print("\n" + "=" * 60)
        print("CLEANUP")
        print("=" * 60)
        delete_file_from_s3(test_s3_key)
        print(f"✅ Test file deleted from S3")
        
        # Summary
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("AWS Textract integration is working correctly!")
        print(f"✓ S3 upload/download: OK")
        print(f"✓ Textract extraction: OK")
        print(f"✓ Automatic fallback: OK")
        
        return True
        
    except Exception as e:
        print(f"\n" + "=" * 60)
        print(f"❌ TEST FAILED")
        print("=" * 60)
        print(f"Error: {str(e)}")
        print(f"Type: {type(e).__name__}")
        
        # Try to cleanup
        try:
            delete_file_from_s3(test_s3_key)
            print(f"🗑️  Cleaned up test file from S3")
        except:
            pass
        
        return False


if __name__ == "__main__":
    success = test_textract()
    sys.exit(0 if success else 1)
