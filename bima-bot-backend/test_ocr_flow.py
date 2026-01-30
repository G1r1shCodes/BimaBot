"""
End-to-End OCR Test - Verify S3 Upload and Textract Extraction

This will test the actual OCR flow using the reference pattern.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.services.aws_service import upload_file_to_s3, extract_text_with_async_textract
import time

print("=" * 70)
print("🧪 Testing S3 Upload + Textract OCR (Reference Pattern)")
print("=" * 70)

# Test with a simple text file first
test_content = """
APOLLO HOSPITALS
Final Bill

Patient Name: Test Patient
Bill No: TEST-001
Date: 30-Jan-2024

CHARGES BREAKDOWN:
Room Rent - 1 day @ Rs 5,000/day    Rs 5,000
Doctor Consultation                 Rs 2,000

TOTAL AMOUNT                        Rs 7,000
"""

# Create a test file
test_file_path = "test_bill.txt"
with open(test_file_path, 'w') as f:
    f.write(test_content)

try:
    # Step 1: Upload to S3
    print("\n📤 Step 1: Uploading test file to S3...")
    s3_key = "test/test_bill.txt"
    upload_file_to_s3(test_file_path, s3_key)
    print(f"✅ Uploaded to s3://{s3_key}")
    
    # Step 2: Extract text using async Textract (reference pattern)
    print("\n🔍 Step 2: Extracting text with Textract (async)...")
    extracted_text = extract_text_with_async_textract(s3_key)
    
    print(f"\n✅ Extraction successful!")
    print(f"📊 Extracted {len(extracted_text)} characters")
    print(f"\n📄 Extracted Text:")
    print("-" * 70)
    print(extracted_text[:500] if len(extracted_text) > 500 else extracted_text)
    print("-" * 70)
    
    # Cleanup
    os.remove(test_file_path)
    print("\n✅ Test passed! OCR flow is working.")
    
except Exception as e:
    print(f"\n❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

print("\n" + "=" * 70)
