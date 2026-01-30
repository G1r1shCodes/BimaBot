
import sys
import os
import unittest

# Add project root to path
sys.path.append(os.getcwd())

from app.services.ingestion.bill_parser import parse_bill_from_structured
from app.models.policy import PolicyData, SubLimit, LimitType
from app.services.rule_engine import run_audit_rules
from app.models.bill import ChargeCategory

class VerifyAuditFlow(unittest.TestCase):
    def test_ortho_flow(self):
        print("\n=== STARTING VERIFICATION: Ortho Bill Audit Flow ===\n")
        
        # 1. Simulate AI Structured Output (what comes from OCR + LLM)
        # Note: We simulate the AI being "dumb" about categories to test our Helper Logic
        mock_ai_output = {
            "bill_id": "BILL-ORTHO-VERIFY",
            "hospital_name": "Apollo Hospitals",
            "patient_name": "John Doe",
            "diagnosis": ["Knee Replacement"],
            "charges": [
                {"description": "Room Rent (Private Ward)", "category": "ROOM_RENT", "amount": 20000},
                {"description": "Surgery Charges (Knee Replacement)", "category": "SURGERY", "amount": 60000},
                {"description": "Knee Implant (Cobalt Chrome)", "category": "SURGERY", "amount": 110000},
                {"description": "Pharmacy / Medicines", "category": "PHARMACY", "amount": 22500},
                # AI often misclassifies these:
                {"description": "OT Consumables", "category": "OTHER", "amount": 8000}, 
                {"description": "Admission / Admin Charges", "category": "OTHER", "amount": 1000},
                {"description": "Bio-Medical Waste Disposal", "category": "CONSUMABLES", "amount": 750}, 
                {"description": "Nursing & Physio Charges", "category": "PROFESSIONAL_FEES", "amount": 9000}
            ],
            "stated_total_amount": 281250,
            "currency": "INR"
        }
        print("1. [INPUT] Simulated AI Output received.")
        
        # 2. Run Parser (with Hybrid Classification Logic)
        bill = parse_bill_from_structured(mock_ai_output)
        self.assertIsNotNone(bill, "Bill parsing failed")
        print("2. [PARSER] Bill parsed successfully.")
        
        # Verify Overrides happened
        ot_con = next(c for c in bill.charges if "OT Consumables" in c.label)
        print(f"   - 'OT Consumables' categorized as: {ot_con.category} (Expected: consumables)")
        self.assertEqual(ot_con.category, ChargeCategory.CONSUMABLES)

        waste = next(c for c in bill.charges if "Waste" in c.label)
        print(f"   - 'Bio-Medical Waste' categorized as: {waste.category} (Expected: misc)")
        self.assertEqual(waste.category, ChargeCategory.MISC)

        admin = next(c for c in bill.charges if "Admin" in c.label)
        print(f"   - 'Admin Charges' categorized as: {admin.category} (Expected: misc)")
        self.assertEqual(admin.category, ChargeCategory.MISC)
        
        # 3. Define Policy (Reliance Style)
        policy = PolicyData(
            policy_id="POL-REL-VERIFY",
            policy_holder_name="John Doe",
            insurer_name="Reliance",
            coverage_amount=500000.0,
            ped_list=[],
            sub_limits=[
                SubLimit(category="Consumables", limit_amount=0.0), # Excluded
                SubLimit(category="Room Rent", limit_amount=3000.0) # Cap at 3k
            ]
        )
        print("3. [POLICY] Policy loaded (Consumables excluded, Room Rent capped).")
        
        # 4. Run Rule Engine
        print("4. [RULES] Executing Rule Engine...")
        flags = run_audit_rules(bill, policy)
        
        print("\n=== AUDIT RESULTS ===")
        # Check specific flags
        found_consumables = False
        found_admin = False
        found_waste = False
        
        for f in flags:
            print(f"🚩 FLAG: {f.flag_type.name} | Severity: {f.severity.name}")
            print(f"   Reason: {f.reason}")
            
            if "Annexure A (List III)" in f.reason:
                found_consumables = True
            if "Annexure A (List IV)" in f.reason:
                found_admin = True
            if "Annexure A (List I)" in f.reason:
                found_waste = True
                
        self.assertTrue(found_consumables, "Missing Flag: OT Consumables (List III)")
        self.assertTrue(found_admin, "Missing Flag: Admin Charges (List IV)")
        self.assertTrue(found_waste, "Missing Flag: Waste Disposal (List I)")
        
        print("\n✅ VERIFICATION SUCCESS: All expected flags raised.")

if __name__ == "__main__":
    unittest.main()
