"""
AWS Services - S3 and Textract Integration

This module provides cloud-based document storage and OCR capabilities:
- S3: File upload, download, and automatic cleanup
- Textract: Advanced OCR for PDF and image documents

Responsibilities:
- Upload files to S3 with unique keys
- Extract text using AWS Textract
- Delete files from S3 after processing
- Handle AWS service errors gracefully
"""

import os
from pathlib import Path
from typing import Optional, List, Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize AWS clients
textract = boto3.client('textract', region_name=os.getenv('AWS_REGION', 'us-east-1'))
s3 = boto3.client('s3', region_name=os.getenv('AWS_REGION', 'us-east-1'))

# S3 bucket configuration
BUCKET_NAME = os.getenv('S3_BUCKET_NAME', 'bima-bot-hackathon-2026')


class AWSServiceError(Exception):
    """Base exception for AWS service errors"""
    pass


def upload_file_to_s3(local_path: str, s3_key: str) -> str:
    """
    Upload a file to S3 bucket.
    
    Args:
        local_path: Absolute path to local file
        s3_key: S3 object key (path in bucket)
        
    Returns:
        S3 URI of uploaded file (s3://bucket/key)
        
    Raises:
        AWSServiceError: If upload fails
    """
    try:
        s3.upload_file(local_path, BUCKET_NAME, s3_key)
        s3_uri = f"s3://{BUCKET_NAME}/{s3_key}"
        print(f"✅ Uploaded {local_path} to {s3_uri}")
        return s3_uri
    
    except FileNotFoundError:
        raise AWSServiceError(f"Local file not found: {local_path}")
    except (ClientError, BotoCoreError) as e:
        raise AWSServiceError(f"Failed to upload to S3: {str(e)}")


def download_file_from_s3(s3_key: str, local_path: Optional[str] = None) -> str:
    """
    Download a file from S3 bucket.
    
    Args:
        s3_key: S3 object key
        local_path: Optional local save path (defaults to key's basename)
        
    Returns:
        Path to downloaded file
        
    Raises:
        AWSServiceError: If download fails
    """
    try:
        if local_path is None:
            local_path = s3_key.split('/')[-1]
        
        s3.download_file(BUCKET_NAME, s3_key, local_path)
        print(f"✅ Downloaded {s3_key} to {local_path}")
        return local_path
        
    except (ClientError, BotoCoreError) as e:
        raise AWSServiceError(f"Failed to download from S3: {str(e)}")


def delete_file_from_s3(s3_key: str) -> None:
    """
    Delete a file from S3 bucket.
    
    Args:
        s3_key: S3 object key to delete
        
    Raises:
        AWSServiceError: If deletion fails
    """
    try:
        s3.delete_object(Bucket=BUCKET_NAME, Key=s3_key)
        print(f"🗑️  Deleted {s3_key} from S3")
        
    except (ClientError, BotoCoreError) as e:
        raise AWSServiceError(f"Failed to delete from S3: {str(e)}")


def delete_multiple_files_from_s3(s3_keys: List[str]) -> None:
    """
    Delete multiple files from S3 bucket in a single request.
    
    Args:
        s3_keys: List of S3 object keys to delete
        
    Raises:
        AWSServiceError: If deletion fails
    """
    if not s3_keys:
        return
    
    try:
        objects = [{'Key': key} for key in s3_keys]
        s3.delete_objects(
            Bucket=BUCKET_NAME,
            Delete={'Objects': objects}
        )
        print(f"🗑️  Deleted {len(s3_keys)} files from S3")
        
    except (ClientError, BotoCoreError) as e:
        raise AWSServiceError(f"Failed to delete multiple files from S3: {str(e)}")


def list_s3_files(prefix: str = '') -> List[str]:
    """
    List files in the S3 bucket with optional prefix filter.
    
    Args:
        prefix: Optional prefix to filter results
        
    Returns:
        List of S3 object keys
        
    Raises:
        AWSServiceError: If listing fails
    """
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        if 'Contents' in response:
            return [obj['Key'] for obj in response['Contents']]
        return []
        
    except (ClientError, BotoCoreError) as e:
        raise AWSServiceError(f"Failed to list S3 files: {str(e)}")


def extract_text_with_textract(s3_key: str) -> str:
    """
    Extract text from a document in S3 using AWS Textract.
    
    This replaces pypdf OCR with cloud-based OCR that supports:
    - PDF documents (digital and scanned)
    - Images (JPEG, PNG)
    - Superior accuracy for scanned documents
    
    Args:
        s3_key: S3 object key of the document
        
    Returns:
        Extracted text from all pages/blocks
        
    Raises:
        AWSServiceError: If Textract processing fails
    """
    try:
        response = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': s3_key
                }
            }
        )
        
        # Extract LINE blocks (similar to pypdf's line-by-line extraction)
        lines = []
        for block in response.get('Blocks', []):
            if block['BlockType'] == 'LINE':
                lines.append(block.get('Text', ''))
        
        text = '\n'.join(lines)
        print(f"📄 Extracted {len(lines)} lines from {s3_key}")
        return text
        
    except (ClientError, BotoCoreError) as e:
        # Enhanced error handling to capture detailed AWS error info
        if isinstance(e, ClientError):
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            error_msg = e.response.get('Error', {}).get('Message', str(e))
            print(f"❌ Textract ClientError - Code: {error_code}, Message: {error_msg}")
            print(f"   Document: s3://{BUCKET_NAME}/{s3_key}")
            raise AWSServiceError(f"Textract error for {s3_key}: {error_code} - {error_msg}")
        else:
            print(f"❌ Textract BotoCoreError: {str(e)}")
            raise AWSServiceError(f"Textract failed to process {s3_key}: {str(e)}")


def extract_text_from_s3_file(s3_key: str) -> str:
    """
    Extract text from a file already in S3 using Textract.
    
    Tries synchronous API first, falls back to async API if needed.
    
    Args:
        s3_key: S3 object key of the document (e.g., 'audits/AUD-123/bill.pdf')
        
    Returns:
        Extracted text
        
    Raises:
        AWSServiceError: If extraction fails
    """
    try:
        # Try synchronous API first (faster for simple documents)
        return extract_text_with_textract(s3_key)
    except AWSServiceError as e:
        # If sync fails with UnsupportedDocument, try async API
        if "UnsupportedDocument" in str(e) or "unsupported document format" in str(e).lower():
            print(f"⚠️  Sync Textract failed, switching to async API for {s3_key}")
            return extract_text_with_async_textract(s3_key)
        else:
            # Re-raise other errors
            raise


def extract_text_with_async_textract(s3_key: str) -> str:
    """
    Extract text from a document in S3 using AWS Textract ASYNC API.
    
    This is the production-ready approach for complex/large PDFs that fail
    with the synchronous detect_document_text API.
    
    Uses start_document_text_detection + polling for job completion.
    
    Args:
        s3_key: S3 object key of the document
        
    Returns:
        Extracted text from all pages/blocks
        
    Raises:
        AWSServiceError: If Textract processing fails or times out
    """
    import time
    
    try:
        # Start async job
        print(f"🔄 Starting async Textract job for {s3_key}")
        response = textract.start_document_text_detection(
            DocumentLocation={
                'S3Object': {
                    'Bucket': BUCKET_NAME,
                    'Name': s3_key
                }
            }
        )
        
        job_id = response['JobId']
        print(f"📋 Job ID: {job_id}")
        
        # Poll for completion
        max_wait_time = 60  # seconds
        poll_interval = 2   # seconds
        elapsed_time = 0
        
        while elapsed_time < max_wait_time:
            print(f"⏳ Waiting for job completion... ({elapsed_time}s elapsed)")
            time.sleep(poll_interval)
            elapsed_time += poll_interval
            
            response = textract.get_document_text_detection(JobId=job_id)
            status = response['JobStatus']
            
            if status == 'SUCCEEDED':
                print(f"✅ Job completed in {elapsed_time} seconds")
                
                # Extract text from results
                lines = []
                
                # Get first page of results
                for block in response.get('Blocks', []):
                    if block['BlockType'] == 'LINE':
                        lines.append(block.get('Text', ''))
                
                # Handle pagination if there are more results
                next_token = response.get('NextToken')
                while next_token:
                    response = textract.get_document_text_detection(
                        JobId=job_id,
                        NextToken=next_token
                    )
                    for block in response.get('Blocks', []):
                        if block['BlockType'] == 'LINE':
                            lines.append(block.get('Text', ''))
                    next_token = response.get('NextToken')
                
                text = '\n'.join(lines)
                print(f"📄 Extracted {len(lines)} lines from {s3_key} (async)")
                return text
                
            elif status == 'FAILED':
                error_msg = response.get('StatusMessage', 'Unknown error')
                raise AWSServiceError(f"Async Textract job failed: {error_msg}")
            
            # Status is IN_PROGRESS, continue polling
        
        # Timeout reached
        raise AWSServiceError(f"Async Textract job timed out after {max_wait_time}s for {s3_key}")
        
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        error_msg = e.response.get('Error', {}).get('Message', str(e))
        print(f"❌ Async Textract ClientError - Code: {error_code}, Message: {error_msg}")
        raise AWSServiceError(f"Async Textract error for {s3_key}: {error_code} - {error_msg}")
    except BotoCoreError as e:
        print(f"❌ Async Textract BotoCoreError: {str(e)}")
        raise AWSServiceError(f"Async Textract failed to process {s3_key}: {str(e)}")


def upload_and_extract_text(local_path: str, s3_key: str) -> str:
    """
    Upload a local file to S3 and extract text using Textract.
    
    Designed for multi-user scenarios - caller specifies unique S3 key.
    Does NOT delete the file from S3 after extraction (caller's responsibility).
    
    Args:
        local_path: Path to local PDF or image file
        s3_key: Unique S3 key to upload to (e.g., 'audits/AUD-123/bill.pdf')
        
    Returns:
        Extracted text
        
    Raises:
        AWSServiceError: If upload or extraction fails
        
    Example:
        >>> text = upload_and_extract_text(
        ...     '/path/to/bill.pdf',
        ...     'audits/AUD-ABC123/bill.pdf'
        ... )
    """
    # Upload to caller-specified S3 key (no temp folder!)
    upload_file_to_s3(local_path, s3_key)
    
    # Extract text from the uploaded file
    return extract_text_with_textract(s3_key)
