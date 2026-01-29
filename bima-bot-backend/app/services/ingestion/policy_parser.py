"""
Policy Parser Service - Phase 4
Responsible for converting RAW TEXT -> Structured PolicyData object.
Uses AI (Simulated) to understand context.
"""

from typing import Optional, List
from app.models.policy import PolicyData, PolicyClause, SubLimit

def parse_policy_from_text(raw_text: str) -> Optional[PolicyData]:
    """
    Simulates AI extracting policy details from raw OCR text.
    Strictly follows schema.
    """
    if "HDFC ERGO" not in raw_text:
        return None
        
    # AI Logic: Maps raw text features to specific schema fields.
    
    return PolicyData(
        policy_id="POL-2025-XYZ123",
        policy_holder_name="John Doe",
        insurer_name="HDFC ERGO Health Insurance",
        coverage_amount=500000.0,
        
        # AI Normalization: "Diabtes" typo -> "Diabetes"
        ped_list=["Diabetes", "Hypertension", "Asthma"],
        
        general_waiting_period_months=30,
        ped_waiting_period_months=48,
        
        room_limit_type="amount",
        room_limit_value="3000",
        
        copay_percentage=10.0,
        
        sub_limits=[
            SubLimit(
                category="ICU",
                limit_amount=50000.0
            )
        ],
        
        clauses=[
            PolicyClause(
                clause_id="extracted-1",
                clause_type="PED",
                text="PED covered after 48 months",
                page_number=1
            ),
            PolicyClause(
                clause_id="extracted-2",
                clause_type="ROOM_RENT",
                text="Room Rent: Capped at 3000 / day",
                page_number=1
            )
        ]
    )
