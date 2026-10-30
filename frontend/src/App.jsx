import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import Dashboard from './pages/Dashboard';
import ActivityTracker from './pages/ActivityTracker';
import Analytics from './pages/Analytics';
import AICoach from './pages/AICoach';
import Reductions from './pages/Reductions';
import Leaderboard from './pages/Leaderboard';
import Settings from './pages/Settings';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [summary, setSummary] = useState(null);
  const [activities, setActivities] = useState([]);
  const [language, setLanguage] = useState('en');
  const [userName, setUserName] = useState('Student Pioneer');
  const [userGroup, setUserGroup] = useState('Hostel Krishna');
  const [quickLogOpen, setQuickLogOpen] = useState(false);

  // Fetch carbon data
  const fetchData = async () => {
    try {
      const [sumRes, actRes] = await Promise.all([
        fetch('/api/summary?session_id=default_user'),
        fetch('/api/activities?session_id=default_user')
      ]);

      if (sumRes.ok) {
        const sumData = await sumRes.json();
        setSummary(sumData);
      }
      if (actRes.ok) {
        const actData = await actRes.json();
        setActivities(actData.activities || []);
      }
    } catch (err) {
      console.warn('API fetch warning (is backend server running?):', err);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleActivityLogged = (data) => {
    fetchData();
  };

  return (
    <div className="app-container">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        summary={summary}
        userGroup={userGroup}
      />

      {/* Main Content Area */}
      <div className="main-content">
        <Header
          activeTab={activeTab}
          language={language}
          setLanguage={setLanguage}
          userName={userName}
          onOpenQuickLog={() => setActiveTab('tracker')}
          onRefresh={fetchData}
        />

        <main className="page-wrapper">
          {activeTab === 'dashboard' && (
            <Dashboard
              summary={summary}
              activities={activities}
              onNavigate={setActiveTab}
              onOpenQuickLog={() => setActiveTab('tracker')}
              userGroup={userGroup}
            />
          )}

          {activeTab === 'tracker' && (
            <ActivityTracker
              activities={activities}
              onActivityLogged={handleActivityLogged}
            />
          )}

          {activeTab === 'analytics' && (
            <Analytics
              summary={summary}
            />
          )}

          {activeTab === 'coach' && (
            <AICoach
              onActivityLogged={handleActivityLogged}
              language={language}
            />
          )}

          {activeTab === 'reductions' && (
            <Reductions
              summary={summary}
            />
          )}

          {activeTab === 'leaderboard' && (
            <Leaderboard
              userGroup={userGroup}
            />
          )}

          {activeTab === 'settings' && (
            <Settings
              userName={userName}
              setUserName={setUserName}
              userGroup={userGroup}
              setUserGroup={setUserGroup}
              language={language}
              setLanguage={setLanguage}
              onClearSession={fetchData}
            />
          )}
        </main>
      </div>
    </div>
  );
}
