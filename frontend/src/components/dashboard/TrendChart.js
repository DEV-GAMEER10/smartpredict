'use client';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload && payload.length) {
    return (
      <div style={{
        background: 'rgba(15, 15, 35, 0.95)',
        border: '1px solid rgba(255,255,255,0.1)',
        borderRadius: '12px',
        padding: '12px 16px',
        backdropFilter: 'blur(20px)',
        boxShadow: '0 8px 32px rgba(0,0,0,0.4)',
      }}>
        <div style={{ fontSize: '0.82rem', color: '#94a3b8', marginBottom: '6px' }}>
          {label}
        </div>
        {payload.map((item, i) => (
          item.value !== null && item.value !== undefined && (
            <div key={i} style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              fontSize: '0.88rem',
              color: item.color,
              fontWeight: 600,
            }}>
              <span style={{
                width: '8px',
                height: '8px',
                borderRadius: '50%',
                background: item.color,
              }} />
              {item.name}: {typeof item.value === 'number' ? item.value.toLocaleString() : item.value}
            </div>
          )
        ))}
      </div>
    );
  }
  return null;
};

export default function TrendChart({ data }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="chart-container">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 10, right: 30, left: 10, bottom: 0 }}>
          <defs>
            <linearGradient id="actualGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="predictedGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
            </linearGradient>
            <linearGradient id="boundsGradient" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.1} />
              <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            stroke="rgba(255,255,255,0.04)"
            vertical={false}
          />
          <XAxis
            dataKey="label"
            tick={{ fontSize: 11, fill: '#64748b' }}
            axisLine={{ stroke: 'rgba(255,255,255,0.06)' }}
            tickLine={false}
            interval="preserveStartEnd"
          />
          <YAxis
            tick={{ fontSize: 11, fill: '#64748b' }}
            axisLine={false}
            tickLine={false}
            tickFormatter={(v) => {
              if (v >= 1000000) return `${(v / 1000000).toFixed(1)}M`;
              if (v >= 1000) return `${(v / 1000).toFixed(0)}K`;
              return v;
            }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend
            wrapperStyle={{ fontSize: '0.8rem', color: '#94a3b8', paddingTop: '12px' }}
          />
          
          {/* Confidence bounds */}
          <Area
            type="monotone"
            dataKey="upper_bound"
            stroke="none"
            fill="url(#boundsGradient)"
            name="Upper Bound"
            dot={false}
            legendType="none"
          />
          <Area
            type="monotone"
            dataKey="lower_bound"
            stroke="none"
            fill="transparent"
            name="Lower Bound"
            dot={false}
            legendType="none"
          />
          
          {/* Actual data */}
          <Area
            type="monotone"
            dataKey="actual"
            stroke="#6366f1"
            strokeWidth={2.5}
            fill="url(#actualGradient)"
            name="Actual"
            dot={{ r: 3, fill: '#6366f1', strokeWidth: 0 }}
            activeDot={{ r: 5, fill: '#6366f1', stroke: '#fff', strokeWidth: 2 }}
            connectNulls={false}
          />
          
          {/* Predicted data */}
          <Area
            type="monotone"
            dataKey="predicted"
            stroke="#10b981"
            strokeWidth={2.5}
            strokeDasharray="8 4"
            fill="url(#predictedGradient)"
            name="Predicted"
            dot={{ r: 3, fill: '#10b981', strokeWidth: 0 }}
            activeDot={{ r: 5, fill: '#10b981', stroke: '#fff', strokeWidth: 2 }}
            connectNulls={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
