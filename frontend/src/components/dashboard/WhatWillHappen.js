'use client';

import dynamic from 'next/dynamic';

// Dynamic import to avoid SSR issues with Recharts
const TrendChart = dynamic(() => import('./TrendChart'), { ssr: false });

export default function WhatWillHappen({ trends }) {
  if (!trends || trends.length === 0) return null;

  return (
    <div className="dashboard-section animate-fade-in-up delay-3">
      <div className="section-header">
        <div className="section-icon" style={{ background: 'rgba(139, 92, 246, 0.12)' }}>
          🔮
        </div>
        <div>
          <div className="section-title">What Will Happen Next?</div>
          <div className="section-subtitle">AI predictions based on your data trends</div>
        </div>
      </div>

      {/* Trend Summary Cards */}
      <div className="grid-3" style={{ marginBottom: 'var(--space-xl)' }}>
        {trends.slice(0, 3).map((trend, i) => (
          <div key={i} className="glass-card trend-summary">
            <div className="trend-direction">
              <span className={`trend-arrow ${trend.direction}`}>
                {trend.direction === 'up' ? '↑' : trend.direction === 'down' ? '↓' : '→'}
              </span>
              <span className={`trend-pct ${trend.direction}`}>
                {trend.direction === 'stable' ? '~0' : (trend.direction === 'up' ? '+' : '-')}{Math.abs(trend.change_percent)}%
              </span>
            </div>
            <div className="trend-name">{trend.friendly_name}</div>
            <div className="trend-desc">{trend.summary}</div>
            {trend.confidence > 0 && (
              <div style={{ marginTop: '8px' }}>
                <span className="badge badge-primary">
                  {trend.confidence > 70 ? '🎯 High' : trend.confidence > 40 ? '📊 Moderate' : '📉 Low'} confidence
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Trend Chart — Show the first trend with chart data */}
      {trends[0] && trends[0].chart_data && trends[0].chart_data.length > 0 && (
        <div className="glass-card chart-card">
          <div className="chart-title">
            📈 {trends[0].friendly_name} — Trend &amp; Forecast
          </div>
          <div className="chart-subtitle">
            Solid line = actual data &nbsp;|&nbsp; Dashed line = AI prediction
          </div>
          <TrendChart data={trends[0].chart_data} />
        </div>
      )}
    </div>
  );
}
