import React from 'react';
import {
  LayoutDashboard,
  Activity,
  BarChart3,
  Bot,
  Lightbulb,
  Trophy,
  Settings as SettingsIcon,
  Leaf,
  ChevronRight,
  TrendingDown
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, summary, userGroup }) {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'tracker', label: 'Activity Tracker', icon: Activity },
    { id: 'analytics', label: 'Analytics', icon: BarChart3 },
    { id: 'coach', label: 'AI Carbon Coach', icon: Bot, badge: 'AI' },
    { id: 'reductions', label: 'Recommendations', icon: Lightbulb },
    { id: 'leaderboard', label: 'Leaderboard', icon: Trophy },
    { id: 'settings', label: 'Settings', icon: SettingsIcon },
  ];

  const totalKg = summary?.total_emissions_kg || 0;
  // Estimate trees needed to offset (1 tree absorbs ~21.77 kg CO2/year, ~0.06 kg/day)
  const treesNeeded = (totalKg / 21.77).toFixed(1);

  return (
    <aside className="sidebar">
      {/* Brand Header */}
      <div className="sidebar-brand">
        <div className="brand-icon-wrap">
          <Leaf size={22} strokeWidth={2.5} />
        </div>
        <div>
          <div className="brand-name">
            Carbon<span>Coach</span>
          </div>
        </div>
        <span className="brand-tag">SaaS</span>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        <div className="nav-section-title">Main Menu</div>
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={19} />
              <span style={{ flex: 1 }}>{item.label}</span>
              {item.badge && (
                <span
                  style={{
                    fontSize: '0.7rem',
                    background: '#059669',
                    color: 'white',
                    padding: '2px 6px',
                    borderRadius: '6px',
                    fontWeight: 700,
                  }}
                >
                  {item.badge}
                </span>
              )}
              {isActive && <ChevronRight size={16} style={{ color: '#059669' }} />}
            </button>
          );
        })}
      </nav>

      {/* Footer Info / Campus Footprint Pill */}
      <div className="sidebar-footer">
        <div className="sidebar-carbon-badge">
          <div
            style={{
              width: 38,
              height: 38,
              borderRadius: 10,
              background: '#dcfce7',
              color: '#15803d',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <TrendingDown size={20} />
          </div>
          <div style={{ flex: 1, minWidth: 0 }}>
            <div style={{ fontSize: '0.75rem', color: '#64748b', fontWeight: 600 }}>
              {userGroup || 'Hostel Krishna'}
            </div>
            <div style={{ fontSize: '0.92rem', fontWeight: 800, color: '#0f172a' }}>
              {totalKg.toFixed(1)} <span style={{ fontSize: '0.75rem', fontWeight: 500, color: '#64748b' }}>kg CO₂e</span>
            </div>
            <div style={{ fontSize: '0.7rem', color: '#059669', fontWeight: 600 }}>
              🌱 {treesNeeded} trees to offset
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
