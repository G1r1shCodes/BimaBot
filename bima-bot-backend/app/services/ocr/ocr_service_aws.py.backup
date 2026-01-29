"""
OCR Service - Phase 4.2 (AWS Textract Integration)

DUMB LAYER: Extracts raw text only. No validation. No interpretation.

Responsibilities:
- Read PDF/image files (now via AWS Textract)
- Extract text from all pages
- Return raw text string (even if empty)
- Raise errors only on processing failures

NOT responsible for:
- Validating document content
- Detecting scanned vs digital PDFs
- Parsing or structuring text
- Business logic decisions

Changes from Phase 4.1:
- Replaced pypdf with AWS Textract for superior OCR
- Files uploaded to S3 for processing (unique folder per audit)
- Supports both digital and scanned PDFs
- Multi-user safe: each audit has its own S3 folder
"""

from pathlib import Path
from app.services.aws_service import extract_text_from_s3_file, AWSServiceError


def extract_text_from_document(file_path: str, s3_key: str) -> str:
    """
    Extract raw text from PDF or image document using AWS Textract.
    
    This is a DUMB LAYER by design:
    - Returns text as-is, no validation
    - Empty text is valid (caller decides what to do)
    - No interpretation of content quality
    - Single responsibility: read document → return text
    
    Args:
        file_path: Absolute path to PDF or image file (for local access)
        s3_key: S3 key where this file is stored (e.g., 'audits/AUD-123/bill.pdf')
        
    Returns:
        Raw text extracted from all pages (may be empty string)
        
    Raises:
        RuntimeError: If file cannot be processed
        
    Examples:
        >>> text = extract_text_from_document(
        ...     "/path/to/bill.pdf",
        ...     "audits/AUD-ABC123/bill.pdf"
        ... )
        >>> # text may be empty if document has no text — that's fine, ingestion handles it
    """
    try:
        # Use AWS Textract to extract from S3
        # File should already be uploaded to S3 by the audit route
        # S3 cleanup is handled by the audit service after completion
        text = extract_text_from_s3_file(s3_key)
        
        # Return as-is, even if empty
        # Validation is the ingestion layer's job, not OCR's
        return text
        
    except AWSServiceError as e:
        raise RuntimeError(f"AWS Textract failed for {s3_key}: {str(e)}")
    except FileNotFoundError:
        raise RuntimeError(f"Document file not found: {file_path}")
    except Exception as e:
        raise RuntimeError(f"Failed to process document {file_path}: {str(e)}")

