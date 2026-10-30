import React, { useState, useEffect } from 'react';
import {
  Trophy,
  Medal,
  Award,
  Users,
  TrendingDown,
  TreePine,
  Search,
  Sparkles,
  Building2
} from 'lucide-react';

export default function Leaderboard({ userGroup = 'Hostel Krishna' }) {
  const [leaderboard, setLeaderboard] = useState([]);
  const [filterType, setFilterType] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      const resp = await fetch('/api/campus');
      const data = await resp.json();
      setLeaderboard(data.leaderboard || []);
    } catch (err) {
      console.error('Failed to fetch campus leaderboard:', err);
      // Fallback seed data
      setLeaderboard([
        { rank: 1, name: "Hostel Krishna", total_kg: 142.5, members: 45, per_capita_kg: 3.17 },
        { rank: 2, name: "Computer Science Dept", total_kg: 210.0, members: 60, per_capita_kg: 3.50 },
        { rank: 3, name: "Hostel Cauvery", total_kg: 185.2, members: 48, per_capita_kg: 3.86 },
        { rank: 4, name: "Hostel Godavari", total_kg: 215.8, members: 52, per_capita_kg: 4.15 },
        { rank: 5, name: "ECE Dept", total_kg: 260.4, members: 55, per_capita_kg: 4.73 },
        { rank: 6, name: "Mechanical Dept", total_kg: 290.0, members: 50, per_capita_kg: 5.80 },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const filtered = leaderboard.filter(item => {
    if (filterType === 'hostels') return item.name.toLowerCase().includes('hostel');
    if (filterType === 'departments') return item.name.toLowerCase().includes('dept');
    return true;
  });

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Top Banner */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, #0f172a 0%, #1e293b 100%)',
          color: 'white',
          border: 'none',
          padding: 28,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
              <Trophy size={20} style={{ color: '#fbbf24' }} />
              <span style={{ fontSize: '0.85rem', fontWeight: 700, color: '#fbbf24', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                Campus Sustainability Challenge
              </span>
            </div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'white', marginBottom: 6 }}>
              Inter-Hostel & Department Green Standings
            </h2>
            <p style={{ fontSize: '0.88rem', color: '#94a3b8', maxWidth: 650 }}>
              Ranked by per-capita daily carbon footprint (kg CO₂e/person). Lower footprint means greener operations and higher ranking!
            </p>
          </div>

          <div style={{ display: 'flex', gap: 16 }}>
            <div style={{ background: 'rgba(255, 255, 255, 0.08)', padding: '14px 20px', borderRadius: 12, textAlign: 'center' }}>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Total Campus Offset</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#34d399' }}>1,103.9 kg</div>
            </div>
            <div style={{ background: 'rgba(255, 255, 255, 0.08)', padding: '14px 20px', borderRadius: 12, textAlign: 'center' }}>
              <div style={{ fontSize: '0.78rem', color: '#94a3b8' }}>Trees Equivalent</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#60a5fa' }}>51 Trees</div>
            </div>
          </div>
        </div>
      </div>

      {/* Leaderboard Table Card */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Live Sustainability Standings</h2>

          {/* Filter Pills */}
          <div style={{ display: 'flex', gap: 8 }}>
            {[
              { id: 'all', label: 'All Campus' },
              { id: 'hostels', label: 'Hostels Only' },
              { id: 'departments', label: 'Academic Depts' },
            ].map(tab => (
              <button
                key={tab.id}
                onClick={() => setFilterType(tab.id)}
                style={{
                  background: filterType === tab.id ? '#059669' : '#f1f5f9',
                  color: filterType === tab.id ? 'white' : '#475569',
                  border: 'none',
                  borderRadius: 8,
                  padding: '6px 14px',
                  fontSize: '0.82rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                {tab.label}
              </button>
            ))}
          </div>
        </div>

        <div style={{ overflowX: 'auto' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.9rem' }}>
            <thead>
              <tr style={{ borderBottom: '1px solid #e2e8f0', color: '#64748b', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                <th style={{ padding: '12px 16px' }}>Rank</th>
                <th style={{ padding: '12px 16px' }}>Group / Entity</th>
                <th style={{ padding: '12px 16px' }}>Community Members</th>
                <th style={{ padding: '12px 16px' }}>Total Emissions</th>
                <th style={{ padding: '12px 16px', textAlign: 'right' }}>Per Capita Footprint</th>
                <th style={{ padding: '12px 16px', textAlign: 'center' }}>Badge</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((item, idx) => {
                const isUserGroup = item.name.toLowerCase() === userGroup.toLowerCase();
                const rank = idx + 1;
                return (
                  <tr
                    key={idx}
                    style={{
                      borderBottom: '1px solid #f1f5f9',
                      background: isUserGroup ? '#f0fdf4' : 'transparent',
                      fontWeight: isUserGroup ? 700 : 500,
                    }}
                  >
                    <td style={{ padding: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                        {rank === 1 && <span style={{ fontSize: '1.2rem' }}>🥇</span>}
                        {rank === 2 && <span style={{ fontSize: '1.2rem' }}>🥈</span>}
                        {rank === 3 && <span style={{ fontSize: '1.2rem' }}>🥉</span>}
                        {rank > 3 && (
                          <span style={{ width: 24, height: 24, borderRadius: '50%', background: '#f1f5f9', color: '#64748b', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: '0.8rem', fontWeight: 700 }}>
                            {rank}
                          </span>
                        )}
                      </div>
                    </td>

                    <td style={{ padding: '16px' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                        <Building2 size={18} style={{ color: isUserGroup ? '#059669' : '#64748b' }} />
                        <div>
                          <div style={{ color: isUserGroup ? '#059669' : '#0f172a' }}>{item.name}</div>
                          {isUserGroup && (
                            <span style={{ fontSize: '0.7rem', color: '#059669', fontWeight: 700 }}>★ YOUR HOSTEL</span>
                          )}
                        </div>
                      </div>
                    </td>

                    <td style={{ padding: '16px', color: '#64748b' }}>
                      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                        <Users size={15} />
                        <span>{item.members} members</span>
                      </div>
                    </td>

                    <td style={{ padding: '16px', color: '#475569' }}>
                      {item.total_kg.toFixed(1)} kg CO₂e
                    </td>

                    <td style={{ padding: '16px', textAlign: 'right' }}>
                      <span style={{ fontSize: '1rem', fontWeight: 800, color: rank === 1 ? '#059669' : '#0f172a' }}>
                        {item.per_capita_kg.toFixed(2)}
                      </span>
                      <span style={{ fontSize: '0.75rem', color: '#64748b', marginLeft: 4 }}>kg / person</span>
                    </td>

                    <td style={{ padding: '16px', textAlign: 'center' }}>
                      {rank === 1 ? (
                        <span className="badge badge-green">🌿 Eco Champion</span>
                      ) : rank <= 3 ? (
                        <span className="badge badge-blue">⭐ Green Star</span>
                      ) : (
                        <span className="badge badge-slate">Participant</span>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
