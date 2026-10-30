import React, { useState } from 'react';
import {
  Car,
  Zap,
  Utensils,
  Trash2,
  Plus,
  CheckCircle2,
  Calculator,
  Info,
  Calendar,
  Filter
} from 'lucide-react';

export default function ActivityTracker({ activities, onActivityLogged }) {
  const [activeCategory, setActiveCategory] = useState('transport');
  const [submitting, setSubmitting] = useState(false);
  const [filterCat, setFilterCat] = useState('all');

  // Transport state
  const [transportMode, setTransportMode] = useState('bus');
  const [transportDistance, setTransportDistance] = useState(12);

  // Electricity state
  const [appliance, setAppliance] = useState('ac_1_5_ton');
  const [electricityHours, setElectricityHours] = useState(4);

  // Food state
  const [dietType, setDietType] = useState('vegetarian');
  const [foodItem, setFoodItem] = useState('Campus Veg Thali Meal');

  // Waste state
  const [wasteType, setWasteType] = useState('landfill_mixed');
  const [wasteWeight, setWasteWeight] = useState(1.5);

  // Real-time calculation previews based on official factors
  const calculatePreview = () => {
    if (activeCategory === 'transport') {
      const factors = {
        bus: 0.1023,
        train: 0.0355,
        metro: 0.0290,
        auto: 0.1150,
        petrol_car: 0.1710,
        diesel_car: 0.1710,
        ev_car: 0.0530,
        bike: 0.1030,
        flight_domestic: 0.2550,
      };
      const factor = factors[transportMode] || 0.1023;
      return (Number(transportDistance) * factor).toFixed(3);
    } else if (activeCategory === 'electricity') {
      const ratings = {
        ac_1_5_ton: 1.5,
        ac_1_ton: 1.0,
        fan: 0.075,
        led_bulb: 0.012,
        refrigerator: 0.15,
        laptop: 0.065,
        tv: 0.10,
        water_heater: 2.0,
      };
      const kw = ratings[appliance] || 1.5;
      const kwh = Number(electricityHours) * kw;
      return (kwh * 0.713).toFixed(3);
    } else if (activeCategory === 'food') {
      const foodFactors = {
        vegan: 2.0,
        vegetarian: 3.5,
        pescatarian: 4.5,
        mixed: 5.5,
        heavy_meat: 7.5,
      };
      // Single meal approx
      return ((foodFactors[dietType] || 3.5) / 3).toFixed(3);
    } else if (activeCategory === 'waste') {
      const wasteFactors = {
        landfill_mixed: 0.58,
        organic_composted: 0.05,
        plastic_recycled: -1.2,
        paper_recycled: -0.8,
      };
      return (Number(wasteWeight) * (wasteFactors[wasteType] || 0.58)).toFixed(3);
    }
    return '0.000';
  };

  const handleLogActivity = async (e) => {
    e.preventDefault();
    setSubmitting(true);

    let message = '';
    if (activeCategory === 'transport') {
      message = `I travelled ${transportDistance} km by ${transportMode}`;
    } else if (activeCategory === 'electricity') {
      const names = {
        ac_1_5_ton: '1.5 ton AC',
        fan: 'ceiling fan',
        led_bulb: 'LED bulb',
        refrigerator: 'refrigerator',
        laptop: 'laptop',
        tv: 'TV',
        water_heater: 'geyser/water heater'
      };
      message = `I used ${names[appliance] || appliance} for ${electricityHours} hours`;
    } else if (activeCategory === 'food') {
      message = `I had a ${dietType} meal: ${foodItem}`;
    } else if (activeCategory === 'waste') {
      message = `I disposed ${wasteWeight} kg of ${wasteType.replace('_', ' ')} waste`;
    }

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message, session_id: 'default_user' })
      });
      const data = await resp.json();
      if (onActivityLogged) onActivityLogged(data);
    } catch (err) {
      console.error('Failed to log activity:', err);
    } finally {
      setSubmitting(false);
    }
  };

  const filteredActivities = activities.filter(a =>
    filterCat === 'all' ? true : a.category === filterCat
  );

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Category Selection Tabs */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 16 }}>
        {[
          { id: 'transport', label: 'Transport', icon: Car, color: '#2563eb', bg: '#eff6ff', desc: 'DEFRA emission factors' },
          { id: 'electricity', label: 'Electricity', icon: Zap, color: '#ca8a04', bg: '#fefce8', desc: 'CEA India 0.713 kg/kWh' },
          { id: 'food', label: 'Food & Diet', icon: Utensils, color: '#db2777', bg: '#fdf2f8', desc: 'Poore & Nemecek Oxford' },
          { id: 'waste', label: 'Waste Management', icon: Trash2, color: '#059669', bg: '#f0fdf4', desc: 'EPA WARM factors' },
        ].map(cat => {
          const Icon = cat.icon;
          const isSel = activeCategory === cat.id;
          return (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              style={{
                background: isSel ? '#ffffff' : '#f8fafc',
                border: isSel ? `2px solid ${cat.color}` : '1px solid #e2e8f0',
                borderRadius: 14,
                padding: 16,
                textAlign: 'left',
                cursor: 'pointer',
                display: 'flex',
                flexDirection: 'column',
                gap: 8,
                boxShadow: isSel ? '0 4px 14px rgba(0,0,0,0.06)' : 'none',
                transition: 'all 0.15s ease'
              }}
            >
              <div style={{ width: 40, height: 40, borderRadius: 10, background: cat.bg, color: cat.color, display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Icon size={20} />
              </div>
              <div>
                <div style={{ fontSize: '0.95rem', fontWeight: 700, color: '#0f172a' }}>{cat.label}</div>
                <div style={{ fontSize: '0.72rem', color: '#64748b' }}>{cat.desc}</div>
              </div>
            </button>
          );
        })}
      </div>

      {/* Main Logging Form Card */}
      <div className="card">
        <form onSubmit={handleLogActivity} style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <h2 style={{ fontSize: '1.1rem', fontWeight: 700, textTransform: 'capitalize' }}>
                Log {activeCategory} Activity
              </h2>
              <p style={{ fontSize: '0.8rem', color: '#64748b' }}>
                Input your event metrics for deterministic scientific emission calculation
              </p>
            </div>
            {/* Live calculation pill */}
            <div style={{ background: '#f0fdf4', border: '1px solid #bbf7d0', borderRadius: 12, padding: '8px 16px', display: 'flex', alignItems: 'center', gap: 8 }}>
              <Calculator size={18} style={{ color: '#059669' }} />
              <div>
                <span style={{ fontSize: '0.75rem', color: '#64748b', display: 'block' }}>Calculated Impact</span>
                <span style={{ fontSize: '1.1rem', fontWeight: 800, color: '#059669' }}>
                  {calculatePreview()} <span style={{ fontSize: '0.75rem', fontWeight: 600 }}>kg CO₂e</span>
                </span>
              </div>
            </div>
          </div>

          {/* Dynamic Category Inputs */}
          {activeCategory === 'transport' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Transport Mode
                </label>
                <select
                  value={transportMode}
                  onChange={(e) => setTransportMode(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                >
                  <option value="bus">🚌 Public Bus (0.1023 kg/km)</option>
                  <option value="metro">🚇 Metro Rail (0.0290 kg/km)</option>
                  <option value="train">🚆 Indian Railways (0.0355 kg/km)</option>
                  <option value="auto">🛺 Auto Rickshaw (0.1150 kg/km)</option>
                  <option value="bike">🛵 Motorbike / Scooter (0.1030 kg/km)</option>
                  <option value="petrol_car">🚗 Petrol Car (0.1710 kg/km)</option>
                  <option value="diesel_car">🚙 Diesel Car (0.1710 kg/km)</option>
                  <option value="ev_car">⚡ Electric Car (0.0530 kg/km)</option>
                  <option value="flight_domestic">✈️ Flight Domestic (0.2550 kg/km)</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Distance Travelled (km)
                </label>
                <input
                  type="number"
                  min="0.1"
                  step="0.5"
                  value={transportDistance}
                  onChange={(e) => setTransportDistance(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                  required
                />
              </div>
            </div>
          )}

          {activeCategory === 'electricity' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Campus/Home Appliance
                </label>
                <select
                  value={appliance}
                  onChange={(e) => setAppliance(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                >
                  <option value="ac_1_5_ton">❄️ Air Conditioner 1.5 Ton (1.5 kW)</option>
                  <option value="ac_1_ton">❄️ Air Conditioner 1.0 Ton (1.0 kW)</option>
                  <option value="fan">🌀 Ceiling Fan (75 W)</option>
                  <option value="laptop">💻 Laptop Computer (65 W)</option>
                  <option value="refrigerator">🧊 Refrigerator (150 W)</option>
                  <option value="water_heater">🚿 Water Heater / Geyser (2.0 kW)</option>
                  <option value="led_bulb">💡 LED Room Light (12 W)</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Duration (Hours)
                </label>
                <input
                  type="number"
                  min="0.25"
                  step="0.5"
                  value={electricityHours}
                  onChange={(e) => setElectricityHours(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                  required
                />
              </div>
            </div>
          )}

          {activeCategory === 'food' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Diet Type
                </label>
                <select
                  value={dietType}
                  onChange={(e) => setDietType(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                >
                  <option value="vegetarian">🥗 Vegetarian (~1.17 kg/meal)</option>
                  <option value="vegan">🌱 100% Plant-Based Vegan (~0.67 kg/meal)</option>
                  <option value="pescatarian">🐟 Pescatarian (~1.50 kg/meal)</option>
                  <option value="mixed">🍗 Mixed Omnivore (~1.83 kg/meal)</option>
                  <option value="heavy_meat">🥩 High Red Meat (~2.50 kg/meal)</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Meal / Dish Name
                </label>
                <input
                  type="text"
                  value={foodItem}
                  onChange={(e) => setFoodItem(e.target.value)}
                  placeholder="e.g. Hostel Mess Lunch, Paneer Curry"
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                  required
                />
              </div>
            </div>
          )}

          {activeCategory === 'waste' && (
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20 }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Waste Stream
                </label>
                <select
                  value={wasteType}
                  onChange={(e) => setWasteType(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                >
                  <option value="landfill_mixed">🗑️ Landfill Mixed Waste (+0.58 kg/kg)</option>
                  <option value="organic_composted">🍂 Organic Compost (+0.05 kg/kg)</option>
                  <option value="plastic_recycled">♻️ Recycled Plastic (-1.2 kg credit/kg)</option>
                  <option value="paper_recycled">📄 Recycled Paper (-0.8 kg credit/kg)</option>
                </select>
              </div>
              <div>
                <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 600, color: '#334155', marginBottom: 6 }}>
                  Weight (kg)
                </label>
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={wasteWeight}
                  onChange={(e) => setWasteWeight(e.target.value)}
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 10, border: '1px solid #cbd5e1', fontSize: '0.9rem', outline: 'none' }}
                  required
                />
              </div>
            </div>
          )}

          <div style={{ display: 'flex', justifyContent: 'flex-end', gap: 12, marginTop: 10 }}>
            <button
              type="submit"
              disabled={submitting}
              className="btn-primary"
              style={{ minWidth: 160 }}
            >
              {submitting ? 'Recording...' : 'Record Activity'}
            </button>
          </div>
        </form>
      </div>

      {/* Activities Log History Table */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
          <div>
            <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Activity History Log</h2>
            <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Filter by scope or search verified events</p>
          </div>

          {/* Filter Pills */}
          <div style={{ display: 'flex', gap: 6 }}>
            {['all', 'transport', 'electricity', 'food', 'waste'].map(cat => (
              <button
                key={cat}
                onClick={() => setFilterCat(cat)}
                style={{
                  background: filterCat === cat ? '#059669' : '#f1f5f9',
                  color: filterCat === cat ? 'white' : '#475569',
                  border: 'none',
                  borderRadius: 8,
                  padding: '6px 12px',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  textTransform: 'capitalize'
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {filteredActivities.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '36px 0', color: '#64748b', fontSize: '0.88rem' }}>
            No activities found for this filter.
          </div>
        ) : (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '0.88rem' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid #e2e8f0', color: '#64748b', fontSize: '0.75rem', textTransform: 'uppercase' }}>
                  <th style={{ padding: '10px 12px' }}>Category</th>
                  <th style={{ padding: '10px 12px' }}>Activity Description</th>
                  <th style={{ padding: '10px 12px' }}>Timestamp</th>
                  <th style={{ padding: '10px 12px', textAlign: 'right' }}>Emissions (kg CO₂e)</th>
                </tr>
              </thead>
              <tbody>
                {filteredActivities.map((act, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                    <td style={{ padding: '12px' }}>
                      <span className={`badge ${
                        act.category === 'transport' ? 'badge-blue' :
                        act.category === 'electricity' ? 'badge-yellow' :
                        act.category === 'food' ? 'badge-purple' : 'badge-green'
                      }`}>
                        {act.category}
                      </span>
                    </td>
                    <td style={{ padding: '12px', fontWeight: 500, color: '#1e293b' }}>
                      {act.description}
                    </td>
                    <td style={{ padding: '12px', color: '#64748b', fontSize: '0.8rem' }}>
                      {act.timestamp ? new Date(act.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : 'Today'}
                    </td>
                    <td style={{ padding: '12px', textAlign: 'right', fontWeight: 700, color: '#0f172a' }}>
                      +{Number(act.emissions_kg).toFixed(3)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
