import React, { useState } from 'react';
import {
  User,
  Building2,
  Target,
  Globe,
  Trash2,
  CheckCircle2,
  Save,
  AlertTriangle
} from 'lucide-react';

export default function Settings({
  userName,
  setUserName,
  userGroup,
  setUserGroup,
  language,
  setLanguage,
  onClearSession
}) {
  const [dailyTarget, setDailyTarget] = useState(4.0);
  const [unit, setUnit] = useState('kg');
  const [savedNotice, setSavedNotice] = useState(false);
  const [clearing, setClearing] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSavedNotice(true);
    setTimeout(() => setSavedNotice(false), 3000);
  };

  const handleClearActivities = async () => {
    if (!window.confirm('Are you sure you want to clear your logged session activities?')) return;
    try {
      setClearing(true);
      await fetch('/api/clear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: 'default_user' })
      });
      if (onClearSession) onClearSession();
      alert('Session activities cleared successfully.');
    } catch (err) {
      console.error('Failed to clear session:', err);
    } finally {
      setClearing(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24, maxWidth: 900 }}>
      {savedNotice && (
        <div style={{ background: '#dcfce7', border: '1px solid #86efac', color: '#15803d', padding: '12px 18px', borderRadius: 10, display: 'flex', alignItems: 'center', gap: 8, fontSize: '0.88rem', fontWeight: 600 }}>
          <CheckCircle2 size={18} />
          <span>Settings saved successfully!</span>
        </div>
      )}

      {/* Profile & Affiliation Card */}
      <div className="card">
        <h2 style={{ fontSize: '1.1rem', fontWeight: 700, marginBottom: 4 }}>User Profile & Campus Affiliation</h2>
        <p style={{ fontSize: '0.82rem', color: '#64748b', marginBottom: 20 }}>Configure your identity and hostel/department leaderboard grouping</p>

        <form onSubmit={handleSave} style={{ display: 'flex', flexDirection: 'column', gap: 18 }}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Display Name
              </label>
              <div style={{ position: 'relative' }}>
                <input
                  type="text"
                  value={userName}
                  onChange={(e) => setUserName(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                  required
                />
              </div>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Campus Hostel / Department
              </label>
              <select
                value={userGroup}
                onChange={(e) => setUserGroup(e.target.value)}
                style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
              >
                <option value="Hostel Krishna">Hostel Krishna</option>
                <option value="Hostel Godavari">Hostel Godavari</option>
                <option value="Hostel Cauvery">Hostel Cauvery</option>
                <option value="Computer Science Dept">Computer Science Dept</option>
                <option value="ECE Dept">ECE Dept</option>
                <option value="Mechanical Dept">Mechanical Dept</option>
              </select>
            </div>
          </div>

          {/* Daily Carbon Budget */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <label style={{ fontSize: '0.85rem', fontWeight: 600, color: '#334155' }}>
                Daily Carbon Target: <span style={{ color: '#059669', fontWeight: 700 }}>{dailyTarget} kg CO₂e / day</span>
              </label>
              <span style={{ fontSize: '0.8rem', color: '#64748b' }}>India Avg: 5.2 kg</span>
            </div>
            <input
              type="range"
              min="2.0"
              max="10.0"
              step="0.5"
              value={dailyTarget}
              onChange={(e) => setDailyTarget(Number(e.target.value))}
              style={{ width: '100%', accentColor: '#059669', cursor: 'pointer' }}
            />
          </div>

          {/* Language & Units */}
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Platform Language
              </label>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
              >
                <option value="en">🇬🇧 English</option>
                <option value="te">🇮🇳 తెలుగు (Telugu)</option>
                <option value="hi">🇮🇳 हिन्दी (Hindi)</option>
              </select>
            </div>

            <div>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                Measurement Units
              </label>
              <select
                value={unit}
                onChange={(e) => setUnit(e.target.value)}
                style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
              >
                <option value="kg">Metric (kg CO₂e, km, kWh)</option>
                <option value="lbs">Imperial (lbs CO₂e, miles, kWh)</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: 10 }}>
            <button type="submit" className="btn-primary" style={{ minWidth: 150 }}>
              <Save size={16} />
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      </div>

      {/* Danger Zone: Session Data Management */}
      <div className="card" style={{ border: '1px solid #fecaca', background: '#fffafb' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, color: '#dc2626', marginBottom: 6 }}>
          <AlertTriangle size={18} />
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700, color: '#dc2626' }}>Data Management & Reset</h2>
        </div>
        <p style={{ fontSize: '0.82rem', color: '#64748b', marginBottom: 16 }}>
          Clear all locally logged activities and restart your carbon session counter. Leaderboard seed records will remain intact.
        </p>

        <button
          onClick={handleClearActivities}
          disabled={clearing}
          className="btn-secondary"
          style={{ borderColor: '#fca5a5', color: '#dc2626' }}
        >
          <Trash2 size={16} />
          <span>{clearing ? 'Clearing...' : 'Reset All Session Activities'}</span>
        </button>
      </div>
    </div>
  );
}
