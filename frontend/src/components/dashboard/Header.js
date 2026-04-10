'use client';

export default function Header({ datasetName, onUploadClick, hasData }) {
  return (
    <header className="dashboard-header">
      <div>
        <h1 className="header-title">
          {hasData ? `Insights — ${datasetName}` : 'SmartPredict Dashboard'}
        </h1>
      </div>
      <div className="header-actions">
        {hasData && (
          <span className="badge badge-emerald">
            ✓ Data Loaded
          </span>
        )}
        <button
          className="btn btn-primary btn-sm"
          onClick={onUploadClick}
          id="header-upload-btn"
        >
          📤 {hasData ? 'New Data' : 'Upload Data'}
        </button>
      </div>
    </header>
  );
}
