"""
Test Script: RAG, Dispute Letter, and Explanation Services

Tests:
1. RAG Service - Bedrock Knowledge Base retrieval
2. Dispute Letter Generation - Nova Pro
3. Explanation Service - RAG explanations for rules
"""

import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from app.services.ai.rag_service import (
    get_rag_explanation,
    explain_consumables_exclusion,
    explain_room_rent_limits,
    explain_ped_waiting_period
)
from app.services.reporting.letter_generator import generate_dispute_letter
from app.models.bill import HospitalBill, LineItem, ChargeCategory
from app.models.policy import PolicyData, SubLimit
from app.models.audit import AuditFlag, FlagType, FlagSeverity

print("=" * 70)
print("🧪 Testing RAG, Dispute Letter, and Explanation Services")
print("=" * 70)

# Test 1: RAG Service - Direct Query
print("\n📚 TEST 1: RAG Service - Direct Query")
print("-" * 70)
try:
    explanation = get_rag_explanation("Why are consumables like gloves excluded from health insurance?")
    if explanation:
        print(f"✅ RAG Query Successful")
        print(f"Response: {explanation[:200]}..." if len(explanation) > 200 else f"Response: {explanation}")
    else:
        print("⚠️ RAG returned None (KB might not be configured or query failed)")
except Exception as e:
    print(f"❌ RAG Query Failed: {e}")

# Test 2: RAG Service - Helper Functions
print("\n📚 TEST 2: RAG Service - Explanation Helpers")
print("-" * 70)
try:
    print("Testing explain_consumables_exclusion()...")
    consumables_exp = explain_consumables_exclusion()
    print(f"✅ Consumables: {consumables_exp[:150]}...")
    
    print("\nTesting explain_room_rent_limits()...")
    room_exp = explain_room_rent_limits()
    print(f"✅ Room Rent: {room_exp[:150]}...")
    
    print("\nTesting explain_ped_waiting_period()...")
    ped_exp = explain_ped_waiting_period()
    print(f"✅ PED: {ped_exp[:150]}...")
    
except Exception as e:
    print(f"❌ Explanation Helpers Failed: {e}")

# Test 3: Dispute Letter Generation
print("\n✉️ TEST 3: Dispute Letter Generation")
print("-" * 70)
try:
    # Create sample bill
    sample_bill = HospitalBill(
        bill_id="BILL-TEST-001",
        patient_name="John Doe",
        admission_date="2024-01-15",
        discharge_date="2024-01-18",
        hospital_name="City Hospital",
        diagnosis=["Appendicitis"],
        charges=[
            LineItem(
                line_item_id="LI-001",
                label="Room Rent",
                category=ChargeCategory.ROOM_RENT,
                amount=15000.0,
                raw_text="Private Room - 3 days @ 5000/day"
            ),
            LineItem(
                line_item_id="LI-002",
                label="Surgical Gloves",
                category=ChargeCategory.CONSUMABLES,
                amount=500.0,
                raw_text="Gloves (10 pairs)"
            ),
            LineItem(
                line_item_id="LI-003",
                label="Surgeon Fee",
                category=ChargeCategory.SURGERY,
                amount=50000.0,
                raw_text="Laparoscopic Appendectomy"
            )
        ],
        stated_total_amount=65500.0,
        currency="INR"
    )
    
    # Create sample policy
    sample_policy = PolicyData(
        policy_id="POL-2024-12345",
        policy_holder_name="John Doe",
        insurer_name="National Health Insurance",
        coverage_amount=500000.0,
        ped_list=["Diabetes", "Hypertension"],
        general_waiting_period_months=30,
        ped_waiting_period_months=48,
        room_limit_type="amount",
        room_limit_value="3000",
        copay_percentage=10.0,
        sub_limits=[
            SubLimit(
                category="consumables",
                limit_amount=0.0  # 0 means excluded
            )
        ]
    )
    
    # Create sample flags
    sample_flags = [
        AuditFlag(
            flag_type=FlagType.CONSUMABLES,
            severity=FlagSeverity.WARNING,
            line_item_id="LI-002",
            reason="Consumables (Surgical Gloves) are excluded per policy terms",
            amount_affected=500.0,
            policy_clause="Clause 4.2.1"
        ),
        AuditFlag(
            flag_type=FlagType.ROOM_RENT,
            severity=FlagSeverity.WARNING,
            line_item_id="LI-001",
            reason="Room rent (₹5,000/day) exceeds policy limit (₹3,000/day)",
            amount_affected=6000.0,
            policy_clause="Clause 2.3"
        )
    ]
    
    print("Generating dispute letter with Nova Pro...")
    letter = generate_dispute_letter(sample_bill, sample_policy, sample_flags)
    
    print(f"✅ Dispute Letter Generated ({len(letter)} characters)")
    print("\n" + "=" * 70)
    print("GENERATED LETTER:")
    print("=" * 70)
    print(letter)
    print("=" * 70)
    
except Exception as e:
    print(f"❌ Dispute Letter Generation Failed: {e}")
    import traceback
    traceback.print_exc()

# Summary
print("\n" + "=" * 70)
print("✅ Test Suite Complete")
print("=" * 70)
print("\n📊 Summary:")
print("- RAG Service: Tests ability to retrieve explanations from Bedrock KB")
print("- Dispute Letter: Tests Nova Pro-powered letter generation")
print(" - Explanation Helpers: Tests pre-configured RAG queries")
print("\nIf any service shows '⚠️ using fallback', it means:")
print("  1. RAG Service: BEDROCK_KB_ID not configured or KB doesn't exist")
print("  2. Dispute Letter: Nova Pro unavailable, using template")
print("\nBoth services have graceful fallbacks and will work without AWS Bedrock.")
