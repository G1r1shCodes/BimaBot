import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Add project root to path
sys.path.append(os.getcwd())

from app.services.audit_service import process_audit_pipeline
from app.models.audit import AuditFlag
from app.models.bill import HospitalBill

class VerifyNovaFlow(unittest.TestCase):
    
    @patch('app.services.audit_service.extract_text_from_document')
    @patch('app.services.ai.structuring_service.bedrock')
    @patch('app.services.ai.rag_service.agent')
    @patch('app.services.reporting.letter_generator.bedrock')
    @patch('app.services.aws_service.delete_multiple_files_from_s3') # Mock cleanup
    def test_nova_pipeline(self, mock_delete, mock_letter_bedrock, mock_rag_agent, mock_struct_bedrock, mock_ocr):
        
        print("\n=== STARTING VERIFICATION: Nova AI Pipeline ===\n")
        
        # 1. Mock OCR
        mock_ocr.return_value = "Sample Bill Text with enough characters to pass the validation check which requires at least 50 characters."
        
        # 2. Mock Structuring (Nova Lite)
        # Mock response structure for converse API
        mock_struct_response = {
            'output': {
                'message': {
                    'content': [{'text': json.dumps({
                        "items": [
                            { "description": "Gloves", "amount": 500, "category": "CONSUMABLES" },
                            { "description": "Consultation", "amount": 1000, "category": "DOCTOR_FEES" }
                        ],
                        "total_claimed": 1500
                    })}]
                }
            }
        }
        mock_struct_bedrock.converse.return_value = mock_struct_response
        
        # 3. Mock Audit (Nova Pro + RAG)
        # Mock response structure for retrieve_and_generate API
        audit_json = {
            "audit_summary": {
                "total_bill_amount": "1500",
                "charges_reviewed": 2,
                "amount_requiring_review": "500",
                "status": "Potential Policy Discrepancies"
            },
            "structured_bill": {
                "items": [
                    {
                        "description": "Gloves",
                        "category": "consumables",
                        "amount": 500,
                        "status": "May Not Comply",
                        "reference": "IRDAI Non-Payable"
                    },
                    {
                        "description": "Consultation",
                        "category": "professional_fees",
                        "amount": 1000,
                        "status": "Covered",
                        "reference": "Policy Section 3"
                    }
                ]
            },
            "explanations": [
                {
                    "title": "Gloves",
                    "text": "Gloves are non-payable items."
                }
            ]
        }
        mock_rag_agent.retrieve_and_generate.return_value = {
            'output': {'text': json.dumps(audit_json)}
        }
        
        # 4. Mock Letter (Nova Pro)
        mock_letter_response = {
            'output': {
                'message': {
                    'content': [{'text': "Dear User, We dispute the gloves."}]
                }
            }
        }
        mock_letter_bedrock.converse.return_value = mock_letter_response
        
        # 5. Run Pipeline
        result = process_audit_pipeline("AUD-TEST", "bill.pdf", "policy.pdf")
        
        # 6. Verify Results
        print("✅ Pipeline finished execution.")
        
        # Check generated object
        self.assertIsInstance(result.bill, HospitalBill)
        print(f"✅ Generated Bill object with {len(result.bill.charges)} charges.")
        
        # Check Flags
        flags = result.flags
        print(f"✅ Generated {len(flags)} flags.")
        for f in flags:
            print(f"   Flag: Type={f.flag_type}, Sev={f.severity}, Amt={f.amount_affected}, Reason={f.reason}")
        
        warning_flag = next((f for f in flags if f.amount_affected == 500), None)
        self.assertIsNotNone(warning_flag)
        print(f"   Found expected flag for Gloves: {warning_flag.severity}")
        
        # Check RAG Enrichment in Reason
        print(f"   Flag Reason: {warning_flag.reason}")
        self.assertIn("AI Analysis", warning_flag.reason)
        print("✅ Flag reason successfully enriched with AI explanation from 'explanations' list.")
        
        # Check Stats
        self.assertEqual(result.amount_under_review, 500)
        self.assertEqual(result.fully_covered_amount, 1000)
        print(f"✅ Stats: Review={result.amount_under_review}, Covered={result.fully_covered_amount}")
        
        # Check Letter
        self.assertEqual(result.dispute_letter_content, "Dear User, We dispute the gloves.")
        print("✅ Dispute letter content mapped correctly.")

if __name__ == "__main__":
    unittest.main()
