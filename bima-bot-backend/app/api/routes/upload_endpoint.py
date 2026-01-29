"""
File Upload Endpoint - Phase 4.1

New endpoint to accept hospital bill and insurance policy PDFs.

Rules enforced:
- Only allowed when audit status == "created"
- Files saved to disk immediately  
- Paths stored in audit session (not objects)
- No processing happens here (deferred to /complete)
"""

import os
import shutil
from pathlib import Path
from fastapi import UploadFile, File, HTTPException

from app.api.routes.audit import router
from app.models.audit import AuditStatus
from app.services.audit_service import AUDIT_STORE

# Configuration
UPLOAD_DIR = Path("uploads")
ALLOWED_EXTENSIONS = {".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


@router.post("/audit/{audit_id}/upload")
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
    
    Returns:
        Success message with file sizes
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
    bill_ext = Path(bill.filename).suffix.lower()
    policy_ext = Path(policy.filename).suffix.lower()
    
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
    
    # 5. Save files to disk
    bill_path = audit_upload_dir / "bill.pdf"
    policy_path = audit_upload_dir / "policy.pdf"
    
    bill_path.write_bytes(bill_content)
    policy_path.write_bytes(policy_content)
    
    # 6. Store PATHS in audit session (not file objects!)
    audit["bill_path"] = str(bill_path.absolute())
    audit["policy_path"] = str(policy_path.absolute())
    
    # 7. Return success (status remains "created")
    return {
        "message": "Files uploaded successfully",
        "bill_size_kb": round(len(bill_content) / 1024, 2),
        "policy_size_kb": round(len(policy_content) / 1024, 2),
        "status": audit["status"]
    }
