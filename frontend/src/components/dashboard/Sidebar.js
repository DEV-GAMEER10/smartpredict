'use client';

export default function Sidebar({ activeSection, onNavigate, onUploadClick }) {
  const navItems = [
    { id: 'dashboard', icon: '📊', label: 'Dashboard' },
    { id: 'upload', icon: '📤', label: 'Upload Data', action: onUploadClick },
    { id: 'history', icon: '📁', label: 'Datasets' },
    { id: 'settings', icon: '⚙️', label: 'Settings' },
  ];

  return (
    <aside className="dashboard-sidebar">
      {/* Brand */}
      <div className="sidebar-brand">
        <div className="sidebar-brand-icon">🧠</div>
        <span className="sidebar-brand-name">SmartPredict</span>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        {navItems.map((item) => (
          <button
            key={item.id}
            className={`sidebar-link ${activeSection === item.id ? 'active' : ''}`}
            onClick={() => {
              if (item.action) {
                item.action();
              } else {
                onNavigate(item.id);
              }
            }}
            id={`nav-${item.id}`}
          >
            <span className="sidebar-link-icon">{item.icon}</span>
            <span>{item.label}</span>
          </button>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <div className="sidebar-status">
          <div className="status-dot" />
          <span>AI Engine Active</span>
        </div>
      </div>
    </aside>
  );
}
