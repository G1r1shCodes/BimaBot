// TypeScript type definitions for BimaBot Backend API

// Audit Status Types
export type AuditStatus = 'created' | 'processing' | 'completed' | 'failed';

// Flag Types
export type FlagType =
    | 'CONSUMABLES'
    | 'ROOM_RENT_EXCESS'
    | 'NON_MEDICAL'
    | 'PRE_EXISTING'
    | 'WAITING_PERIOD'
    | 'UNCOVERED_PROCEDURE'
    | 'POLICY_LIMIT_EXCEEDED'
    | 'REGISTRATION_FEE'
    | 'MISC';

export type FlagSeverity = 'INFO' | 'WARNING' | 'ERROR';

// Audit Flag Interface
export interface AuditFlag {
    flag_type: FlagType;
    severity: FlagSeverity;
    charge_category?: string;
    charge_description?: string;
    amount_affected?: number;
    reason: string;
    regulatory_reference?: string;
}

// Hospital Bill Interface
export interface HospitalBill {
    hospital_name?: string;
    patient_name?: string;
    bill_number?: string;
    admission_date?: string;
    discharge_date?: string;
    total_amount?: number;
    charges?: Array<{
        line_item_id: string;
        label?: string;
        description?: string;
        amount: number;
        category?: string;
    }>;
}

// Policy Data Interface
export interface PolicyData {
    policy_number?: string;
    insurer_name?: string;
    policy_holder_name?: string;
    sum_insured?: number;
    room_rent_limit?: number;
    waiting_period_months?: number;
    coverage_details?: Record<string, any>;
}

// Audit Result Interface (Main Response)
export interface AuditResult {
    audit_id: string;
    status: AuditStatus;
    bill: HospitalBill;
    policy: PolicyData;
    flags: AuditFlag[];
    total_billed: number;
    amount_under_review: number;
    fully_covered_amount: number;
    dispute_letter_content: string;
    created_at?: string;
    completed_at?: string;
}

// API Response Types
export interface StartAuditResponse {
    audit_id: string;
    status: AuditStatus;
    message: string;
}

export interface UploadDocumentsResponse {
    message: string;
    bill_uploaded: boolean;
    policy_uploaded: boolean;
}

export interface AuditStatusResponse {
    audit_id: string;
    status: AuditStatus;
}

export interface CompleteAuditResponse {
    message: string;
}
