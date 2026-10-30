import React from 'react';
import {
  Globe,
  PlusCircle,
  Bell,
  RefreshCw,
  Search,
  Sparkles
} from 'lucide-react';

export default function Header({
  activeTab,
  onOpenQuickLog,
  language,
  setLanguage,
  userName = 'Campus Eco Pioneer',
  onRefresh
}) {
  const titles = {
    dashboard: { title: 'Executive Carbon Dashboard', subtitle: 'Real-time footprint monitoring, benchmark comparisons & analytics' },
    tracker: { title: 'Multi-Modal Activity Tracker', subtitle: 'Log transport, electricity, food, and waste using verified scientific factors' },
    analytics: { title: 'Carbon Analytics & Trends', subtitle: 'Weekly emissions distribution, category share & goal tracking' },
    coach: { title: 'AI Carbon Coach', subtitle: 'Interactive natural language coaching with instant tool calculations' },
    reductions: { title: 'Personalized Reduction Actions', subtitle: 'Quantified impact savings tailored to your lifestyle and campus habits' },
    leaderboard: { title: 'Campus Sustainability Leaderboard', subtitle: 'Inter-hostel and department green standings and rankings' },
    settings: { title: 'Platform & Profile Settings', subtitle: 'Configure campus affiliation, reduction goals, units & language' },
  };

  const current = titles[activeTab] || titles.dashboard;

  return (
    <header className="header">
      <div>
        <h1 style={{ fontSize: '1.25rem', fontWeight: 800, color: '#0f172a', letterSpacing: '-0.02em' }}>
          {current.title}
        </h1>
        <p style={{ fontSize: '0.8rem', color: '#64748b', marginTop: 1 }}>
          {current.subtitle}
        </p>
      </div>

      <div className="header-actions">
        {/* Quick Log Action Button */}
        <button
          className="btn-primary"
          onClick={onOpenQuickLog}
          style={{ padding: '8px 14px', fontSize: '0.85rem' }}
        >
          <PlusCircle size={16} />
          <span>Log Activity</span>
        </button>

        {/* Language selector */}
        <div style={{ position: 'relative' }}>
          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="lang-select-btn"
            style={{ outline: 'none' }}
          >
            <option value="en">🇬🇧 English</option>
            <option value="te">🇮🇳 తెలుగు (Telugu)</option>
            <option value="hi">🇮🇳 हिन्दी (Hindi)</option>
          </select>
        </div>

        {/* Refresh button */}
        {onRefresh && (
          <button
            onClick={onRefresh}
            title="Refresh Data"
            className="btn-secondary"
            style={{ padding: '8px 10px', borderRadius: 8 }}
          >
            <RefreshCw size={15} />
          </button>
        )}

        {/* User Profile */}
        <div className="user-profile-badge">
          <div className="avatar">
            {userName.slice(0, 2).toUpperCase()}
          </div>
          <div style={{ lineHeight: 1.2 }}>
            <div style={{ fontSize: '0.86rem', fontWeight: 700, color: '#0f172a' }}>
              {userName}
            </div>
            <div style={{ fontSize: '0.72rem', color: '#059669', fontWeight: 600 }}>
              🌿 Net-Zero Tier
            </div>
          </div>
        </div>
      </div>
    </header>
  );
}
