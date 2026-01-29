import { useState } from 'react';
import { Upload, FileText, CheckCircle2 } from 'lucide-react';
import { startAudit, uploadDocuments } from '@/services/api';

interface AuditBillPageProps {
  onStartAudit: (billFile: File | null, policyFile: File | null, isSample: boolean, auditId?: string) => void;
}

export default function AuditBillPage({ onStartAudit }: AuditBillPageProps) {
  const [billFile, setBillFile] = useState<File | null>(null);
  const [policyFile, setPolicyFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleBillUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setBillFile(e.target.files[0]);
      setError(null);
    }
  };

  const handlePolicyUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setPolicyFile(e.target.files[0]);
      setError(null);
    }
  };

  const handleStartAudit = async () => {
    if (!billFile || !policyFile) {
      setError('Please upload both files');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      // Step 1: Start audit session
      const { audit_id } = await startAudit();

      // Step 2: Upload documents
      await uploadDocuments(audit_id, billFile, policyFile);

      // Step 3: Proceed to processing with audit ID
      onStartAudit(billFile, policyFile, false, audit_id);
    } catch (err) {
      console.error('Failed to start audit:', err);
      setError(err instanceof Error ? err.message : 'Failed to start audit. Please try again.');
      setIsUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl mb-4 text-gray-900">Upload Your Documents</h1>
          <p className="text-xl text-gray-600">
            Upload your final hospital bill and insurance policy.
            Photos or PDFs both work.
          </p>
        </div>

        {/* Upload Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
          {/* Hospital Bill Upload */}
          <div className="bg-white rounded-xl border-2 border-gray-200 p-8">
            <div className="text-center">
              <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-[#1E3A8A]" />
              </div>
              <h3 className="text-xl mb-2 text-gray-900">Hospital Bill</h3>
              <p className="text-sm text-gray-600 mb-4">
                Final bill provided at discharge
              </p>

              {billFile ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-2 justify-center text-green-700">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="text-sm truncate">{billFile.name}</span>
                  </div>
                </div>
              ) : (
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">
                    Click below to upload
                  </p>
                </div>
              )}

              <label className="block">
                <input
                  type="file"
                  accept=".pdf,.jpg,.jpeg,.png"
                  onChange={handleBillUpload}
                  className="hidden"
                />
                <span className="bg-[#1E3A8A] hover:bg-[#1E40AF] text-white px-6 py-3 rounded-lg cursor-pointer inline-block transition-colors">
                  {billFile ? 'Change File' : 'Upload Bill'}
                </span>
              </label>

              <p className="text-xs text-gray-500 mt-4">
                Usually 3–10 pages
              </p>
            </div>
          </div>

          {/* Insurance Policy Upload */}
          <div className="bg-white rounded-xl border-2 border-gray-200 p-8">
            <div className="text-center">
              <div className="bg-blue-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                <FileText className="w-8 h-8 text-[#1E3A8A]" />
              </div>
              <h3 className="text-xl mb-2 text-gray-900">Insurance Policy</h3>
              <p className="text-sm text-gray-600 mb-4">
                Policy schedule or wording document (PDF only)
              </p>

              {policyFile ? (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <div className="flex items-center gap-2 justify-center text-green-700">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="text-sm truncate">{policyFile.name}</span>
                  </div>
                </div>
              ) : (
                <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4">
                  <Upload className="w-8 h-8 text-gray-400 mx-auto mb-2" />
                  <p className="text-sm text-gray-500">
                    Click below to upload
                  </p>
                </div>
              )}

              <label className="block">
                <input
                  type="file"
                  accept=".pdf"
                  onChange={handlePolicyUpload}
                  className="hidden"
                />
                <span className="bg-[#1E3A8A] hover:bg-[#1E40AF] text-white px-6 py-3 rounded-lg cursor-pointer inline-block transition-colors">
                  {policyFile ? 'Change File' : 'Upload Policy'}
                </span>
              </label>

              <p className="text-xs text-gray-500 mt-4">
                PDF format only
              </p>
            </div>
          </div>
        </div>

        {/* Privacy Notice */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8">
          <div className="flex items-start gap-3">
            <div className="bg-blue-100 p-2 rounded-lg flex-shrink-0">
              <FileText className="w-5 h-5 text-[#1E3A8A]" />
            </div>
            <div>
              <h4 className="text-gray-900 mb-1">Privacy Notice</h4>
              <p className="text-sm text-gray-700">
                Your documents are processed only for this audit and are not stored.
                We do not share or retain your personal information.
              </p>
            </div>
          </div>
        </div>

        {/* Start Audit Button */}
        <div className="text-center">
          {error && (
            <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-4">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          )}

          <button
            onClick={handleStartAudit}
            disabled={!billFile || !policyFile || isUploading}
            className={`px-8 py-4 rounded-lg text-lg transition-colors inline-flex items-center gap-2 ${billFile && policyFile && !isUploading
              ? 'bg-[#10B981] hover:bg-[#059669] text-white cursor-pointer'
              : 'bg-gray-300 text-gray-500 cursor-not-allowed'
              }`}
          >
            {isUploading ? 'Uploading...' : 'Start Bill Audit'}
            <span>→</span>
          </button>

          {(!billFile || !policyFile) && !isUploading && (
            <p className="text-sm text-gray-500 mt-4">
              Please upload both documents to continue
            </p>
          )}
        </div>
      </div>
    </div>
  );
}