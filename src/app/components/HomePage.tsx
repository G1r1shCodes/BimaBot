import { useState } from 'react';
import { Upload, Trash2, Scale, FileText, Shield, AlertTriangle } from 'lucide-react';
import SampleBillModal from '@/app/components/SampleBillModal';
import TechStackFlow from '@/app/components/TechStackFlow';
import ScrollReveal from '@/app/components/ScrollReveal';
import logoImage from '/images/bima bot logo.jpg.jpeg';

interface HomePageProps {
  onStartAudit: () => void;
  onStartSampleAudit: () => void;
  onNavigate?: (page: 'how-it-works' | 'about') => void;
}

export default function HomePage({ onStartAudit, onStartSampleAudit, onNavigate }: HomePageProps) {
  const [showSampleModal, setShowSampleModal] = useState(false);
  const [showDisclaimerModal, setShowDisclaimerModal] = useState(false);

  return (
    <div>
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-slate-50 to-teal-50 py-20">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="inline-block bg-teal-50 text-teal-700 px-4 py-2 rounded-full text-sm mb-6 border border-teal-200">
                Your Insurance Advocate at the Hospital Billing Desk
              </div>

              <h1 className="text-5xl mb-6 text-gray-900 leading-tight">
                Check Your Hospital Bill Before You Pay It
              </h1>

              <p className="text-xl text-gray-600 mb-8 leading-relaxed">
                Even insured patients are often charged unfairly at discharge.
                Bima Bot helps you verify your insurance claim in minutes.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 mb-4">
                <button
                  onClick={onStartAudit}
                  className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-4 rounded-lg text-lg transition-all hover:shadow-lg flex items-center justify-center gap-2"
                >
                  Audit My Hospital Bill
                  <span>→</span>
                </button>

                <button
                  onClick={() => setShowSampleModal(true)}
                  className="border-2 border-gray-300 hover:border-[#1E3A8A] text-gray-700 hover:text-[#1E3A8A] px-8 py-4 rounded-lg text-lg transition-all hover:shadow-md flex items-center justify-center gap-2"
                >
                  <FileText className="w-5 h-5" />
                  View Sample Bill & Audit
                </button>
              </div>

              <p className="text-sm text-gray-500">
                No signup required. Documents are not stored.
              </p>
            </div>

            {/* Bill Analysis Preview Card */}
            <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
              <div className="flex items-center gap-3 mb-6">
                <div className="bg-blue-100 p-3 rounded-lg">
                  <FileText className="w-6 h-6 text-[#1E3A8A]" />
                </div>
                <div>
                  <h3 className="text-lg text-gray-900">Bill Analysis</h3>
                  <p className="text-sm text-gray-500">In Progress</p>
                </div>
              </div>

              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
                  <span className="text-gray-700">Room Charges</span>
                  <span className="text-green-700 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    Valid
                  </span>
                </div>

                <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
                  <span className="text-gray-700">Consumables</span>
                  <span className="text-red-700 flex items-center gap-2">
                    <span className="w-2 h-2 bg-red-500 rounded-full"></span>
                    Flagged
                  </span>
                </div>

                <div className="flex items-center justify-between p-4 bg-green-50 rounded-lg border border-green-200">
                  <span className="text-gray-700">Surgery</span>
                  <span className="text-green-700 flex items-center gap-2">
                    <span className="w-2 h-2 bg-green-500 rounded-full"></span>
                    Valid
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Problem Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl mb-4 text-gray-900">
              Even Insured Patients Pay More Than They Should
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Hospital billing is complex and often works against patients. Here's what you're up against.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="bg-red-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <AlertTriangle className="w-8 h-8 text-red-600" />
              </div>
              <h3 className="text-xl mb-3 text-gray-900">Hidden Deductions</h3>
              <p className="text-gray-600">
                Hospitals often apply unauthorized deductions that violate IRDAI guidelines.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-red-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-red-600" />
              </div>
              <h3 className="text-xl mb-3 text-gray-900">Confusing Policies</h3>
              <p className="text-gray-600">
                Insurance documents are complex and hard to understand in stressful times.
              </p>
            </div>

            <div className="text-center">
              <div className="bg-red-50 w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileText className="w-8 h-8 text-red-600" />
              </div>
              <h3 className="text-xl mb-3 text-gray-900">Panic at Discharge</h3>
              <p className="text-gray-600">
                Patients are pressured to pay at discharge without time to verify charges.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-6">
          <ScrollReveal>
            <div className="text-center mb-16">
              <h2 className="text-4xl mb-4 text-gray-900">How Bima Bot Works</h2>
              <p className="text-xl text-gray-600">
                A simple, structured process to review your hospital bill and identify questionable deductions.
              </p>
            </div>
          </ScrollReveal>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
            <ScrollReveal delay={0.1}>
              <div className="text-center">
                <div className="relative inline-block">
                  <div className="bg-blue-100 w-20 h-20 rounded-2xl flex items-center justify-center mb-6">
                    <Upload className="w-10 h-10 text-[#1E3A8A]" />
                  </div>
                  <div className="absolute -top-3 -right-3 bg-[#10B981] text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold shadow-lg">
                    1
                  </div>
                </div>
                <h3 className="text-xl mb-3 text-gray-900">Upload Documents</h3>
                <p className="text-gray-600">
                  Upload your hospital bill and insurance policy documents.
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={0.2}>
              <div className="text-center">
                <div className="relative inline-block">
                  <div className="bg-blue-100 w-20 h-20 rounded-2xl flex items-center justify-center mb-6">
                    <Scale className="w-10 h-10 text-[#1E3A8A]" />
                  </div>
                  <div className="absolute -top-3 -right-3 bg-[#10B981] text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold shadow-lg">
                    2
                  </div>
                </div>
                <h3 className="text-xl mb-3 text-gray-900">Bill Audit</h3>
                <p className="text-gray-600">
                  Our system analyzes charges against IRDAI rules and your policy.
                </p>
              </div>
            </ScrollReveal>

            <ScrollReveal delay={0.3}>
              <div className="text-center">
                <div className="relative inline-block">
                  <div className="bg-blue-100 w-20 h-20 rounded-2xl flex items-center justify-center mb-6">
                    <FileText className="w-10 h-10 text-[#1E3A8A]" />
                  </div>
                  <div className="absolute -top-3 -right-3 bg-[#10B981] text-white w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold shadow-lg">
                    3
                  </div>
                </div>
                <h3 className="text-xl mb-3 text-gray-900">Take Action</h3>
                <p className="text-gray-600">
                  Get a ready-to-send dispute message for unfair charges.
                </p>
              </div>
            </ScrollReveal>
          </div>
        </div>
      </section>

      {/* Technology Stack Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-4xl mb-4 text-gray-900">Enterprise AI Technology</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Bima Bot leverages industry-leading AI and cloud infrastructure to deliver accurate, reliable bill audits in seconds.
            </p>
          </div>

          <div className="max-w-5xl mx-auto">
            <TechStackFlow showcaseMode={true} />
          </div>

          <div className="mt-12 text-center">
            <p className="text-sm text-gray-500 max-w-2xl mx-auto">
              Our AI pipeline processes your documents securely using AWS and IBM Watson technologies, ensuring institutional-grade accuracy while protecting your privacy.
            </p>
          </div>
        </div>
      </section>

      {/* Privacy Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl mb-4 text-gray-900">Built With Your Privacy in Mind</h2>
            <p className="text-xl text-gray-600">
              We prioritize your privacy and security at every step.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-gray-50 p-8 rounded-xl border border-gray-200">
              <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <Shield className="w-6 h-6 text-green-700" />
              </div>
              <h3 className="text-lg mb-2 text-gray-900">No Signup Required</h3>
              <p className="text-gray-600">
                Start auditing immediately without creating an account.
              </p>
            </div>

            <div className="bg-gray-50 p-8 rounded-xl border border-gray-200">
              <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <Trash2 className="w-6 h-6 text-green-700" />
              </div>
              <h3 className="text-lg mb-2 text-gray-900">Documents Auto-Deleted</h3>
              <p className="text-gray-600">
                Your files are processed and deleted—we don't store them.
              </p>
            </div>

            <div className="bg-gray-50 p-8 rounded-xl border border-gray-200">
              <div className="bg-green-100 w-12 h-12 rounded-lg flex items-center justify-center mb-4">
                <Scale className="w-6 h-6 text-green-700" />
              </div>
              <h3 className="text-lg mb-2 text-gray-900">Decision-Support Tool</h3>
              <p className="text-gray-600">
                We help you understand your rights under IRDAI guidelines.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-[#1E3A8A] to-[#1E40AF]">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h2 className="text-4xl mb-4 text-white">
            Ready to Audit Your Hospital Bill?
          </h2>
          <p className="text-xl text-blue-100 mb-8">
            Don't let unfair charges go unnoticed. Start your free audit now and take control of your healthcare expenses.
          </p>
          <button
            onClick={onStartAudit}
            className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-4 rounded-lg text-lg transition-all hover:shadow-lg inline-flex items-center gap-2"
          >
            Start Bill Audit Now
            <span>→</span>
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200 py-12">
        <div className="max-w-7xl mx-auto px-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-12 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <img src={logoImage} alt="Bima Bot" className="h-6 w-6" />
                <span className="text-xl text-slate-700">Bima Bot</span>
              </div>
              <p className="text-gray-600 text-sm">
                Your insurance advocate. We help you identify unfair deductions in hospital bills and take action to protect your rights.
              </p>
            </div>

            <div>
              <h4 className="text-gray-900 mb-4">Quick Links</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><button onClick={onStartAudit} className="hover:text-[#1E3A8A] transition-colors">Audit Bill</button></li>
                <li><button onClick={() => onNavigate?.('how-it-works')} className="hover:text-[#1E3A8A] transition-colors">How It Works</button></li>
                <li><button onClick={() => onNavigate?.('about')} className="hover:text-[#1E3A8A] transition-colors">About Us</button></li>
              </ul>
            </div>

            <div>
              <h4 className="text-gray-900 mb-4">Legal</h4>
              <ul className="space-y-2 text-sm text-gray-600">
                <li><button onClick={() => setShowDisclaimerModal(true)} className="hover:text-[#1E3A8A] transition-colors">Disclaimer</button></li>
              </ul>
            </div>
          </div>

          <div className="pt-8 border-t border-gray-200 flex flex-col md:flex-row justify-between items-center text-sm text-gray-500">
            <p>© 2026 Bima Bot. All rights reserved.</p>
          </div>
        </div>
      </footer>

      {/* Sample Bill Modal */}
      {showSampleModal && (
        <SampleBillModal
          onClose={() => setShowSampleModal(false)}
          onRunSampleAudit={() => {
            setShowSampleModal(false);
            onStartSampleAudit();
          }}
        />
      )}

      {/* Disclaimer Modal */}
      {showDisclaimerModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center z-50 p-4 pt-12 overflow-y-auto">
          <div className="bg-white rounded-xl max-w-3xl w-full max-h-[90vh] overflow-y-auto">
            <div className="p-8">
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center gap-3">
                  <div className="bg-blue-100 p-3 rounded-lg">
                    <Scale className="w-6 h-6 text-[#1E3A8A]" />
                  </div>
                  <div>
                    <h2 className="text-2xl text-gray-900">Legal Disclaimer</h2>
                    <p className="text-sm text-gray-500">Important information about Bima Bot services</p>
                  </div>
                </div>
                <button
                  onClick={() => setShowDisclaimerModal(false)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <div className="space-y-6 text-gray-700">
                <div className="bg-amber-50 border border-amber-200 rounded-lg p-4">
                  <h3 className="text-lg mb-2 text-gray-900">Decision-Support Tool Only</h3>
                  <p className="text-sm">
                    Bima Bot is a decision-support tool designed to help you understand your insurance policy and hospital bills. It is not a substitute for professional legal, financial, or medical advice.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">Not Legal or Financial Advice</h3>
                  <p className="text-sm leading-relaxed">
                    The information and analysis provided by Bima Bot are for informational purposes only. They do not constitute legal advice, financial advice, or any form of professional consultation. Users should consult with qualified professionals before making decisions based on the tool's output.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">No Guarantee of Accuracy</h3>
                  <p className="text-sm leading-relaxed">
                    While Bima Bot uses IRDAI guidelines and policy documents to analyze bills, we make no guarantees about the accuracy, completeness, or reliability of the analysis. Insurance policies are complex legal documents, and actual coverage may vary based on specific terms and conditions.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">User Responsibility</h3>
                  <p className="text-sm leading-relaxed">
                    Users are solely responsible for reviewing all audit results and making informed decisions. Bima Bot does not make decisions on your behalf. Any actions taken based on the tool's output are at the user's own risk.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">No Liability</h3>
                  <p className="text-sm leading-relaxed">
                    Bima Bot and its operators shall not be held liable for any claims, losses, damages, or disputes arising from the use of this tool. This includes, but is not limited to, denied insurance claims, financial losses, or legal disputes with hospitals or insurance providers.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">Privacy and Data Security</h3>
                  <p className="text-sm leading-relaxed">
                    Uploaded documents are processed for analysis purposes only and are automatically deleted after processing. We do not store personal health information, medical records, or personally identifiable information. However, users should be aware of the risks involved in uploading sensitive documents online.
                  </p>
                </div>

                <div>
                  <h3 className="text-lg mb-2 text-gray-900">Regulatory Compliance</h3>
                  <p className="text-sm leading-relaxed">
                    Our analysis references IRDAI (Insurance Regulatory and Development Authority of India) guidelines as publicly available. However, insurance regulations are subject to change, and specific implementations may vary by insurer. Always verify current regulations and policy-specific terms.
                  </p>
                </div>

                <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
                  <h3 className="text-lg mb-2 text-gray-900">Acceptance of Terms</h3>
                  <p className="text-sm">
                    By using Bima Bot, you acknowledge that you have read, understood, and agree to this disclaimer. If you do not agree with any part of this disclaimer, please do not use the service.
                  </p>
                </div>
              </div>

              <div className="mt-8 flex justify-end">
                <button
                  onClick={() => setShowDisclaimerModal(false)}
                  className="bg-[#1E3A8A] hover:bg-[#1E40AF] text-white px-6 py-3 rounded-lg transition-colors"
                >
                  I Understand
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}