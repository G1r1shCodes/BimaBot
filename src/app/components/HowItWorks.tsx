import { FileText, CheckSquare, FileCheck, Mail } from 'lucide-react';
import { motion } from 'motion/react';
import { useEffect, useRef, useState } from 'react';
import ScrollReveal from '@/app/components/ScrollReveal';

interface HowItWorksProps {
  onNavigate: (page: 'home' | 'audit-bill') => void;
}

export default function HowItWorks({ onNavigate }: HowItWorksProps) {
  const [stepsVisible, setStepsVisible] = useState(false);
  const stepsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setStepsVisible(true);
          observer.disconnect(); // Only animate once
        }
      },
      {
        threshold: 0.2,
        rootMargin: '0px'
      }
    );

    if (stepsRef.current) {
      observer.observe(stepsRef.current);
    }

    return () => observer.disconnect();
  }, []);

  const steps = [
    {
      number: '1',
      icon: FileText,
      heading: 'Upload Your Bill & Policy',
      description: 'Upload your final hospital bill and insurance policy. You can upload photos or PDFs.',
      helper: 'Most hospital bills are 3–10 pages long.'
    },
    {
      number: '2',
      icon: CheckSquare,
      heading: 'Claim Verification',
      description: 'Bima Bot reviews bill items and checks them against your insurance policy terms.',
      helper: null
    },
    {
      number: '3',
      icon: FileCheck,
      heading: 'IRDAI Guideline Check',
      description: 'Each charge is verified against applicable IRDAI guidelines to identify deductions that may not be permitted.',
      helper: 'Only publicly available IRDAI circulars are referenced.'
    },
    {
      number: '4',
      icon: Mail,
      heading: 'Ready-to-Use Dispute Message',
      description: 'If any charges require review, you receive a formal dispute message you can share with the billing desk or TPA.',
      helper: null
    }
  ];

  const outputs = [
    'Claim audit summary',
    'Clear list of charges requiring review',
    'References to policy or IRDAI guidelines',
    'Ready-to-send dispute message'
  ];

  const boundaries = [
    'Does not approve or reject claims',
    'Does not replace insurance companies or lawyers',
    'Does not submit claims on your behalf'
  ];

  const privacyPoints = [
    'Documents are processed only for this audit',
    'Files are not stored after completion',
    'No account or login is required'
  ];

  return (
    <div className="min-h-screen bg-white">
      {/* Page Header */}
      <ScrollReveal>
        <div className="bg-slate-50 border-b border-gray-200">
          <div className="max-w-4xl mx-auto px-6 py-12 text-center">
            <h1 className="text-slate-900 mb-3">How Bima Bot Works</h1>
            <p className="text-gray-700 max-w-2xl mx-auto">
              Bima Bot helps you verify your hospital bill against your insurance policy and IRDAI guidelines — before you pay.
            </p>
          </div>
        </div>
      </ScrollReveal>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-6 py-12">
        
        {/* Process Section */}
        <section className="mb-16" ref={stepsRef}>
          <ScrollReveal delay={0.05}>
            <h2 className="text-slate-900 mb-8 text-center">
              The Audit Process
            </h2>
          </ScrollReveal>
          
          <div className="relative space-y-6">
            {steps.map((step, index) => (
              <ScrollReveal key={step.number} delay={index * 0.05}>
                <div className="flex gap-6 p-6 bg-white border border-gray-200 rounded-lg hover:border-gray-300 hover:shadow-md transition-all relative">
                  {/* Step Number & Icon */}
                  <div className="flex-shrink-0">
                    <motion.div 
                      className="w-12 h-12 rounded-full bg-teal-50 border-2 border-teal-500 flex items-center justify-center mb-3 relative z-10"
                      initial={{ scale: 0 }}
                      animate={stepsVisible ? { scale: 1 } : { scale: 0 }}
                      transition={{ 
                        delay: index * 0.15, 
                        duration: 0.3,
                        ease: [0.25, 0.1, 0.25, 1]
                      }}
                    >
                      <span className="text-teal-700 font-semibold">
                        {step.number}
                      </span>
                    </motion.div>
                    <div className="flex justify-center">
                      <step.icon className="w-6 h-6 text-gray-400" />
                    </div>
                  </div>

                  {/* Content */}
                  <div className="flex-1 pt-1">
                    <h3 className="text-slate-900 mb-2">{step.heading}</h3>
                    <p className="text-gray-700 leading-relaxed mb-2">
                      {step.description}
                    </p>
                    {step.helper && (
                      <p className="text-sm text-gray-500 italic">
                        {step.helper}
                      </p>
                    )}
                  </div>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </section>

        {/* Outputs Section */}
        <ScrollReveal>
          <section className="mb-16">
            <h2 className="text-slate-900 mb-6 text-center">What You Receive</h2>
            
            <div className="bg-slate-50 border border-gray-200 rounded-lg p-6">
              <ul className="space-y-3">
                {outputs.map((output, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-teal-600 mt-1 flex-shrink-0">✔</span>
                    <span className="text-gray-700">{output}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </ScrollReveal>

        {/* Boundaries Section */}
        <ScrollReveal>
          <section className="mb-16">
            <h2 className="text-slate-900 mb-6 text-center">What Bima Bot Does Not Do</h2>
            
            <div className="bg-white border border-gray-300 rounded-lg p-6">
              <ul className="space-y-3 mb-4">
                {boundaries.map((boundary, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-gray-400 mt-1 flex-shrink-0">•</span>
                    <span className="text-gray-700">{boundary}</span>
                  </li>
                ))}
              </ul>
              <p className="text-gray-600 text-sm mt-4 pt-4 border-t border-gray-200">
                Bima Bot is a decision-support tool to help you take informed action.
              </p>
            </div>
          </section>
        </ScrollReveal>

        {/* Privacy Section */}
        <ScrollReveal>
          <section className="mb-12">
            <h2 className="text-slate-900 mb-6 text-center">Data Privacy & Security</h2>
            
            <div className="bg-slate-50 border border-gray-200 rounded-lg p-6">
              <ul className="space-y-3">
                {privacyPoints.map((point, index) => (
                  <li key={index} className="flex items-start gap-3">
                    <span className="text-teal-600 mt-1 flex-shrink-0">✔</span>
                    <span className="text-gray-700">{point}</span>
                  </li>
                ))}
              </ul>
            </div>
          </section>
        </ScrollReveal>

        {/* Call to Action */}
        <ScrollReveal>
          <div className="text-center space-y-4 pt-8 border-t border-gray-200">
            <button
              onClick={() => onNavigate('audit-bill')}
              className="bg-[#10B981] hover:bg-[#059669] text-white px-8 py-3 rounded-lg transition-all hover:shadow-lg"
            >
              Audit My Hospital Bill
            </button>
            <div>
              <button
                className="text-gray-600 hover:text-gray-900 text-sm underline"
              >
                View Sample Bill & Audit
              </button>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </div>
  );
}