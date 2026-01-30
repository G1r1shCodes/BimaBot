
import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.getcwd())

from app.services.audit_service import process_audit_pipeline
from app.models.history import AuditFlag, FlagSeverity, FlagType

class VerifyRnGEnrichment(unittest.TestCase):
    @patch('app.services.audit_service.get_rag_explanation')
    @patch('app.services.audit_service.extract_text_from_document')
    @patch('app.services.audit_service.structure_and_categorize')
    @patch('app.services.audit_service.run_audit_rules')
    @patch('app.services.audit_service.generate_dispute_letter')
    @patch('app.services.audit_service.delete_multiple_files_from_s3') # Mock cleanup
    def test_rag_enrichment_logic(self, mock_delete, mock_letter, mock_rules, mock_structure, mock_ocr, mock_rag):
        
        print("\n=== STARTING VERIFICATION: RAG Enrichment Logic ===\n")
        
        # 1. Setup Mocks
        # OCR returns dummy text
        mock_ocr.return_value = "Run Audit on Sample Data"
        
        # Structure returns dummy objects
        mock_structure.return_value = {
            "bill": {"bill_id": "TEST", "charges": [], "stated_total_amount": 1000},
            "policy": {"policy_id": "TEST", "coverage_amount": 500000}
        }
        
        # Rule Engine returns a flag that needs explanation
        test_flag = AuditFlag(
            flag_type=FlagType.MISC,
            severity=FlagSeverity.ERROR,
            reason="Policy Annexure A (List IV) - Admin",
            policy_clause="Annexure A List IV"
        )
        mock_rules.return_value = [test_flag]
        
        # RAG Service returns a mock explanation
        mock_rag.return_value = "According to IRDAI, Admin charges are non-payable."
        
        # 2. Run Pipeline
        result = process_audit_pipeline("AUD-TEST", "bill.pdf", "policy.pdf")
        
        # 3. Verify RAG was called
        mock_rag.assert_called()
        print("✅ RAG Service was called.")
        
        # 4. Verify Flag Reason was enriched
        enriched_flag = result.flags[0]
        print(f"Original Reason: Policy Annexure A (List IV) - Admin")
        print(f"Enriched Reason: {enriched_flag.reason}")
        
        self.assertIn("According to IRDAI", enriched_flag.reason)
        self.assertIn("Policy Annexure A (List IV) - Admin", enriched_flag.reason)
        print("✅ Flag reason successfully enriched with AI explanation.")

if __name__ == "__main__":
    unittest.main()
