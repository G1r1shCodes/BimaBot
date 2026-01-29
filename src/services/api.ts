// API Service for BimaBot Backend Integration
// Base URL for the backend API
const API_BASE_URL = 'http://127.0.0.1:8000';

import type {
    StartAuditResponse,
    UploadDocumentsResponse,
    AuditStatusResponse,
    AuditResult
} from '@/types/types';

/**
 * Start a new audit session
 * POST /audit/start
 */
export async function startAudit(): Promise<StartAuditResponse> {
    const response = await fetch(`${API_BASE_URL}/audit/start`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        throw new Error(`Failed to start audit: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Upload hospital bill and insurance policy PDFs
 * POST /audit/{audit_id}/upload
 */
export async function uploadDocuments(
    auditId: string,
    billFile: File,
    policyFile: File
): Promise<UploadDocumentsResponse> {
    const formData = new FormData();
    formData.append('bill', billFile);
    formData.append('policy', policyFile);

    const response = await fetch(`${API_BASE_URL}/audit/${auditId}/upload`, {
        method: 'POST',
        body: formData,
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to upload documents: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Trigger the audit processing pipeline
 * POST /audit/{audit_id}/complete
 */
export async function triggerProcessing(auditId: string): Promise<{ message: string }> {
    const response = await fetch(`${API_BASE_URL}/audit/${auditId}/complete`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to trigger processing: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get the current status of an audit
 * GET /audit/{audit_id}/status
 */
export async function getAuditStatus(auditId: string): Promise<AuditStatusResponse> {
    const response = await fetch(`${API_BASE_URL}/audit/${auditId}/status`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Failed to get audit status: ${response.statusText}`);
    }

    return response.json();
}

/**
 * Get the final audit result
 * GET /audit/{audit_id}/result
 */
export async function getAuditResult(auditId: string): Promise<AuditResult> {
    const response = await fetch(`${API_BASE_URL}/audit/${auditId}/result`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));

        if (response.status === 404) {
            throw new Error('Audit not found or not yet completed');
        }

        throw new Error(errorData.detail || `Failed to get audit result: ${response.statusText}`);
    }

    return response.json();
}
