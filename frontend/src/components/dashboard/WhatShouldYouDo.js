'use client';

export default function WhatShouldYouDo({ recommendations }) {
  if (!recommendations || recommendations.length === 0) return null;

  const getCategoryStyle = (category) => {
    switch (category) {
      case 'opportunity':
        return { bg: 'rgba(16, 185, 129, 0.12)', border: 'rgba(16, 185, 129, 0.2)' };
      case 'warning':
        return { bg: 'rgba(245, 158, 11, 0.12)', border: 'rgba(245, 158, 11, 0.2)' };
      case 'action':
        return { bg: 'rgba(59, 130, 246, 0.12)', border: 'rgba(59, 130, 246, 0.2)' };
      default:
        return { bg: 'rgba(139, 92, 246, 0.12)', border: 'rgba(139, 92, 246, 0.2)' };
    }
  };

  const getImpactBadge = (impact) => {
    switch (impact) {
      case 'high':
        return { class: 'badge-red', text: '🔴 High Impact' };
      case 'medium':
        return { class: 'badge-amber', text: '🟡 Medium Impact' };
      case 'low':
        return { class: 'badge-blue', text: '🔵 Low Impact' };
      default:
        return { class: 'badge-blue', text: 'Impact: Unknown' };
    }
  };

  return (
    <div className="dashboard-section animate-fade-in-up delay-4">
      <div className="section-header">
        <div className="section-icon" style={{ background: 'rgba(16, 185, 129, 0.12)' }}>
          💡
        </div>
        <div>
          <div className="section-title">What Should You Do?</div>
          <div className="section-subtitle">AI-powered recommendations for your next steps</div>
        </div>
      </div>

      <div className="grid-2">
        {recommendations.slice(0, 6).map((rec, i) => {
          const style = getCategoryStyle(rec.category);
          const impact = getImpactBadge(rec.impact);

          return (
            <div
              key={i}
              className="glass-card rec-card"
              style={{ borderLeft: `3px solid ${style.border}` }}
            >
              <div className={`rec-icon ${rec.category}`}>
                {rec.icon || '💡'}
              </div>
              <div className="rec-content">
                <div className="rec-title">{rec.title}</div>
                <div className="rec-desc">{rec.description}</div>
                <div className="rec-impact">
                  <span className={`badge ${impact.class}`}>
                    {impact.text}
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
