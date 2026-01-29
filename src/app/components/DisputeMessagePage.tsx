import { useState } from 'react';
import { Copy, Download, CheckCircle2, Mail, Share2 } from 'lucide-react';
import type { AuditResult } from '@/types/types';

interface DisputeMessagePageProps {
  auditResult: AuditResult | null;
  onFinish: () => void;
}

export default function DisputeMessagePage({ auditResult, onFinish }: DisputeMessagePageProps) {
  const [copied, setCopied] = useState(false);

  // Use backend dispute letter content or fallback message
  const disputeMessage = auditResult?.dispute_letter_content ||
    'No dispute letter available. Please refresh and try again.';

  const handleCopy = () => {
    // Use fallback method that works reliably across all environments
    const textArea = document.createElement('textarea');
    textArea.value = disputeMessage;
    textArea.style.position = 'fixed';
    textArea.style.left = '-999999px';
    textArea.style.top = '-999999px';
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand('copy');
      if (successful) {
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (err) {
      console.error('Copy failed:', err);
    } finally {
      document.body.removeChild(textArea);
    }
  };

  const handleDownload = () => {
    const blob = new Blob([disputeMessage], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'dispute-message.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  const handleEmail = () => {
    const subject = encodeURIComponent('Request for Reconsideration of Claim Settlement - Policy No. HDFC/ERG/2025/12345');
    const body = encodeURIComponent(disputeMessage);
    window.location.href = `mailto:claims@insurancecompany.com?subject=${subject}&body=${body}`;
  };

  const handleWhatsApp = () => {
    const text = encodeURIComponent(disputeMessage);
    window.open(`https://wa.me/?text=${text}`, '_blank');
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-4xl mx-auto px-6">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl mb-4 text-gray-900">Dispute Message Ready</h1>
          <p className="text-xl text-gray-600">
            This message is based on your policy and applicable IRDAI guidelines.
          </p>
        </div>

        {/* Message Card */}
        <div className="bg-white rounded-xl border border-gray-200 overflow-hidden mb-8">
          {/* Message Header */}
          <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
            <div className="space-y-3">
              <div className="flex items-start">
                <span className="text-sm text-gray-600 w-20">To:</span>
                <span className="text-sm text-gray-900">claims@insurancecompany.com</span>
              </div>
              <div className="flex items-start">
                <span className="text-sm text-gray-600 w-20">Subject:</span>
                <span className="text-sm text-gray-900">
                  Request for Reconsideration of Claim Settlement - Policy No. HDFC/ERG/2025/12345
                </span>
              </div>
            </div>
          </div>

          {/* Message Body */}
          <div className="px-6 py-6">
            <pre className="whitespace-pre-wrap text-sm text-gray-700 leading-relaxed font-sans">
              {disputeMessage}
            </pre>
          </div>

          {/* Message Footer */}
          <div className="bg-blue-50 px-6 py-4 border-t border-blue-200">
            <p className="text-sm text-gray-700">
              <span className="font-medium">Note:</span> You can edit this message before sending.
              Make sure to attach your hospital bill and policy documents when submitting this dispute.
            </p>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-8">
          <button
            onClick={handleCopy}
            className="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
          >
            {copied ? (
              <>
                <CheckCircle2 className="w-5 h-5 text-green-600" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="w-5 h-5" />
                Copy Message
              </>
            )}
          </button>

          <button
            onClick={handleDownload}
            className="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
          >
            <Download className="w-5 h-5" />
            Download as PDF
          </button>

          <button
            onClick={handleEmail}
            className="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
          >
            <Mail className="w-5 h-5" />
            Email to Claims
          </button>

          <button
            onClick={handleWhatsApp}
            className="bg-white hover:bg-gray-50 border-2 border-gray-300 text-gray-700 px-6 py-3 rounded-lg transition-colors inline-flex items-center justify-center gap-2"
          >
            <Share2 className="w-5 h-5" />
            Share via WhatsApp
          </button>
        </div>

        {/* Next Steps */}
        <div className="bg-white rounded-xl border border-gray-200 p-6 mb-8">
          <h3 className="text-lg mb-4 text-gray-900">Next Steps</h3>
          <ol className="space-y-3 text-gray-700">
            <li className="flex items-start gap-3">
              <span className="bg-[#1E3A8A] text-white w-6 h-6 rounded-full flex items-center justify-center text-sm flex-shrink-0">1</span>
              <span>Send this message to your insurance company's claims department via email.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-[#1E3A8A] text-white w-6 h-6 rounded-full flex items-center justify-center text-sm flex-shrink-0">2</span>
              <span>Attach copies of your hospital bill and insurance policy documents.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-[#1E3A8A] text-white w-6 h-6 rounded-full flex items-center justify-center text-sm flex-shrink-0">3</span>
              <span>Keep a copy of this correspondence for your records.</span>
            </li>
            <li className="flex items-start gap-3">
              <span className="bg-[#1E3A8A] text-white w-6 h-6 rounded-full flex items-center justify-center text-sm flex-shrink-0">4</span>
              <span>If you don't receive a response within 15 days, you can escalate to the Insurance Ombudsman.</span>
            </li>
          </ol>
        </div>

        {/* Legal Disclaimer */}
        <div className="bg-slate-100 border-2 border-slate-300 rounded-xl p-6 mb-8">
          <h3 className="text-lg mb-3 text-gray-900 flex items-center gap-2">
            <svg className="w-5 h-5 text-slate-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Legal Disclaimer
          </h3>
          <p className="text-sm text-gray-700 leading-relaxed">
            This is a document-based audit and not legal advice. The analysis provided is based on
            available IRDAI guidelines and policy documents. For complex disputes or legal matters,
            please consult a qualified attorney or insurance advisor. Bima Bot does not guarantee
            claim approval or settlement outcomes.
          </p>
        </div>

        {/* Finish Button */}
        <div className="text-center">
          <button
            onClick={onFinish}
            className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-4 rounded-lg text-lg transition-colors inline-flex items-center gap-2"
          >
            Finish Audit
            <span>→</span>
          </button>
        </div>
      </div>
    </div>
  );
}