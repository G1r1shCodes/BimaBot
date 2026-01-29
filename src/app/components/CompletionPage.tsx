import { CheckCircle2, Home, FileText } from 'lucide-react';

interface CompletionPageProps {
  onAuditAnother: () => void;
  onReturnHome: () => void;
}

export default function CompletionPage({ onAuditAnother, onReturnHome }: CompletionPageProps) {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center px-6">
      <div className="max-w-2xl w-full">
        <div className="bg-white rounded-xl border border-gray-200 p-12 text-center">
          {/* Success Icon */}
          <div className="bg-green-100 w-24 h-24 rounded-full flex items-center justify-center mx-auto mb-8">
            <CheckCircle2 className="w-12 h-12 text-green-600" />
          </div>

          {/* Title */}
          <h1 className="text-4xl mb-4 text-gray-900">Audit Complete</h1>
          
          {/* Message */}
          <p className="text-xl text-gray-600 mb-8 max-w-lg mx-auto leading-relaxed">
            You've taken an informed step.
            Please focus on recovery while the claim is reviewed.
          </p>

          {/* Information Box */}
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8 text-left">
            <h3 className="text-lg mb-3 text-gray-900">What Happens Next?</h3>
            <ul className="space-y-2 text-gray-700">
              <li className="flex items-start gap-2">
                <span className="text-blue-600 mt-1">•</span>
                <span>Your insurance company will review the dispute within 15 days as per IRDAI regulations.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 mt-1">•</span>
                <span>Keep copies of all correspondence and documents for your records.</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-blue-600 mt-1">•</span>
                <span>If the response is unsatisfactory, you have the right to escalate to the Insurance Ombudsman.</span>
              </li>
            </ul>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={onAuditAnother}
              className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
            >
              <FileText className="w-5 h-5" />
              Audit Another Bill
            </button>

            <button
              onClick={onReturnHome}
              className="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 px-8 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
            >
              <Home className="w-5 h-5" />
              Return to Home
            </button>
          </div>

          {/* Additional Resources */}
          <div className="mt-8 pt-8 border-t border-gray-200">
            <h4 className="text-sm text-gray-600 mb-4">Additional Resources</h4>
            <div className="flex flex-col sm:flex-row gap-3 justify-center text-sm">
              <button className="text-[#1E3A8A] hover:underline">
                IRDAI Guidelines
              </button>
              <span className="hidden sm:inline text-gray-300">|</span>
              <button className="text-[#1E3A8A] hover:underline">
                Insurance Ombudsman Contact
              </button>
              <span className="hidden sm:inline text-gray-300">|</span>
              <button className="text-[#1E3A8A] hover:underline">
                Patient Rights
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
