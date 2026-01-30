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


def parse_policy_from_structured(structured_data: dict) -> Optional[PolicyData]:
    """
    Convert AI-structured policy dictionary to PolicyData object.
    
    This replaces the mock parser above - validates AI-structured data
    and converts it to the proper Pydantic model.
    
    Args:
        structured_data: Dictionary from AI structuring service
        
    Returns:
        PolicyData object or None if validation fails
    """
    try:
        return PolicyData(
            policy_id=structured_data.get("policy_id") or "UNKNOWN",
            policy_holder_name=structured_data.get("policy_holder_name") or "Unknown",
            insurer_name=structured_data.get("insurer_name") or "Unknown Insurer",
            coverage_amount=float(structured_data.get("coverage_amount", 0)),
            ped_list=structured_data.get("ped_list", []),
            general_waiting_period_months=structured_data.get("general_waiting_period_months"),
            ped_waiting_period_months=structured_data.get("ped_waiting_period_months") or 48,
            room_limit_type=structured_data.get("room_limit_type"),
            room_limit_value=structured_data.get("room_limit_value"),
            copay_percentage=structured_data.get("copay_percentage"),
            sub_limits=[],  # Simplified - would parse from structured_data if needed
            clauses=[]  # Simplified - would parse from structured_data if needed
        )
        
    except (KeyError, ValueError, TypeError) as e:
        print(f"❌ Failed to convert structured policy data: {e}")
        return None

