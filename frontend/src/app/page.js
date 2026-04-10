'use client';

import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

export default function LandingPage() {
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  const particles = Array.from({ length: 20 }, (_, i) => ({
    id: i,
    left: `${Math.random() * 100}%`,
    top: `${Math.random() * 100}%`,
    delay: `${Math.random() * 5}s`,
    size: `${3 + Math.random() * 4}px`,
    opacity: 0.1 + Math.random() * 0.3,
  }));

  return (
    <div className="landing-page">
      {/* Background effects */}
      <div className="landing-bg" />
      <div className="landing-grid" />
      
      {/* Floating particles */}
      <div className="landing-particles">
        {mounted && particles.map((p) => (
          <div
            key={p.id}
            className="particle"
            style={{
              left: p.left,
              top: p.top,
              width: p.size,
              height: p.size,
              animationDelay: p.delay,
              opacity: p.opacity,
              background: p.id % 3 === 0 ? '#6366f1' : p.id % 3 === 1 ? '#8b5cf6' : '#10b981',
            }}
          />
        ))}
      </div>

      {/* Main content */}
      <div className="landing-content">
        <div className={`animate-fade-in-up ${mounted ? '' : ''}`}>
          <div style={{ fontSize: '3rem', marginBottom: '8px' }}>🧠</div>
          <h1 className="landing-logo">SmartPredict</h1>
          <p className="landing-tagline">
            Transform your raw data into clear insights, predictions, and actionable recommendations — no technical skills needed.
          </p>
        </div>

        <div className="landing-features animate-fade-in-up delay-2">
          <div className="landing-feature">
            <div className="landing-feature-icon">📊</div>
            <div className="landing-feature-text">Upload &amp; Analyze</div>
          </div>
          <div className="landing-feature">
            <div className="landing-feature-icon">🔮</div>
            <div className="landing-feature-text">Predict Trends</div>
          </div>
          <div className="landing-feature">
            <div className="landing-feature-icon">💡</div>
            <div className="landing-feature-text">Get Recommendations</div>
          </div>
        </div>

        <button
          className="btn btn-primary landing-cta animate-fade-in-up delay-3"
          onClick={() => router.push('/dashboard')}
          id="get-started-btn"
        >
          Get Started — It&apos;s Free
          <span style={{ fontSize: '1.2rem' }}>→</span>
        </button>

        <p className="animate-fade-in-up delay-4" style={{
          marginTop: '24px',
          fontSize: '0.82rem',
          color: 'var(--text-muted)',
        }}>
          No signup required. Just upload your CSV or Excel file.
        </p>
      </div>
    </div>
  );
}
