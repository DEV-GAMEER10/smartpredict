'use client';

export default function KPICards({ kpis }) {
  if (!kpis || kpis.length === 0) return null;

  const getColorClass = (color) => {
    const map = {
      emerald: 'emerald',
      green: 'emerald',
      blue: 'blue',
      violet: 'violet',
      purple: 'violet',
      amber: 'amber',
      yellow: 'amber',
      red: 'red',
    };
    return map[color] || 'blue';
  };

  return (
    <div className="dashboard-section">
      <div className="grid-kpi">
        {kpis.map((kpi, index) => {
          const colorClass = getColorClass(kpi.color);
          return (
            <div
              key={index}
              className={`glass-card kpi-card ${colorClass} animate-fade-in-up delay-${index + 1}`}
            >
              <div className="kpi-header">
                <div className={`kpi-icon ${colorClass}`}>
                  {kpi.icon || '📊'}
                </div>
                {kpi.change !== null && kpi.change !== undefined && (
                  <span className={`kpi-change ${kpi.direction || 'stable'}`}>
                    {kpi.direction === 'up' && '↑'}
                    {kpi.direction === 'down' && '↓'}
                    {kpi.direction === 'stable' && '→'}
                    {kpi.change !== null ? ` ${Math.abs(kpi.change)}%` : ''}
                  </span>
                )}
              </div>
              <div className="kpi-label">{kpi.label}</div>
              <div className="kpi-value">{kpi.value}</div>
              {kpi.direction && kpi.direction !== 'stable' && (
                <span className={`badge badge-${kpi.direction === 'up' ? 'emerald' : 'red'}`} style={{ marginTop: '4px' }}>
                  {kpi.direction === 'up' ? 'Trending Up' : 'Trending Down'}
                </span>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
