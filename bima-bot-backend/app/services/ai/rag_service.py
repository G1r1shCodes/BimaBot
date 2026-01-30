"""
RAG Retrieval Service - AWS Bedrock Knowledge Base Integration

Retrieves IRDAI regulations and policy clauses for audit explanations.

This implements the reference backend's RAG pattern:
- Uses bedrock-agent-runtime client
- retrieve_and_generate API
- KB_ID + MODEL_ARN configuration
- RAG provides explanations ONLY, NOT decisions

Architecture Principle:
RAG retrieves citations and regulations for reference.
Rules make ALL decisions autonomously.
"""

import boto3
import os
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# Bedrock Knowledge Base configuration
REGION = os.getenv('AWS_REGION', 'us-east-1')
KB_ID = os.getenv('BEDROCK_KB_ID', '')  # Set in .env file
MODEL_ARN = os.getenv('BEDROCK_MODEL_ARN', 'arn:aws:bedrock:us-east-1::foundation-model/amazon.nova-pro-v1:0')

# Initialize bedrock agent runtime client
agent = boto3.client('bedrock-agent-runtime', region_name=REGION)


def get_rag_explanation(query: str) -> Optional[str]:
    """
    Retrieve explanation from knowledge base for a given query.
    
    Uses AWS Bedrock Knowledge Base to find relevant IRDAI regulations
    and policy clauses that explain why certain items are denied/approved.
    
    Args:
        query: Question about insurance rules (e.g., "Why are consumables excluded?")
        
    Returns:
        Retrieved explanation with citations, or None if retrieval fails
        
    Example:
        >>> explanation = get_rag_explanation("Why are consumables not covered?")
        >>> # Returns: "According to IRDAI Circular 123, consumables such as..."
    """
    
    if not KB_ID:
        print("⚠️  BEDROCK_KB_ID not configured, skipping RAG retrieval")
        return None
    
    try:
        response = agent.retrieve_and_generate(
            input={'text': query},
            retrieveAndGenerateConfiguration={
                'type': 'KNOWLEDGE_BASE',
                'knowledgeBaseConfiguration': {
                    'knowledgeBaseId': KB_ID,
                    'modelArn': MODEL_ARN
                }
            }
        )
        
        explanation = response['output']['text']
        print(f"✅ RAG retrieved explanation for: {query[:50]}...")
        return explanation
        
    except Exception as e:
        print(f"❌ RAG retrieval failed for query '{query}': {e}")
        return None


def explain_consumables_exclusion() -> str:
    """Get explanation for why consumables are typically excluded."""
    explanation = get_rag_explanation(
        "Why are medical consumables like gloves, syringes, and masks excluded from health insurance coverage? Quote the specific IRDAI regulation."
    )
    return explanation or "Consumables are typically excluded per policy terms."


def explain_room_rent_limits() -> str:
    """Get explanation for room rent limits and proportionate deductions."""
    explanation = get_rag_explanation(
        "What are the IRDAI guidelines for room rent limits and proportionate deductions in health insurance?"
    )
    return explanation or "Room rent limits are defined in the policy terms."


def explain_ped_waiting_period() -> str:
    """Get explanation for PED waiting periods."""
    explanation = get_rag_explanation(
        "What is the waiting period for pre-existing diseases (PED) according to IRDAI regulations?"
    )
    return explanation or "PED waiting periods are typically 2-4 years as per policy."


def explain_sub_limits() -> str:
    """Get explanation for disease-specific sub-limits."""
    explanation = get_rag_explanation(
        "What are sub-limits in health insurance and when do they apply according to IRDAI guidelines?"
    )
    return explanation or "Sub-limits apply to specific diseases as defined in the policy schedule."


def explain_copayment() -> str:
    """Get explanation for co-payment clauses."""
    explanation = get_rag_explanation(
        "What is co-payment in health insurance and what are the IRDAI regulations around it?"
    )
    return explanation or "Co-payment is the percentage of claim amount borne by the insured."
