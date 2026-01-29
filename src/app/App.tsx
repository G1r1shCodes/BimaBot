import { useState, useEffect } from 'react';
import HomePage from '@/app/components/HomePage';
import AuditBillPage from '@/app/components/AuditBillPage';
import ProcessingPage from '@/app/components/ProcessingPage';
import AuditResultsPage from '@/app/components/AuditResultsPage';
import DisputeMessagePage from '@/app/components/DisputeMessagePage';
import CompletionPage from '@/app/components/CompletionPage';
import HowItWorks from '@/app/components/HowItWorks';
import About from '@/app/components/About';
import Navigation from '@/app/components/Navigation';
import type { AuditResult } from '@/types/types';

type Page = 'home' | 'audit-bill' | 'processing' | 'results' | 'dispute' | 'completion' | 'how-it-works' | 'about';

interface AuditData {
  billFile: File | null;
  policyFile: File | null;
  isSample: boolean;
}

// localStorage keys
const STORAGE_KEYS = {
  AUDIT_ID: 'bimabot_audit_id',
  AUDIT_RESULT: 'bimabot_audit_result',
  CURRENT_PAGE: 'bimabot_current_page',
};

export default function App() {
  const [currentPage, setCurrentPage] = useState<Page>('home');
  const [isAuditMode, setIsAuditMode] = useState(false);
  const [auditData, setAuditData] = useState<AuditData>({
    billFile: null,
    policyFile: null,
    isSample: false
  });

  // NEW: Backend integration state
  const [auditId, setAuditId] = useState<string | null>(null);
  const [auditResult, setAuditResult] = useState<AuditResult | null>(null);

  // Restore state from localStorage on mount
  useEffect(() => {
    const savedAuditId = localStorage.getItem(STORAGE_KEYS.AUDIT_ID);
    const savedAuditResult = localStorage.getItem(STORAGE_KEYS.AUDIT_RESULT);
    const savedPage = localStorage.getItem(STORAGE_KEYS.CURRENT_PAGE);

    if (savedAuditId) {
      setAuditId(savedAuditId);
    }

    if (savedAuditResult) {
      try {
        setAuditResult(JSON.parse(savedAuditResult));
      } catch (e) {
        console.error('Failed to parse saved audit result:', e);
        localStorage.removeItem(STORAGE_KEYS.AUDIT_RESULT);
      }
    }

    if (savedPage && savedAuditId) {
      setCurrentPage(savedPage as Page);
      setIsAuditMode(true);
    }
  }, []);

  // Save audit ID to localStorage whenever it changes
  useEffect(() => {
    if (auditId) {
      localStorage.setItem(STORAGE_KEYS.AUDIT_ID, auditId);
    }
  }, [auditId]);

  // Save audit result to localStorage whenever it changes
  useEffect(() => {
    if (auditResult) {
      localStorage.setItem(STORAGE_KEYS.AUDIT_RESULT, JSON.stringify(auditResult));
    }
  }, [auditResult]);

  // Save current page to localStorage
  useEffect(() => {
    if (isAuditMode) {
      localStorage.setItem(STORAGE_KEYS.CURRENT_PAGE, currentPage);
    }
  }, [currentPage, isAuditMode]);

  const startAudit = (billFile: File | null, policyFile: File | null, isSample = false, receivedAuditId?: string) => {
    setAuditData({ billFile, policyFile, isSample });

    // Store audit ID if provided (from API call)
    if (receivedAuditId) {
      setAuditId(receivedAuditId);
    }

    setIsAuditMode(true);
    setCurrentPage('processing');
  };

  const navigateTo = (page: Page) => {
    setCurrentPage(page);
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const finishAudit = () => {
    setIsAuditMode(false);
    setAuditData({ billFile: null, policyFile: null, isSample: false });

    // Clear backend state
    setAuditId(null);
    setAuditResult(null);

    // Clear localStorage
    localStorage.removeItem(STORAGE_KEYS.AUDIT_ID);
    localStorage.removeItem(STORAGE_KEYS.AUDIT_RESULT);
    localStorage.removeItem(STORAGE_KEYS.CURRENT_PAGE);

    setCurrentPage('home');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const handleSampleAudit = async () => {
    try {
      // Import api
      const { api } = await import('@/app/services/api');

      // Start audit session on backend
      const { audit_id } = await api.startAudit();

      // Start audit with the received ID
      startAudit(null, null, true, audit_id);
    } catch (err) {
      console.error('Failed to start sample audit:', err);
      alert('Failed to connect to backend. Please ensure the server is running.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {!isAuditMode && <Navigation currentPage={currentPage} onNavigate={navigateTo} />}

      <main>
        {currentPage === 'home' && (
          <HomePage
            onStartAudit={() => navigateTo('audit-bill')}
            onStartSampleAudit={handleSampleAudit}
            onNavigate={navigateTo}
          />
        )}

        {currentPage === 'audit-bill' && (
          <AuditBillPage onStartAudit={startAudit} />
        )}

        {currentPage === 'processing' && (
          <ProcessingPage
            auditId={auditId}
            onComplete={() => navigateTo('results')}
            isSample={auditData.isSample}
          />
        )}

        {currentPage === 'results' && (
          <AuditResultsPage
            auditId={auditId}
            auditResult={auditResult}
            onResultLoaded={setAuditResult}
            onGenerateDispute={() => navigateTo('dispute')}
            isSample={auditData.isSample}
          />
        )}

        {currentPage === 'dispute' && (
          <DisputeMessagePage
            auditResult={auditResult}
            onFinish={() => navigateTo('completion')}
          />
        )}

        {currentPage === 'completion' && (
          <CompletionPage
            onAuditAnother={finishAudit}
            onReturnHome={finishAudit}
          />
        )}

        {currentPage === 'how-it-works' && (
          <HowItWorks onNavigate={navigateTo} />
        )}

        {currentPage === 'about' && (
          <About onNavigate={navigateTo} />
        )}
      </main>
    </div>
  );
}