"""
Test OCR Service with AWS Textract Integration

This script tests the complete OCR workflow:
1. Upload document to S3
2. Extract text using OCR service
3. Clean up S3 files
"""

import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ocr.ocr_service import extract_text_from_document
from app.services.aws_service import upload_file_to_s3, delete_file_from_s3, AWSServiceError

def test_ocr_service():
    """Test OCR service end-to-end"""
    
    print("=" * 70)
    print("🧪 OCR SERVICE INTEGRATION TEST")
    print("=" * 70)
    
    # Test files
    test_cases = [
        {
            "name": "Hospital Bill (PDF)",
            "file": "sample_hospital_bill.pdf",
            "s3_key": "test/ocr_test_bill.pdf"
        },
        {
            "name": "Insurance Policy (PDF)",
            "file": "sample_insurance_policy.pdf",
            "s3_key": "test/ocr_test_policy.pdf"
        }
    ]
    
    results = []
    
    for test in test_cases:
        print(f"\n{'=' * 70}")
        print(f"📄 Testing: {test['name']}")
        print(f"{'=' * 70}")
        
        file_path = test['file']
        s3_key = test['s3_key']
        
        if not Path(file_path).exists():
            print(f"⚠️  SKIPPED: File not found - {file_path}")
            continue
        
        try:
            # Step 1: Upload to S3
            print(f"\n1️⃣  Uploading to S3...")
            s3_uri = upload_file_to_s3(file_path, s3_key)
            print(f"   ✅ Uploaded: {s3_uri}")
            
            # Step 2: Extract text using OCR service
            print(f"\n2️⃣  Extracting text with OCR service...")
            extracted_text = extract_text_from_document(file_path, s3_key)
            
            lines = extracted_text.split('\n')
            char_count = len(extracted_text)
            word_count = len(extracted_text.split())
            
            print(f"   ✅ Text extraction successful!")
            print(f"   📊 Statistics:")
            print(f"      - Lines: {len(lines)}")
            print(f"      - Words: {word_count}")
            print(f"      - Characters: {char_count}")
            
            # Show first few lines
            print(f"\n   📝 First 10 lines of extracted text:")
            for i, line in enumerate(lines[:10], 1):
                preview = line[:70] + "..." if len(line) > 70 else line
                if preview.strip():  # Only show non-empty lines
                    print(f"      {i}. {preview}")
            
            # Step 3: Cleanup
            print(f"\n3️⃣  Cleaning up S3...")
            delete_file_from_s3(s3_key)
            print(f"   ✅ Deleted from S3")
            
            results.append({
                "test": test['name'],
                "status": "PASSED",
                "lines": len(lines),
                "words": word_count,
                "chars": char_count
            })
            
        except Exception as e:
            print(f"\n❌ TEST FAILED: {str(e)}")
            results.append({
                "test": test['name'],
                "status": "FAILED",
                "error": str(e)
            })
            
            # Try to cleanup even on failure
            try:
                delete_file_from_s3(s3_key)
                print(f"   🗑️  Cleaned up S3 file")
            except:
                pass
    
    # Summary
    print(f"\n{'=' * 70}")
    print("📊 TEST SUMMARY")
    print(f"{'=' * 70}")
    
    passed = sum(1 for r in results if r['status'] == 'PASSED')
    failed = sum(1 for r in results if r['status'] == 'FAILED')
    
    for result in results:
        if result['status'] == 'PASSED':
            print(f"✅ {result['test']}")
            print(f"   Lines: {result['lines']}, Words: {result['words']}, Chars: {result['chars']}")
        else:
            print(f"❌ {result['test']}")
            print(f"   Error: {result.get('error', 'Unknown')}")
    
    print(f"\n{'=' * 70}")
    if failed == 0:
        print(f"✅ ALL TESTS PASSED ({passed}/{len(results)})")
        print(f"{'=' * 70}")
        print("\n🎉 OCR Service is working correctly!")
        print("✓ File upload to S3: OK")
        print("✓ Text extraction: OK")
        print("✓ S3 cleanup: OK")
        return True
    else:
        print(f"⚠️  {passed} PASSED, {failed} FAILED")
        print(f"{'=' * 70}")
        return False

if __name__ == "__main__":
    success = test_ocr_service()
    sys.exit(0 if success else 1)
