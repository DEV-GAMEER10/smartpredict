'use client';

import { useState, useEffect, useCallback } from 'react';
import api from '@/lib/api';
import Sidebar from '@/components/dashboard/Sidebar';
import Header from '@/components/dashboard/Header';
import KPICards from '@/components/dashboard/KPICards';
import WhatsHappening from '@/components/dashboard/WhatsHappening';
import WhatWillHappen from '@/components/dashboard/WhatWillHappen';
import WhatShouldYouDo from '@/components/dashboard/WhatShouldYouDo';
import FileUploader from '@/components/upload/FileUploader';
import AIChatPanel from '@/components/chat/AIChatPanel';

export default function DashboardPage() {
  const [insights, setInsights] = useState(null);
  const [datasetId, setDatasetId] = useState(null);
  const [datasetName, setDatasetName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showUpload, setShowUpload] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [activeSection, setActiveSection] = useState('dashboard');

  // Load insights for a dataset
  const loadInsights = useCallback(async (id) => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getInsights(id);
      setInsights(data);
      setDatasetName(data.dataset_name || 'Your Data');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);

  // Handle successful upload
  const handleUploadSuccess = useCallback((result) => {
    setDatasetId(result.dataset_id);
    setShowUpload(false);
    loadInsights(result.dataset_id);
  }, [loadInsights]);

  // Check for existing datasets on mount
  useEffect(() => {
    const checkExisting = async () => {
      try {
        const { datasets } = await api.getDatasets();
        if (datasets && datasets.length > 0) {
          const latest = datasets[datasets.length - 1];
          setDatasetId(latest.id);
          loadInsights(latest.id);
        }
      } catch {
        // Backend not running — that's ok
      }
    };
    checkExisting();
  }, [loadInsights]);

  return (
    <div className="dashboard-layout">
      <Sidebar
        activeSection={activeSection}
        onNavigate={setActiveSection}
        onUploadClick={() => setShowUpload(true)}
      />

      <div className="dashboard-main">
        <Header
          datasetName={datasetName}
          onUploadClick={() => setShowUpload(true)}
          hasData={!!insights}
        />

        <div className="dashboard-content">
          {/* Error State */}
          {error && (
            <div className="glass-card animate-fade-in-up" style={{
              padding: 'var(--space-lg)',
              marginBottom: 'var(--space-xl)',
              borderColor: 'rgba(239, 68, 68, 0.2)',
              background: 'rgba(239, 68, 68, 0.05)',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                <span style={{ fontSize: '1.5rem' }}>⚠️</span>
                <div>
                  <div style={{ fontWeight: 600, marginBottom: '4px' }}>Something went wrong</div>
                  <div style={{ fontSize: '0.88rem', color: 'var(--text-secondary)' }}>{error}</div>
                </div>
              </div>
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="loader-wrapper animate-fade-in">
              <div className="loader-spinner" />
              <div className="loader-text">Analyzing your data with AI...</div>
            </div>
          )}

          {/* Empty State */}
          {!loading && !insights && !error && (
            <div className="empty-state animate-fade-in-up">
              <div className="empty-icon">📁</div>
              <h2 className="empty-title">Welcome to SmartPredict</h2>
              <p className="empty-desc">
                Upload your CSV or Excel file to get AI-powered insights, predictions, and recommendations for your business.
              </p>
              <button
                className="btn btn-primary btn-lg"
                onClick={() => setShowUpload(true)}
                id="upload-cta-btn"
              >
                📤 Upload Your Data
              </button>
            </div>
          )}

          {/* Dashboard Content */}
          {!loading && insights && (
            <>
              {/* Summary Banner */}
              {insights.summary && (
                <div className="summary-banner animate-fade-in-up">
                  <div className="summary-label">✨ AI Summary</div>
                  <div className="summary-text">{insights.summary}</div>
                </div>
              )}

              {/* KPI Cards */}
              <KPICards kpis={insights.kpis || []} />

              {/* What's Happening */}
              <WhatsHappening
                statements={insights.whats_happening || []}
                patterns={insights.patterns || []}
                risks={insights.risks || []}
              />

              {/* What Will Happen Next */}
              <WhatWillHappen trends={insights.trends || []} />

              {/* What Should You Do */}
              <WhatShouldYouDo recommendations={insights.recommendations || []} />
            </>
          )}
        </div>
      </div>

      {/* Upload Modal */}
      {showUpload && (
        <FileUploader
          onClose={() => setShowUpload(false)}
          onSuccess={handleUploadSuccess}
        />
      )}

      {/* AI Chat */}
      <AIChatPanel
        show={showChat}
        onToggle={() => setShowChat(!showChat)}
        datasetId={datasetId}
        hasData={!!insights}
      />
    </div>
  );
}
