import React from 'react';
import {
  TrendingDown,
  Calendar,
  Zap,
  Car,
  PieChart as PieIcon,
  BarChart2,
  Layers,
  ArrowUpRight,
  ShieldCheck
} from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend
} from 'recharts';

export default function Analytics({ summary }) {
  // Weekly trend data
  const weeklyData = [
    { day: 'Mon', transport: 1.8, electricity: 2.1, food: 1.2, waste: 0.2, total: 5.3 },
    { day: 'Tue', transport: 1.2, electricity: 1.9, food: 1.0, waste: 0.1, total: 4.2 },
    { day: 'Wed', transport: 2.4, electricity: 2.5, food: 1.5, waste: 0.3, total: 6.7 },
    { day: 'Thu', transport: 0.8, electricity: 1.6, food: 0.9, waste: 0.1, total: 3.4 },
    { day: 'Fri', transport: 1.5, electricity: 2.2, food: 1.3, waste: 0.2, total: 5.2 },
    { day: 'Sat', transport: 0.4, electricity: 1.8, food: 1.1, waste: 0.2, total: 3.5 },
    { day: 'Sun', transport: 0.6, electricity: 1.7, food: 1.2, waste: 0.1, total: 3.6 },
  ];

  // Appliance electricity breakdown
  const applianceData = [
    { name: '1.5 Ton AC', kwh: 6.0, emissions: 4.28 },
    { name: 'Water Heater', kwh: 3.0, emissions: 2.14 },
    { name: 'Refrigerator', kwh: 2.4, emissions: 1.71 },
    { name: 'Ceiling Fan', kwh: 1.2, emissions: 0.86 },
    { name: 'Laptop / PC', kwh: 0.8, emissions: 0.57 },
  ];

  const totalKg = summary?.total_emissions_kg || 4.41;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* KPI Cards Row */}
      <div className="dashboard-grid-3">
        <div className="card stat-card">
          <div className="stat-header">
            <span className="stat-title">7-Day Moving Average</span>
            <div className="stat-icon primary">
              <TrendingDown size={22} />
            </div>
          </div>
          <div className="stat-value">
            4.56 <span>kg / day</span>
          </div>
          <div className="stat-delta good">
            <span>↓ 12.3% vs previous week</span>
          </div>
        </div>

        <div className="card stat-card">
          <div className="stat-header">
            <span className="stat-title">Peak Carbon Day</span>
            <div className="stat-icon" style={{ background: '#fef3c7', color: '#d97706' }}>
              <Calendar size={22} />
            </div>
          </div>
          <div className="stat-value">
            Wednesday <span>(6.7 kg)</span>
          </div>
          <div className="stat-delta neutral">
            <span>Higher travel & AC runtime</span>
          </div>
        </div>

        <div className="card stat-card">
          <div className="stat-header">
            <span className="stat-title">Net-Zero Progress</span>
            <div className="stat-icon" style={{ background: '#dcfce7', color: '#16a34a' }}>
              <ShieldCheck size={22} />
            </div>
          </div>
          <div className="stat-value" style={{ color: '#059669' }}>
            78.4%
          </div>
          <div className="stat-delta good">
            <span>On track for quarterly target</span>
          </div>
        </div>
      </div>

      {/* Main Weekly Trend Area Chart */}
      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
          <div>
            <h2 style={{ fontSize: '1.05rem', fontWeight: 700 }}>Weekly Emission Trajectory (kg CO₂e)</h2>
            <p style={{ fontSize: '0.8rem', color: '#64748b' }}>Daily carbon distribution across all 4 tracked activity scopes</p>
          </div>
          <div style={{ display: 'flex', gap: 8 }}>
            <span className="badge badge-green">Daily Target: 4.0 kg</span>
          </div>
        </div>

        <div style={{ height: 320, width: '100%' }}>
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={weeklyData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
              <defs>
                <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#059669" stopOpacity={0.4}/>
                  <stop offset="95%" stopColor="#059669" stopOpacity={0.0}/>
                </linearGradient>
                <linearGradient id="colorTransport" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2563eb" stopOpacity={0.3}/>
                  <stop offset="95%" stopColor="#2563eb" stopOpacity={0.0}/>
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
              <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} tickLine={false} />
              <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} unit=" kg" />
              <Tooltip
                contentStyle={{ borderRadius: 10, border: '1px solid #e2e8f0', boxShadow: '0 4px 14px rgba(0,0,0,0.06)' }}
              />
              <Legend verticalAlign="top" height={36} />
              <Area type="monotone" dataKey="total" name="Total Emissions" stroke="#059669" strokeWidth={2.5} fillOpacity={1} fill="url(#colorTotal)" />
              <Area type="monotone" dataKey="transport" name="Transport Scope" stroke="#2563eb" strokeWidth={1.8} fillOpacity={1} fill="url(#colorTransport)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Grid: Stacked Category Breakdown & Appliance Energy Distribution */}
      <div className="dashboard-grid-2">
        {/* Stacked Category Chart */}
        <div className="card">
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: 4 }}>Daily Category Share</h2>
          <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: 18 }}>Stacked comparison of emissions across the week</p>

          <div style={{ height: 260, width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                <XAxis dataKey="day" stroke="#94a3b8" fontSize={12} tickLine={false} />
                <YAxis stroke="#94a3b8" fontSize={12} tickLine={false} unit=" kg" />
                <Tooltip
                  contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0' }}
                />
                <Bar dataKey="transport" name="Transport" stackId="a" fill="#2563eb" radius={[0, 0, 0, 0]} />
                <Bar dataKey="electricity" name="Electricity" stackId="a" fill="#ca8a04" />
                <Bar dataKey="food" name="Food" stackId="a" fill="#db2777" />
                <Bar dataKey="waste" name="Waste" stackId="a" fill="#059669" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Appliance Electricity Chart */}
        <div className="card">
          <h2 style={{ fontSize: '1.05rem', fontWeight: 700, marginBottom: 4 }}>Appliance Carbon Footprint</h2>
          <p style={{ fontSize: '0.8rem', color: '#64748b', marginBottom: 18 }}>Grid electricity: CEA India 0.713 kg CO₂e / kWh</p>

          <div style={{ height: 260, width: '100%' }}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={applianceData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
                <XAxis type="number" stroke="#94a3b8" fontSize={12} tickLine={false} unit=" kg" />
                <YAxis dataKey="name" type="category" stroke="#64748b" fontSize={12} tickLine={false} width={110} />
                <Tooltip
                  formatter={(val) => [`${val} kg CO₂e`, 'Emissions']}
                  contentStyle={{ borderRadius: 8, border: '1px solid #e2e8f0' }}
                />
                <Bar dataKey="emissions" fill="#059669" radius={[0, 6, 6, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
