"""
Diagnostic Script: Test End-to-End Audit Flow

This will help us understand why the bill shows ₹0 and 0 observations.
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.services.audit_service import structure_and_categorize
from app.models.bill import HospitalBill

print("=" * 70)
print("🔍 Diagnostic: Bill Parsing Flow")
print("=" * 70)

# Sample bill text (typical hospital bill)
sample_bill_text = """
APOLLO HOSPITALS
Final Bill

Patient Name: Rajesh Kumar
Bill No: APH/2024/001
Date: 15-Jan-2024

CHARGES BREAKDOWN:
Room Rent (Private AC) - 3 days @ Rs 5,000/day    Rs 15,000
ICU Charges - 1 day                                Rs 12,000
Doctor Consultation                                Rs  2,000
Surgical Gloves (10 pairs)                         Rs    500
Medicines - Antibiotics                            Rs  3,500
X-Ray Chest                                        Rs  1,200
Blood Tests (CBC, LFT)                             Rs  2,800

TOTAL AMOUNT                                       Rs 37,000

Diagnosis: Pneumonia
"""

print("\n📄 Testing with sample bill text:")
print("-" * 70)
print(sample_bill_text[:200] + "...")

print("\n🧠 Step 1: AI Structuring + Fallback")
print("-" * 70)

try:
    result = structure_and_categorize(sample_bill_text, "Policy text placeholder")
    
    if result and result.get('bill'):
        bill_data = result['bill']
        print(f"✅ Bill parsing successful!")
        print(f"\n📊 Parsed Bill Data:")
        print(f"   Bill ID: {bill_data.get('bill_id', 'N/A')}")
        print(f"   Hospital: {bill_data.get('hospital_name', 'N/A')}")
        print(f"   Patient: {bill_data.get('patient_name', 'N/A')}")
        print(f"   Total Amount: ₹{bill_data.get('stated_total_amount', 0):,.2f}")
        print(f"   Currency: {bill_data.get('currency', 'N/A')}")
        
        charges = bill_data.get('charges', [])
        print(f"\n📋 Line Items ({len(charges)} items):")
        for idx, charge in enumerate(charges, 1):
            print(f"   {idx}. {charge.get('description', 'Unknown')} - "
                  f"₹{charge.get('amount', 0):,.2f} [{charge.get('category', 'N/A')}]")
        
        # Validate
        if bill_data.get('stated_total_amount', 0) == 0:
            print("\n❌ PROBLEM: Total amount is ₹0!")
        
        if len(charges) == 0:
            print("\n❌ PROBLEM: No line items found!")
            
    else:
        print("❌ Bill parsing completely failed - returned None")
        print(f"   Result: {result}")
        
except Exception as e:
    print(f"❌ Exception during parsing: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("🔍 Diagnosis Complete")
print("=" * 70)

# Check what the actual issue is
print("\n💡 Common Issues:")
print("1. If total is ₹0 but items exist → AI/fallback total extraction failed")
print("2. If 0 items exist → AI structuring failed AND fallback failed")
print("3. If both are 0 → OCR text is empty or malformed")
