import { useEffect, useState } from 'react';
import { CheckCircle2 } from 'lucide-react';
import { api } from '@/services/api';

interface ProcessingPageProps {
  auditId: string | null;
  onComplete: () => void;
  isSample: boolean;
}

export default function ProcessingPage({ auditId, onComplete, isSample }: ProcessingPageProps) {
  const [currentStep, setCurrentStep] = useState(0);
  const [error, setError] = useState<string | null>(null);

  const steps = [
    'Reading hospital bill',
    'Checking policy coverage',
    'Verifying IRDAI guidelines'
  ];

  useEffect(() => {
    if (!auditId) {
      setError('No audit ID found');
      return;
    }

    let cancelled = false;
    let pollInterval: NodeJS.Timeout;

    async function processAudit() {
      try {
        // Step 1: Trigger processing
        await api.completeAudit(auditId!);

        setCurrentStep(1);

        // Step 2: Poll for status
        pollInterval = setInterval(async () => {
          if (cancelled) return;

          try {
            const { status } = await api.getAuditStatus(auditId!);

            // Update steps based on progress
            if (status === 'processing') {
              setCurrentStep((prev) => Math.min(prev + 1, steps.length - 1));
            } else if (status === 'completed') {
              setCurrentStep(steps.length);
              clearInterval(pollInterval);

              // Wait a moment to show completed state
              setTimeout(() => {
                if (!cancelled) {
                  onComplete();
                }
              }, 500);
            } else if (status === 'failed') {
              clearInterval(pollInterval);
              setError('Audit processing failed. Please try again.');
            }
          } catch (err) {
            console.error('Status poll error:', err);
            // Continue polling even if one request fails
          }
        }, 2000); // Poll every 2 seconds

      } catch (err) {
        console.error('Failed to start processing:', err);
        setError(err instanceof Error ? err.message : 'Failed to start processing');
      }
    }

    processAudit();

    // Cleanup
    return () => {
      cancelled = true;
      if (pollInterval) {
        clearInterval(pollInterval);
      }
    };
  }, [auditId, onComplete]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6 py-12">
        <div className="max-w-2xl w-full">
          <div className="bg-white rounded-xl border border-red-200 p-12">
            <div className="text-center">
              <div className="bg-red-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
                <svg className="w-10 h-10 text-red-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </div>
              <h1 className="text-3xl mb-4 text-gray-900">Processing Error</h1>
              <p className="text-gray-600 mb-6">{error}</p>
              <button
                onClick={() => window.location.reload()}
                className="bg-[#1E3A8A] hover:bg-[#1E40AF] text-white px-6 py-3 rounded-lg"
              >
                Try Again
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6 py-12">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-xl border border-gray-200 p-12">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="bg-teal-100 w-20 h-20 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-teal-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <h1 className="text-3xl mb-4 text-gray-900">Verifying Your Bill</h1>
            <p className="text-gray-600">
              This usually takes under one minute.
            </p>
          </div>

          {/* Progress Steps */}
          <div className="space-y-4">
            {steps.map((step, index) => (
              <div
                key={index}
                className={`flex items-center gap-4 p-4 rounded-lg border-2 transition-all ${index < currentStep
                  ? 'bg-teal-50 border-teal-200'
                  : index === currentStep
                    ? 'bg-slate-50 border-slate-300'
                    : 'bg-gray-50 border-gray-200'
                  }`}
              >
                <div className="flex-shrink-0">
                  {index < currentStep ? (
                    <CheckCircle2 className="w-6 h-6 text-teal-600" />
                  ) : index === currentStep ? (
                    <div className="w-6 h-6 rounded-full border-2 border-teal-600 bg-teal-100" />
                  ) : (
                    <div className="w-6 h-6 rounded-full border-2 border-gray-300" />
                  )}
                </div>
                <span
                  className={`text-lg ${index < currentStep
                    ? 'text-teal-700'
                    : index === currentStep
                      ? 'text-slate-700'
                      : 'text-gray-500'
                    }`}
                >
                  {step}
                </span>
              </div>
            ))}
          </div>

          {/* Progress Bar */}
          <div className="mt-8">
            <div className="bg-gray-200 rounded-full h-2 overflow-hidden">
              <div
                className="bg-teal-600 h-full transition-all duration-1000 ease-out"
                style={{ width: `${(currentStep / steps.length) * 100}%` }}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}