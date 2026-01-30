import { useEffect, useState } from 'react';
import { AlertCircle, CheckCircle2, XCircle, FileText, AlertTriangle } from 'lucide-react';
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

  // Categorize flags by scope
  const eligibilityFlags = flags.filter(f => f.flag_scope === 'eligibility');
  const chargeFlags = flags.filter(f => f.flag_scope === 'charge');
  const infoFlags = flags.filter(f => f.flag_scope === 'informational');

  // Check if there are blocking eligibility issues (ERROR severity)
  const hasEligibilityBlock = eligibilityFlags.some(f => f.severity === 'error');

  // Calculate charge-level deductions (excluding eligibility blocks)
  const chargeLevelDeductions = chargeFlags.reduce((sum, flag) =>
    sum + (flag.amount_affected || 0), 0
  );

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
            <p className="text-sm text-gray-600 mb-2">Total Observations</p>
            <p className="text-3xl text-gray-900">{flags.length}</p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">
              {hasEligibilityBlock ? 'Under Review' : 'Charge Deductions'}
            </p>
            <p className={`text-3xl ${hasEligibilityBlock ? 'text-red-600' : 'text-amber-600'}`}>
              ₹{(hasEligibilityBlock ? total_billed : chargeLevelDeductions).toLocaleString('en-IN')}
            </p>
          </div>

          <div className="bg-white rounded-xl border border-gray-200 p-6">
            <p className="text-sm text-gray-600 mb-2">Status</p>
            <div className="flex items-center gap-2">
              {hasEligibilityBlock ? (
                <>
                  <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                  <p className="text-sm text-slate-700">Eligibility Review</p>
                </>
              ) : chargeFlags.length > 0 ? (
                <>
                  <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                  <p className="text-sm text-slate-700">Deductions Found</p>
                </>
              ) : (
                <>
                  <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                  <p className="text-sm text-slate-700">Eligible</p>
                </>
              )}
            </div>
          </div>
        </div>

        {/* ELIGIBILITY SECTION - Shown if eligibility issues exist */}
        {eligibilityFlags.length > 0 && (
          <div className={`rounded-xl border-2 overflow-hidden mb-8 ${hasEligibilityBlock ? 'bg-red-50 border-red-300' : 'bg-blue-50 border-blue-300'
            }`}>
            <div className={`px-6 py-4 ${hasEligibilityBlock ? 'bg-red-100' : 'bg-blue-100'}`}>
              <div className="flex items-center gap-3">
                {hasEligibilityBlock ? (
                  <XCircle className="w-6 h-6 text-red-700" />
                ) : (
                  <AlertCircle className="w-6 h-6 text-blue-700" />
                )}
                <h2 className={`text-2xl font-semibold ${hasEligibilityBlock ? 'text-red-900' : 'text-blue-900'
                  }`}>
                  {hasEligibilityBlock ? '🔴 Claim Under Eligibility Review' : 'ℹ️ Eligibility Observations'}
                </h2>
              </div>
            </div>

            <div className="p-6 space-y-4">
              {eligibilityFlags.map((flag: AuditFlag, index: number) => (
                <div key={index} className="bg-white rounded-lg border border-gray-200 p-5">
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <span className={`px-3 py-1 rounded-full text-sm font-medium ${flag.severity === 'error' ? 'bg-red-100 text-red-800' :
                            flag.severity === 'warning' ? 'bg-amber-100 text-amber-800' :
                              'bg-blue-100 text-blue-800'
                          }`}>
                          {flag.flag_type.replace('_', ' ').toUpperCase()}
                        </span>
                      </div>
                      <p className="text-gray-900 mb-2 text-lg">{flag.reason}</p>
                      {flag.policy_clause && (
                        <p className="text-sm text-gray-600">
                          <span className="font-medium">Policy Clause:</span> {flag.policy_clause}
                        </p>
                      )}
                    </div>
                    {flag.amount_affected && (
                      <div className="text-right ml-4">
                        <p className="text-sm text-gray-600 mb-1">Affected Amount</p>
                        <p className="text-2xl font-semibold text-red-700">
                          ₹{flag.amount_affected.toLocaleString('en-IN')}
                        </p>
                      </div>
                    )}
                  </div>

                  {hasEligibilityBlock && flag.severity === 'error' && (
                    <div className="mt-4 pt-4 border-t border-gray-200">
                      <p className="text-sm text-gray-700 italic">
                        ⚠️ This is a foundational issue that affects the entire claim. The claim cannot be processed until this is resolved.
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* CHARGE-LEVEL DEDUCTIONS SECTION */}
        {chargeFlags.length > 0 && (
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-8">
            <div className="bg-amber-50 px-6 py-4 border-b border-amber-200">
              <div className="flex items-center gap-3">
                <AlertTriangle className="w-6 h-6 text-amber-700" />
                <h2 className="text-2xl font-semibold text-amber-900">
                  {hasEligibilityBlock
                    ? 'Additional Observations (if claim is reconsidered)'
                    : '✅ Claim is Eligible — Charge-Level Deductions'}
                </h2>
              </div>
              {!hasEligibilityBlock && (
                <p className="text-sm text-gray-600 mt-2">
                  Your claim is eligible for processing. The following deductions apply to specific charges:
                </p>
              )}
            </div>

            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">Issue</th>
                    <th className="text-right px-6 py-4 text-sm font-semibold text-gray-700">Amount</th>
                    <th className="text-center px-6 py-4 text-sm font-semibold text-gray-700">Status</th>
                    <th className="text-left px-6 py-4 text-sm font-semibold text-gray-700">Explanation</th>
                  </tr>
                </thead>
                <tbody>
                  {chargeFlags.map((flag: AuditFlag, index: number) => (
                    <tr
                      key={index}
                      className={`border-b border-gray-100 ${flag.severity === 'error' ? 'bg-red-50' :
                          flag.severity === 'warning' ? 'bg-amber-50' : ''
                        }`}
                    >
                      <td className="px-6 py-4 text-gray-900 font-medium">
                        {flag.flag_type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </td>
                      <td className="px-6 py-4 text-right text-gray-900 font-semibold">
                        {flag.amount_affected
                          ? `₹${flag.amount_affected.toLocaleString('en-IN')}`
                          : '—'}
                      </td>
                      <td className="px-6 py-4">
                        <div className="flex items-center justify-center gap-2">
                          {flag.severity === 'info' && (
                            <>
                              <CheckCircle2 className="w-5 h-5 text-green-600" />
                              <span className="text-sm text-green-700">Noted</span>
                            </>
                          )}
                          {flag.severity === 'warning' && (
                            <>
                              <AlertCircle className="w-5 h-5 text-amber-600" />
                              <span className="text-sm text-amber-700">Deduction</span>
                            </>
                          )}
                          {flag.severity === 'error' && (
                            <>
                              <XCircle className="w-5 h-5 text-red-600" />
                              <span className="text-sm text-red-700">Excluded</span>
                            </>
                          )}
                        </div>
                      </td>
                      <td className="px-6 py-4 text-sm text-gray-600">
                        {flag.reason}
                        {flag.policy_clause && (
                          <span className="block text-xs text-gray-500 mt-1">
                            Ref: {flag.policy_clause}
                          </span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {!hasEligibilityBlock && chargeLevelDeductions > 0 && (
              <div className="bg-gray-50 px-6 py-4 border-t border-gray-200">
                <div className="flex justify-between items-center text-lg">
                  <span className="font-semibold text-gray-700">Total Bill:</span>
                  <span className="text-gray-900">₹{total_billed.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between items-center text-lg mt-2">
                  <span className="font-semibold text-gray-700">Total Deductions:</span>
                  <span className="text-amber-700">₹{chargeLevelDeductions.toLocaleString('en-IN')}</span>
                </div>
                <div className="flex justify-between items-center text-xl mt-3 pt-3 border-t border-gray-300">
                  <span className="font-bold text-gray-900">Estimated Payable Amount:</span>
                  <span className="font-bold text-green-700">
                    ₹{(total_billed - chargeLevelDeductions).toLocaleString('en-IN')}
                  </span>
                </div>
              </div>
            )}
          </div>
        )}

        {/* INFORMATIONAL SECTION */}
        {infoFlags.length > 0 && (
          <div className="bg-blue-50 rounded-xl border border-blue-200 p-6 mb-8">
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <AlertCircle className="w-6 h-6 text-blue-700" />
                </div>
              </div>
              <div className="flex-1">
                <h3 className="text-lg font-semibold mb-2 text-gray-900">For Your Information</h3>
                <div className="space-y-3">
                  {infoFlags.map((flag, idx) => (
                    <div key={idx} className="bg-white p-4 rounded-lg border border-blue-200">
                      <p className="text-gray-900 mb-1">
                        <span className="font-medium">{flag.flag_type.replace('_', ' ').toUpperCase()}:</span> {flag.reason}
                      </p>
                      {flag.amount_affected && (
                        <p className="text-sm text-gray-600">
                          Amount: ₹{flag.amount_affected.toLocaleString('en-IN')}
                        </p>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* No Issues Found */}
        {flags.length === 0 && (
          <div className="bg-white rounded-xl border border-gray-200 p-12 text-center mb-8">
            <CheckCircle2 className="w-16 h-16 text-green-600 mx-auto mb-4" />
            <h3 className="text-2xl mb-2 text-gray-900">No Issues Found</h3>
            <p className="text-gray-600">All charges appear to be compliant with your policy and IRDAI guidelines.</p>
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