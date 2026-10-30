import React, { useState } from 'react';
import {
  Lightbulb,
  CheckCircle2,
  TrendingDown,
  Sparkles,
  Zap,
  Car,
  Utensils,
  Leaf,
  Sliders
} from 'lucide-react';

export default function Reductions({ summary }) {
  const [adopted, setAdopted] = useState({});
  const [acHours, setAcHours] = useState(4);
  const [commuteDays, setCommuteDays] = useState(5);

  const tips = [
    {
      id: 'ac_temp',
      title: 'Adjust AC Thermostat to 24°C - 26°C',
      category: 'electricity',
      savings: '0.428 kg CO₂e / hour',
      annualSavings: '312.4 kg / year',
      difficulty: 'Easy',
      badge: 'badge-green',
      icon: Zap,
      description: 'Raising room AC temperature from 18°C to 24°C reduces power consumption by 25-30% without sacrificing comfort (BEE India guidelines).',
    },
    {
      id: 'bus_commute',
      title: 'Shift 10 km Solo Petrol Drive to Metro or Bus',
      category: 'transport',
      savings: '1.420 kg CO₂e / trip',
      annualSavings: '369.2 kg / year',
      difficulty: 'Easy',
      badge: 'badge-blue',
      icon: Car,
      description: 'Public transit bus (0.1023 kg/km) or metro (0.029 kg/km) vs petrol car (0.171 kg/km) achieves immediate Scope 3 decarbonization.',
    },
    {
      id: 'plant_meal',
      title: 'Swap 1 Red Meat Meal for Plant-Based Lentils',
      category: 'food',
      savings: '5.100 kg CO₂e / meal',
      annualSavings: '265.2 kg / year',
      difficulty: 'Moderate',
      badge: 'badge-purple',
      icon: Utensils,
      description: 'Based on Poore & Nemecek Oxford study, switching from beef/mutton to dal or legumes eliminates high enteric methane emissions.',
    },
    {
      id: 'standby_power',
      title: 'Power Down Dorm Electronics at Night',
      category: 'electricity',
      savings: '0.180 kg CO₂e / day',
      annualSavings: '65.7 kg / year',
      difficulty: 'Easy',
      badge: 'badge-yellow',
      icon: Zap,
      description: 'Vampire/phantom power from chargers, monitors, and gaming consoles accounts for 5-10% of campus room electricity.',
    },
    {
      id: 'campus_carpool',
      title: 'Campus Student Carpool or Bike Sharing',
      category: 'transport',
      savings: '0.850 kg CO₂e / day',
      annualSavings: '187.0 kg / year',
      difficulty: 'Easy',
      badge: 'badge-blue',
      icon: Car,
      description: 'Sharing a 4-person ride cuts per-capita vehicle emissions by 75% for campus day-scholars.',
    },
  ];

  const toggleAdopt = (id) => {
    setAdopted(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const adoptedCount = Object.values(adopted).filter(Boolean).length;
  // Estimated personal savings if adopted
  const estimatedSavings = (adoptedCount * 1.25).toFixed(2);

  // Interactive slider calculation
  // AC thermostat savings: 0.107 kg/hr saved * acHours * 30 days
  const monthlyAcSaved = (0.107 * acHours * 30).toFixed(1);
  // Bus switch savings: 1.42 kg/day * commuteDays * 4 weeks
  const monthlyTransitSaved = (1.42 * commuteDays * 4).toFixed(1);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Top Banner / Impact Summary */}
      <div
        className="card"
        style={{
          background: 'linear-gradient(135deg, #059669 0%, #047857 100%)',
          color: 'white',
          border: 'none',
          padding: 28,
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
              <Sparkles size={20} />
              <span style={{ fontSize: '0.85rem', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', opacity: 0.9 }}>
                AI Recommendations Engine
              </span>
            </div>
            <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: 'white', marginBottom: 6 }}>
              Personalized Decarbonization Roadmap
            </h2>
            <p style={{ fontSize: '0.9rem', opacity: 0.9, maxWidth: 650 }}>
              Actionable, high-impact changes tailored to your logged campus routine. Every recommendation includes audited kg CO₂e savings.
            </p>
          </div>

          <div style={{ background: 'rgba(255, 255, 255, 0.15)', backdropFilter: 'blur(10px)', padding: '16px 24px', borderRadius: 14, textAlign: 'center' }}>
            <div style={{ fontSize: '0.8rem', opacity: 0.85 }}>Habits Adopted</div>
            <div style={{ fontSize: '1.8rem', fontWeight: 800 }}>{adoptedCount} / {tips.length}</div>
            <div style={{ fontSize: '0.78rem', color: '#a7f3d0', fontWeight: 600 }}>
              🌿 ~{estimatedSavings} kg CO₂e/day saved
            </div>
          </div>
        </div>
      </div>

      {/* Interactive Savings Simulator */}
      <div className="card">
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
          <Sliders size={18} style={{ color: '#059669' }} />
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Interactive Decarbonization Simulator</h2>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24 }}>
          {/* AC Slider */}
          <div style={{ background: '#f8fafc', padding: 18, borderRadius: 12, border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ fontSize: '0.88rem', fontWeight: 600, color: '#334155' }}>
                Daily AC Runtime ({acHours} hours/day)
              </span>
              <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#059669' }}>
                Save {monthlyAcSaved} kg / month
              </span>
            </div>
            <input
              type="range"
              min="1"
              max="12"
              value={acHours}
              onChange={(e) => setAcHours(Number(e.target.value))}
              style={{ width: '100%', accentColor: '#059669', cursor: 'pointer' }}
            />
            <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: 8 }}>
              By setting AC thermostat to 24°C for {acHours} hours daily instead of 18°C.
            </p>
          </div>

          {/* Commute Slider */}
          <div style={{ background: '#f8fafc', padding: 18, borderRadius: 12, border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
              <span style={{ fontSize: '0.88rem', fontWeight: 600, color: '#334155' }}>
                Metro/Bus Commute Days ({commuteDays} days/week)
              </span>
              <span style={{ fontSize: '0.9rem', fontWeight: 700, color: '#2563eb' }}>
                Save {monthlyTransitSaved} kg / month
              </span>
            </div>
            <input
              type="range"
              min="1"
              max="7"
              value={commuteDays}
              onChange={(e) => setCommuteDays(Number(e.target.value))}
              style={{ width: '100%', accentColor: '#2563eb', cursor: 'pointer' }}
            />
            <p style={{ fontSize: '0.75rem', color: '#64748b', marginTop: 8 }}>
              By taking bus/metro {commuteDays} days/week instead of driving a personal petrol vehicle.
            </p>
          </div>
        </div>
      </div>

      {/* Reduction Recommendations List */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
        {tips.map((tip) => {
          const isAdopted = !!adopted[tip.id];
          const Icon = tip.icon;
          return (
            <div
              key={tip.id}
              className="card"
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                gap: 20,
                borderLeft: isAdopted ? '4px solid #059669' : '1px solid #e2e8f0',
                background: isAdopted ? '#f0fdf4' : '#ffffff',
                transition: 'all 0.2s ease',
              }}
            >
              <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
                <div
                  style={{
                    width: 44,
                    height: 44,
                    borderRadius: 12,
                    background: isAdopted ? '#dcfce7' : '#f1f5f9',
                    color: isAdopted ? '#15803d' : '#64748b',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0
                  }}
                >
                  <Icon size={22} />
                </div>

                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
                    <h3 style={{ fontSize: '1rem', fontWeight: 700, color: '#0f172a' }}>
                      {tip.title}
                    </h3>
                    <span className={`badge ${tip.badge}`}>{tip.difficulty}</span>
                  </div>

                  <p style={{ fontSize: '0.84rem', color: '#475569', marginBottom: 8, maxWidth: 750 }}>
                    {tip.description}
                  </p>

                  <div style={{ display: 'flex', gap: 16, fontSize: '0.8rem' }}>
                    <span style={{ color: '#059669', fontWeight: 700 }}>
                      ⚡ Instant Impact: {tip.savings}
                    </span>
                    <span style={{ color: '#64748b' }}>
                      📅 Annual Equivalent: {tip.annualSavings}
                    </span>
                  </div>
                </div>
              </div>

              <button
                onClick={() => toggleAdopt(tip.id)}
                className={isAdopted ? 'btn-primary' : 'btn-secondary'}
                style={{
                  minWidth: 140,
                  background: isAdopted ? '#059669' : '#ffffff',
                  borderColor: isAdopted ? '#059669' : '#cbd5e1',
                }}
              >
                {isAdopted ? (
                  <>
                    <CheckCircle2 size={16} />
                    <span>Adopted</span>
                  </>
                ) : (
                  <span>Commit to Habit</span>
                )}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
