"""
Test Phase 4.1 PDF Upload Flow
Verifies backend API is working correctly
"""

import requests
import json
from pathlib import Path

API_BASE = "http://localhost:8000/audit"
BILL_PATH = Path("sample_hospital_bill.pdf")
POLICY_PATH = Path("sample_insurance_policy.pdf")

def test_phase_41_flow():
    print("🧪 Testing Phase 4.1 PDF Upload Flow\n")
    print("=" * 60)
    
    # Step 1: Start Audit
    print("\n📝 Step 1: Starting audit session...")
    try:
        response = requests.post(f"{API_BASE}/start")
        response.raise_for_status()
        data = response.json()
        audit_id = data["audit_id"]
        status = data["status"]
        print(f"✅ Audit created: {audit_id}")
        print(f"   Status: {status}")
    except Exception as e:
        print(f"❌ Failed to start audit: {e}")
        return
    
    # Step 2: Upload Files
    print("\n📤 Step 2: Uploading PDFs...")
    try:
        with open(BILL_PATH, "rb") as bill_file, open(POLICY_PATH, "rb") as policy_file:
            files = {
                "bill": ("sample_hospital_bill.pdf", bill_file, "application/pdf"),
                "policy": ("sample_insurance_policy.pdf", policy_file, "application/pdf")
            }
            response = requests.post(f"{API_BASE}/{audit_id}/upload", files=files)
            response.raise_for_status()
            data = response.json()
            print(f"✅ Files uploaded:")
            print(f"   Bill size: {data['bill_size_kb']:.2f} KB")
            print(f"   Policy size: {data['policy_size_kb']:.2f} KB")
            print(f"   Status: {data['status']}")
    except FileNotFoundError:
        print(f"❌ PDF files not found. Make sure you're running this from bima-bot-backend/")
        return
    except Exception as e:
        print(f"❌ Upload failed: {e}")
        return
    
    # Step 3: Trigger Processing
    print("\n⚙️ Step 3: Triggering audit processing...")
    try:
        response = requests.post(f"{API_BASE}/{audit_id}/complete")
        response.raise_for_status()
        data = response.json()
        print(f"✅ Processing triggered: {data['message']}")
    except Exception as e:
        print(f"❌ Processing failed: {e}")
        print(f"   Response: {response.text if 'response' in locals() else 'N/A'}")
        return
    
    # Step 4: Get Results
    print("\n📊 Step 4: Retrieving audit results...")
    try:
        response = requests.get(f"{API_BASE}/{audit_id}/result")
        response.raise_for_status()
        result = response.json()
        
        print(f"\n{'=' * 60}")
        print("AUDIT RESULTS")
        print(f"{'=' * 60}")
        
        print(f"\n💰 Financial Summary:")
        print(f"   Total Billed: ₹{result['total_billed']:,}")
        print(f"   Fully Covered: ₹{result['fully_covered_amount']:,}")
        print(f"   Under Review: ₹{result['amount_under_review']:,}")
        
        print(f"\n🚩 Flags Detected: {len(result['flags'])}")
        for i, flag in enumerate(result['flags'], 1):
            severity_emoji = {
                "error": "🔴",
                "warning": "🟡",
                "info": "🔵"
            }.get(flag['severity'], "⚪")
            
            print(f"\n   {severity_emoji} Flag #{i}: {flag['flag_type'].upper()}")
            print(f"      Severity: {flag['severity']}")
            print(f"      Reason: {flag['reason']}")
            if flag.get('amount_affected'):
                print(f"      Amount: ₹{flag['amount_affected']:,}")
            if flag.get('recommendation'):
                print(f"      💡 Recommendation: {flag['recommendation']}")
        
        print(f"\n📝 Dispute Letter Generated: {len(result['dispute_letter_content'])} characters")
        print(f"\n{'=' * 60}")
        print("✅ PHASE 4.1 TEST COMPLETE")
        print(f"{'=' * 60}\n")
        
    except Exception as e:
        print(f"❌ Failed to get results: {e}")
        print(f"   Response: {response.text if 'response' in locals() else 'N/A'}")
        return

if __name__ == "__main__":
    test_phase_41_flow()
