import { Shield, FileText, CheckCircle2, AlertCircle, Lock, Users } from 'lucide-react';
import ScrollReveal from '@/app/components/ScrollReveal';

interface AboutProps {
  onNavigate: (page: 'home' | 'audit-bill') => void;
}

export default function About({ onNavigate }: AboutProps) {
  const whatItIs = [
    {
      title: 'A patient-side insurance claim auditor',
      icon: Shield
    },
    {
      title: 'A decision-support tool for hospital bills',
      icon: FileText
    },
    {
      title: 'A system that references insurance policies and IRDAI guidelines',
      icon: CheckCircle2
    },
    {
      title: 'A way to generate clear, actionable dispute messages',
      icon: FileText
    }
  ];

  const whatItIsNot = [
    'Not an insurance company',
    'Not a legal service or law firm',
    'Not a claim approval or rejection authority',
    'Not a replacement for insurers or lawyers'
  ];

  const principles = [
    {
      title: 'Clarity over complexity',
      description: 'Simple, understandable outputs that help you make decisions',
      icon: FileText
    },
    {
      title: 'Evidence over assumptions',
      description: 'All findings reference specific policy clauses and IRDAI guidelines',
      icon: CheckCircle2
    },
    {
      title: 'User trust over aggressive automation',
      description: 'You stay in control - we provide information, you take action',
      icon: Users
    },
    {
      title: 'Privacy by default',
      description: 'No accounts, no storage, no tracking',
      icon: Lock
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Page Header */}
      <section className="bg-gradient-to-br from-slate-50 to-teal-50 py-16 border-b border-gray-200">
        <div className="max-w-5xl mx-auto px-6 text-center">
          <div className="inline-block bg-teal-50 text-teal-700 px-4 py-2 rounded-full text-sm mb-6 border border-teal-200">
            About This Tool
          </div>
          <h1 className="text-slate-900 mb-4">About Bima Bot</h1>
          <p className="text-xl text-gray-700 max-w-3xl mx-auto leading-relaxed">
            A patient-side insurance claim auditing tool designed for hospital discharge.
          </p>
        </div>
      </section>

      {/* Main Content */}
      <div className="max-w-5xl mx-auto px-6 py-16">
        
        {/* Problem Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-slate-900 mb-4">Why Bima Bot Exists</h2>
          </div>
          
          <div className="bg-white rounded-xl border-2 border-gray-200 p-8 shadow-sm hover:shadow-md transition-shadow">
            <div className="space-y-6 text-gray-700 leading-relaxed text-lg">
              <p>
                Many insured patients in India face confusion and financial stress during hospital discharge. 
                Despite having health insurance, families are often asked to pay unexpected charges due to 
                complex policies, unclear deductions, and lack of real-time guidance.
              </p>
              <p className="text-[#1E3A8A] font-medium">
                Bima Bot was created to help patients verify their hospital bills and understand whether 
                deductions align with their policy terms and applicable IRDAI guidelines — before making payment.
              </p>
            </div>
          </div>
        </section>

        {/* What It Is Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-slate-900 mb-4">What Bima Bot Is</h2>
            <p className="text-gray-600 text-lg">Four core capabilities designed for clarity</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {whatItIs.map((item, index) => (
              <div 
                key={index}
                className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-teal-400 hover:shadow-lg transition-all group"
              >
                <div className="flex items-start gap-4">
                  <div className="bg-teal-50 p-3 rounded-lg group-hover:bg-teal-100 transition-colors flex-shrink-0">
                    <item.icon className="w-6 h-6 text-teal-600" />
                  </div>
                  <p className="text-gray-700 pt-2 leading-relaxed">{item.title}</p>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* What It Is Not Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-slate-900 mb-4">What Bima Bot Is Not</h2>
            <p className="text-gray-600 text-lg">Clear boundaries for your protection</p>
          </div>
          
          <div className="bg-slate-50 border-2 border-slate-300 rounded-xl p-8 shadow-sm">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
              {whatItIsNot.map((item, index) => (
                <div key={index} className="flex items-start gap-3 bg-white p-4 rounded-lg border border-gray-200">
                  <AlertCircle className="w-5 h-5 text-slate-500 mt-0.5 flex-shrink-0" />
                  <span className="text-gray-700">{item}</span>
                </div>
              ))}
            </div>
            <div className="pt-6 border-t-2 border-slate-300">
              <p className="text-gray-700 text-center font-medium">
                Bima Bot helps users take informed action; final decisions remain with insurers and hospitals.
              </p>
            </div>
          </div>
        </section>

        {/* Principles Section */}
        <section className="mb-20">
          <div className="text-center mb-12">
            <h2 className="text-slate-900 mb-4">Our Principles</h2>
            <p className="text-gray-600 text-lg">How we approach every audit</p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {principles.map((principle, index) => (
              <div 
                key={index}
                className="bg-white border-2 border-gray-200 rounded-xl p-6 hover:border-blue-300 hover:shadow-lg transition-all"
              >
                <div className="flex items-start gap-4 mb-3">
                  <div className="bg-blue-50 p-2 rounded-lg flex-shrink-0">
                    <principle.icon className="w-5 h-5 text-[#1E3A8A]" />
                  </div>
                  <h3 className="text-lg text-gray-900 pt-1">{principle.title}</h3>
                </div>
                <p className="text-gray-600 leading-relaxed ml-12">{principle.description}</p>
              </div>
            ))}
          </div>
        </section>

        {/* Trust & Responsibility Section */}
        <section className="mb-16">
          <div className="text-center mb-12">
            <h2 className="text-slate-900 mb-4">Trust & Responsibility</h2>
          </div>
          
          <div className="bg-gradient-to-br from-blue-50 to-teal-50 border-2 border-blue-200 rounded-xl p-8 shadow-sm">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div className="text-center">
                <div className="bg-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm border border-blue-100">
                  <Shield className="w-8 h-8 text-[#1E3A8A]" />
                </div>
                <h4 className="text-gray-900 mb-2">Decision Support</h4>
                <p className="text-sm text-gray-600">
                  Designed as a tool to inform, not replace professional judgment
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm border border-blue-100">
                  <FileText className="w-8 h-8 text-[#1E3A8A]" />
                </div>
                <h4 className="text-gray-900 mb-2">Public Guidelines</h4>
                <p className="text-sm text-gray-600">
                  All references based on user documents and IRDAI guidelines
                </p>
              </div>
              
              <div className="text-center">
                <div className="bg-white w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm border border-blue-100">
                  <Lock className="w-8 h-8 text-[#1E3A8A]" />
                </div>
                <h4 className="text-gray-900 mb-2">No Storage</h4>
                <p className="text-sm text-gray-600">
                  Documents processed only for audit, not stored after completion
                </p>
              </div>
            </div>
          </div>
        </section>

        {/* Call to Action */}
        <div className="text-center space-y-6 pt-12 border-t-2 border-gray-200">
          <h3 className="text-2xl text-gray-900">Ready to Audit Your Bill?</h3>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              onClick={() => onNavigate('audit-bill')}
              className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-4 rounded-lg text-lg transition-all hover:shadow-lg inline-flex items-center justify-center gap-2"
            >
              Audit My Hospital Bill
              <span>→</span>
            </button>
            <button
              className="border-2 border-gray-300 hover:border-[#1E3A8A] text-gray-700 hover:text-[#1E3A8A] px-8 py-4 rounded-lg text-lg transition-all hover:shadow-md inline-flex items-center justify-center gap-2"
            >
              <FileText className="w-5 h-5" />
              View Sample Bill & Audit
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}