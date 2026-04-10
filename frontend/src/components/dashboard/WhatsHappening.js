'use client';

export default function WhatsHappening({ statements, patterns, risks }) {
  const hasContent = (statements && statements.length > 0) || 
                     (patterns && patterns.length > 0) || 
                     (risks && risks.length > 0);

  if (!hasContent) return null;

  const bulletColors = ['blue', 'emerald', 'amber', 'blue', 'emerald'];

  return (
    <div className="dashboard-section animate-fade-in-up delay-2">
      <div className="section-header">
        <div className="section-icon" style={{ background: 'rgba(59, 130, 246, 0.12)' }}>
          👁️
        </div>
        <div>
          <div className="section-title">What&apos;s Happening?</div>
          <div className="section-subtitle">A snapshot of your current data</div>
        </div>
      </div>

      <div className="grid-2">
        {/* Current State */}
        <div className="glass-card section-card">
          <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 'var(--space-md)', color: 'var(--text-primary)' }}>
            📋 Current Overview
          </h4>
          <div className="insight-list">
            {statements.map((statement, i) => (
              <div key={i} className="insight-item">
                <div className={`insight-bullet ${bulletColors[i % bulletColors.length]}`} />
                <div className="insight-text">{statement}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Patterns & Risks */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--space-lg)' }}>
          {/* Patterns */}
          {patterns && patterns.length > 0 && (
            <div className="glass-card section-card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 'var(--space-md)', color: 'var(--text-primary)' }}>
                🔍 Patterns Found
              </h4>
              {patterns.slice(0, 3).map((pattern, i) => (
                <div key={i} className="glass-card pattern-card" style={{ marginBottom: i < patterns.length - 1 ? '8px' : 0 }}>
                  <div className={`pattern-type ${pattern.pattern_type}`}>
                    {pattern.pattern_type === 'correlation' && '🔗 Relationship'}
                    {pattern.pattern_type === 'cluster' && '🎯 Segments'}
                    {pattern.pattern_type === 'seasonal' && '🔄 Cycle'}
                  </div>
                  <div className="pattern-title">{pattern.title}</div>
                  <div className="pattern-desc">{pattern.description}</div>
                  <span className={`badge badge-${pattern.strength === 'strong' ? 'emerald' : 'amber'}`} style={{ marginTop: '8px' }}>
                    {pattern.strength} pattern
                  </span>
                </div>
              ))}
            </div>
          )}

          {/* Risks */}
          {risks && risks.length > 0 && (
            <div className="glass-card section-card">
              <h4 style={{ fontSize: '0.95rem', fontWeight: 600, marginBottom: 'var(--space-md)', color: 'var(--text-primary)' }}>
                ⚡ Areas to Watch
              </h4>
              {risks.slice(0, 3).map((risk, i) => (
                <div key={i} className="risk-card" style={{ padding: '12px 0', borderBottom: i < risks.length - 1 ? '1px solid var(--border-subtle)' : 'none' }}>
                  <div className={`risk-severity ${risk.severity}`} />
                  <div>
                    <div className="risk-title">{risk.title}</div>
                    <div className="risk-desc">{risk.description}</div>
                    <span className={`badge badge-${risk.severity === 'high' || risk.severity === 'critical' ? 'red' : 'amber'}`} style={{ marginTop: '6px' }}>
                      {risk.severity} priority
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
