import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle2, XCircle, FileText } from 'lucide-react';
import { getAuditResult } from '@/services/api';
import type { AuditResult, AuditFlag } from '@/types/types';

interface AuditResultsPageProps {
  auditId: string | null;
  auditResult: AuditResult | null;
  onResultLoaded: (result: AuditResult) => void;
  onGenerateDispute: () => void;
  isSample: boolean;
}

export default function AuditResultsPage({
  auditId,
  auditResult,
  onResultLoaded,
  onGenerateDispute,
  isSample
}: AuditResultsPageProps) {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (auditResult || !auditId) return;

    setIsLoading(true);
    setError(null);

    async function fetchResult() {
      try {
        const result = await getAuditResult(auditId!);
        onResultLoaded(result);
        setIsLoading(false);
      } catch (err) {
        console.error('Failed to load audit result:', err);
        setError(err instanceof Error ? err.message : 'Failed to load audit result');
        setIsLoading(false);
      }
    }

    fetchResult();
  }, [auditId, auditResult, onResultLoaded]);

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-teal-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading audit results...</p>
        </div>
      </div>
    );
  }

  if (error || !auditResult) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
        <div className="max-w-md w-full bg-white rounded-xl border border-red-200 p-8 text-center">
          <div className="bg-red-100 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
            <XCircle className="w-8 h-8 text-red-600" />
          </div>
          <h2 className="text-2xl mb-2 text-gray-900">Error Loading Results</h2>
          <p className="text-gray-600 mb-6">{error || 'No audit data available'}</p>
          <button
            onClick={() => window.location.reload()}
            className="bg-[#1E3A8A] hover:bg-[#1E40AF] text-white px-6 py-3 rounded-lg"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  const { flags, total_billed, amount_under_review, fully_covered_amount } = auditResult;

  // Group non-covered/review flags for explanation
  const flaggedItems = flags.filter(f => f.flag_type !== 'MISC' && f.amount_affected);

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-6xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl mb-4 text-gray-900">Insurance Claim Audit Summary</h1>
          <p className="text-xl text-gray-600">
            Review of charges against your policy and IRDAI guidelines
          </p>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">Total Bill Amount</p>
            <p className="text-3xl text-gray-900">₹{total_billed.toLocaleString('en-IN')}</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">Charges Reviewed</p>
            <p className="text-3xl text-gray-900">{flags.length}</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">Amount Requiring Review</p>
            <p className="text-3xl text-red-600">₹{amount_under_review.toLocaleString('en-IN')}</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">Status</p>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
              <p className="text-sm text-slate-700">
                {amount_under_review > 0 ? 'Potential Discrepancies' : 'All Clear'}
              </p>
            </div>
          </div>
        </div>

        {/* Flags Table */}
        {flags.length > 0 ? (
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-8">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-4 text-sm text-gray-700">Description</th>
                    <th className="text-right px-6 py-4 text-sm text-gray-700">Amount</th>
                    <th className="text-center px-6 py-4 text-sm text-gray-700">Status</th>
                    <th className="text-left px-6 py-4 text-sm text-gray-700">Reason</th>
                  </tr>
                </thead>
                <tbody>
                  {flags.map((flag: AuditFlag, index: number) => {
                    const isProblematic = flag.severity === 'WARNING' || flag.severity === 'ERROR';

                    return (
                      <tr
                        key={index}
                        className={`border-b border-gray-100 ${flag.severity === 'ERROR' ? 'bg-red-50' :
                            flag.severity === 'WARNING' ? 'bg-amber-50' :
                              ''
                          }`}
                      >
                        <td className="px-6 py-4 text-gray-900">
                          {flag.charge_description || flag.charge_category || flag.flag_type}
                        </td>
                        <td className="px-6 py-4 text-right text-gray-900">
                          {flag.amount_affected
                            ? `₹${flag.amount_affected.toLocaleString('en-IN')}`
                            : '—'}
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center justify-center gap-2">
                            {flag.severity === 'INFO' && (
                              <>
                                <CheckCircle2 className="w-5 h-5 text-green-600" />
                                <span className="text-sm text-green-700">Covered</span>
                              </>
                            )}
                            {flag.severity === 'WARNING' && (
                              <>
                                <AlertCircle className="w-5 h-5 text-amber-600" />
                                <span className="text-sm text-amber-700">Review</span>
                              </>
                            )}
                            {flag.severity === 'ERROR' && (
                              <>
                                <XCircle className="w-5 h-5 text-red-600" />
                                <span className="text-sm text-red-700">Not Allowed</span>
                              </>
                            )}
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-gray-600">{flag.reason}</td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div className="bg-white rounded-xl border border-gray-200 p-12 text-center mb-8">
            <CheckCircle2 className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h3 className="text-2xl mb-2 text-gray-900">No Issues Found</h3>
            <p className="text-gray-600">All charges appear to be compliant with your policy and IRDAI guidelines.</p>
          </div>
        )}

        {/* Explanation Box - Only show if there are flagged items */}
        {flaggedItems.length > 0 && (
          <div className="bg-amber-50 border-2 border-amber-200 rounded-xl p-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <div className="bg-amber-100 p-3 rounded-lg">
                  <AlertCircle className="w-6 h-6 text-amber-700" />
                </div>
              </div>
              <div>
                <h3 className="text-lg mb-2 text-gray-900">Explanation</h3>
                <p className="text-gray-700 leading-relaxed mb-4">
                  The charges marked above may not be permitted as per your policy terms or IRDAI guidelines.
                </p>
                <div className="space-y-3">
                  {flaggedItems.map((flag, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg border border-amber-200">
                      <p className="text-gray-900 mb-1">
                        <span className="font-medium">
                          {flag.charge_description || flag.charge_category}
                          {flag.amount_affected && ` (₹${flag.amount_affected.toLocaleString('en-IN')})`}:
                        </span>
                      </p>
                      <p className="text-sm text-gray-700">{flag.reason}</p>
                      {flag.regulatory_reference && (
                        <p className="text-xs text-gray-600 mt-2">
                          Reference: {flag.regulatory_reference}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="text-center">
          <button
            onClick={onGenerateDispute}
            className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-4 rounded-lg text-lg transition-colors inline-flex items-center gap-2"
          >
            <FileText className="w-5 h-5" />
            Generate Dispute Message
          </button>
          <p className="text-sm text-gray-500 mt-4">
            We'll create a ready-to-send message for your insurance company
          </p>
        </div>
      </div>
    </div>
  );
}