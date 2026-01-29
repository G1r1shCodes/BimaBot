"""
Audit API Routes - Phase 4.1 Implementation

Phase 4.1 adds real PDF document upload and processing.

Routes delegate all logic to the service layer.
No business logic should exist in routes.
"""

import os
from pathlib import Path
from fastapi import APIRouter, HTTPException, UploadFile, File

from app.models.audit import AuditResult, AuditStatus
from app.services import audit_service
from app.services.audit_service import AUDIT_STORE, process_audit_pipeline
from app.services.aws_service import upload_file_to_s3, delete_multiple_files_from_s3, AWSServiceError


router = APIRouter()

# Upload configuration
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/start")
def start_audit():
    """
    Start a new audit session.
    
    Phase 4.1: Creates session with CREATED status
    Returns: audit_id and initial status
    """
    return audit_service.start_audit()


@router.post("/{audit_id}/upload")
async def upload_documents(
    audit_id: str,
    bill: UploadFile = File(..., description="Hospital bill PDF"),
    policy: UploadFile = File(..., description="Insurance policy PDF")
):
    """
    Upload hospital bill and insurance policy PDFs.
    
    Rules:
    - Only allowed when audit status == "created"
    - Files saved to disk immediately
    - Paths stored in audit session
    - No processing happens here (deferred to /complete)
    """
    
    # 1. Validate audit exists and status
    if audit_id not in AUDIT_STORE:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    audit = AUDIT_STORE[audit_id]
    if audit["status"] != AuditStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Upload not allowed. Audit status is '{audit['status']}', expected 'created'"
        )
    
    # 2. Validate file types
    bill_ext = Path(bill.filename).suffix.lower() if bill.filename else ""
    policy_ext = Path(policy.filename).suffix.lower() if policy.filename else ""
    
    if bill_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Bill must be PDF, got {bill_ext}")
    if policy_ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail=f"Policy must be PDF, got {policy_ext}")
    
    # 3. Validate file sizes
    bill_content = await bill.read()
    policy_content = await policy.read()
    
    if len(bill_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Bill file too large (max 10MB)")
    if len(policy_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Policy file too large (max 10MB)")
    
    # 4. Create upload directory for this audit
    audit_upload_dir = UPLOAD_DIR / audit_id
    audit_upload_dir.mkdir(parents=True, exist_ok=True)
    
    # 5. Save files to disk (for local processing)
    bill_path = audit_upload_dir / "bill.pdf"
    policy_path = audit_upload_dir / "policy.pdf"
    
    bill_path.write_bytes(bill_content)
    policy_path.write_bytes(policy_content)
    
    # 6. Upload files to S3 for cloud processing
    try:
        bill_s3_key = f"audits/{audit_id}/bill.pdf"
        policy_s3_key = f"audits/{audit_id}/policy.pdf"
        
        upload_file_to_s3(str(bill_path.absolute()), bill_s3_key)
        upload_file_to_s3(str(policy_path.absolute()), policy_s3_key)
        
        # Store both local and S3 paths
        audit["bill_path"] = str(bill_path.absolute())
        audit["policy_path"] = str(policy_path.absolute())
        audit["bill_s3_key"] = bill_s3_key
        audit["policy_s3_key"] = policy_s3_key
        
    except AWSServiceError as e:
        # Cleanup local files if S3 upload fails
        bill_path.unlink(missing_ok=True)
        policy_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to upload files to S3: {str(e)}"
        )
    
    # 7. Return success (status remains "created")
    return {
        "message": "Files uploaded successfully",
        "bill_size_kb": round(len(bill_content) / 1024, 2),
        "policy_size_kb": round(len(policy_content) / 1024, 2),
        "status": audit["status"]
    }


@router.get("/{audit_id}/status")
def get_audit_status(audit_id: str):
    """
    Get current audit processing status.
    
    Phase 4.1: Returns status from in-memory store
    """
    status = audit_service.get_audit_status(audit_id)
    
    if status is None:
        raise HTTPException(status_code=404, detail="Audit ID not found")
    
    return status


@router.get("/{audit_id}/result", response_model=AuditResult)
def get_audit_result(audit_id: str):
    """
    Get completed audit result.
    
    Phase 4.1: Returns AuditResult if completed
    Returns 404 if audit not found
    Returns 400 if audit still processing
    """
    result = audit_service.get_audit_result(audit_id)
    
    if result is None:
        # Check if audit exists at all
        status = audit_service.get_audit_status(audit_id)
        if status is None:
            raise HTTPException(status_code=404, detail="Audit ID not found")
        
        # Audit exists but not completed yet
        raise HTTPException(
            status_code=400,
            detail="Audit still in progress",
        )
    
    return result


@router.post("/{audit_id}/complete")
def complete_audit(audit_id: str):
    """
    Trigger audit processing pipeline.
    
    Phase 4.1: Validates files exist, processes PDFs, runs rules.
    
    Rules:
    - Only allowed when status == "created"
    - Requires bill_path and policy_path to be set
    - Sets status = "processing" immediately
    - Runs OCR → Parse → Validate → Rules
    - Sets status = "completed" or "failed"
    """
    
    if audit_id not in AUDIT_STORE:
        raise HTTPException(status_code=404, detail="Audit not found")
    
    audit = AUDIT_STORE[audit_id]
    
    # Validate status
    if audit["status"] != AuditStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot complete. Status is '{audit['status']}', expected 'created'"
        )
    
    # Validate files uploaded
    if not audit.get("bill_path") or not audit.get("policy_path"):
        raise HTTPException(
            status_code=400,
            detail="Files not uploaded. Call /upload first"
        )
    
    # Set processing status
    audit["status"] = AuditStatus.PROCESSING
    
    try:
        # Run pipeline with S3 keys for multi-user safe OCR processing
        result = process_audit_pipeline(
            audit_id=audit_id,
            bill_path=audit["bill_path"],
            policy_path=audit["policy_path"],
            bill_s3_key=audit.get("bill_s3_key"),
            policy_s3_key=audit.get("policy_s3_key")
        )
        
        audit["result"] = result
        audit["status"] = AuditStatus.COMPLETED
        
        # Cleanup: Delete entire audit folder from S3
        # Multi-user safe: each audit has its own folder (audits/{audit_id}/)
        try:
            s3_keys_to_delete = []
            
            # Only clean up files we actually uploaded
            if audit.get("bill_s3_key"):
                s3_keys_to_delete.append(audit["bill_s3_key"])
            if audit.get("policy_s3_key"):
                s3_keys_to_delete.append(audit["policy_s3_key"])
            
            # No temp folder cleanup - we don't use temp folders anymore!
            
            if s3_keys_to_delete:
                delete_multiple_files_from_s3(s3_keys_to_delete)
                print(f"✅ Cleaned up S3 files for audit {audit_id}: {len(s3_keys_to_delete)} files deleted")
        
        except AWSServiceError as cleanup_error:
            # Log cleanup error but don't fail the audit
            print(f"⚠️ S3 cleanup failed for audit {audit_id}: {cleanup_error}")
        
        return {"message": "Audit completed successfully"}
        
    except Exception as e:
        audit["status"] = AuditStatus.FAILED
        audit["error"] = str(e)
        
        # Attempt cleanup even on failure
        try:
            s3_keys_to_delete = []
            if audit.get("bill_s3_key"):
                s3_keys_to_delete.append(audit["bill_s3_key"])
            if audit.get("policy_s3_key"):
                s3_keys_to_delete.append(audit["policy_s3_key"])
            if s3_keys_to_delete:
                delete_multiple_files_from_s3(s3_keys_to_delete)
                print(f"🗑️ Cleaned up S3 after failure for audit {audit_id}")
        except:
            pass  # Ignore cleanup errors when audit already failed
        
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

