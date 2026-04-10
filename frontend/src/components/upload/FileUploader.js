'use client';

import { useState, useRef, useCallback } from 'react';
import api from '@/lib/api';

export default function FileUploader({ onClose, onSuccess }) {
  const [dragover, setDragover] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [status, setStatus] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef(null);

  const validTypes = [
    'text/csv',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/vnd.ms-excel',
  ];

  const validExtensions = ['.csv', '.xlsx', '.xls'];

  const validateFile = (file) => {
    const ext = '.' + file.name.split('.').pop().toLowerCase();
    if (!validExtensions.includes(ext)) {
      return `Invalid file type "${ext}". Please upload CSV or Excel files.`;
    }
    if (file.size > 50 * 1024 * 1024) {
      return `File too large (${(file.size / 1024 / 1024).toFixed(1)}MB). Maximum is 50MB.`;
    }
    return null;
  };

  const processFile = useCallback(async (file) => {
    const validationError = validateFile(file);
    if (validationError) {
      setError(validationError);
      return;
    }

    setUploading(true);
    setProgress(0);
    setError('');
    setStatus('Uploading file...');

    try {
      setStatus('Uploading & processing...');
      const result = await api.uploadFile(file, (pct) => {
        setProgress(pct);
        if (pct < 100) {
          setStatus(`Uploading... ${pct}%`);
        } else {
          setStatus('Processing with AI... 🧠');
        }
      });

      setSuccess(true);
      setStatus(result.message || 'File processed successfully!');
      setProgress(100);

      // Delay slightly for the success animation
      setTimeout(() => {
        onSuccess(result);
      }, 1200);
    } catch (err) {
      setError(err.message);
      setUploading(false);
      setProgress(0);
      setStatus('');
    }
  }, [onSuccess]);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    setDragover(false);
    const file = e.dataTransfer.files[0];
    if (file) processFile(file);
  }, [processFile]);

  const handleFileSelect = useCallback((e) => {
    const file = e.target.files[0];
    if (file) processFile(file);
  }, [processFile]);

  return (
    <div className="upload-overlay" onClick={(e) => {
      if (e.target === e.currentTarget && !uploading) onClose();
    }}>
      <div className="glass-card-strong upload-modal">
        {/* Header */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: 'var(--space-xl)',
        }}>
          <div>
            <h2 style={{ fontSize: '1.3rem', fontWeight: 700 }}>Upload Your Data</h2>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-tertiary)', marginTop: '4px' }}>
              CSV or Excel files up to 50MB
            </p>
          </div>
          {!uploading && (
            <button
              className="btn btn-ghost btn-icon"
              onClick={onClose}
              id="upload-close-btn"
              style={{ fontSize: '1.3rem' }}
            >
              ✕
            </button>
          )}
        </div>

        {/* Drop Zone */}
        {!success && (
          <div
            className={`upload-zone ${dragover ? 'dragover' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragover(true); }}
            onDragLeave={() => setDragover(false)}
            onDrop={handleDrop}
            onClick={() => !uploading && fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".csv,.xlsx,.xls"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
              id="file-input"
            />
            
            <div className="upload-icon">
              {uploading ? '⏳' : dragover ? '📥' : '📁'}
            </div>
            <div className="upload-text">
              {uploading
                ? 'Processing your file...'
                : dragover
                  ? 'Drop your file here!'
                  : 'Drag & drop your file here, or click to browse'
              }
            </div>
            <div className="upload-hint">
              Supported: CSV, Excel (.xlsx, .xls)
            </div>
          </div>
        )}

        {/* Success State */}
        {success && (
          <div style={{ textAlign: 'center', padding: 'var(--space-xl)' }}>
            <div style={{ fontSize: '4rem', marginBottom: 'var(--space-md)' }}>✅</div>
            <div style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '8px' }}>
              Data Processed Successfully!
            </div>
            <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
              Redirecting to your insights...
            </div>
          </div>
        )}

        {/* Progress Bar */}
        {uploading && !success && (
          <div className="upload-progress">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progress}%` }}
              />
            </div>
            <div className="upload-status">{status}</div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div style={{
            marginTop: 'var(--space-md)',
            padding: 'var(--space-md)',
            borderRadius: 'var(--radius-md)',
            background: 'rgba(239, 68, 68, 0.1)',
            border: '1px solid rgba(239, 68, 68, 0.2)',
            fontSize: '0.88rem',
            color: 'var(--red-light)',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
          }}>
            <span>⚠️</span> {error}
          </div>
        )}
      </div>
    </div>
  );
}
