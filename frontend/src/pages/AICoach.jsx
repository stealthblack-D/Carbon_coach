import React, { useState, useRef, useEffect } from 'react';
import {
  Send,
  Bot,
  User,
  Sparkles,
  HelpCircle,
  Lightbulb,
  ShieldCheck,
  Zap,
  Globe
} from 'lucide-react';

export default function AICoach({ onActivityLogged, language = 'en' }) {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: language === 'te'
        ? "నమస్కారం! నేను మీ AI కార్బన్ కోచ్‌ని 🌱.\n\nవాతావరణ మార్పులు, పునరుత్పాదక శక్తి, మీ కళాశాలను గ్రీన్‌గా మార్చడం లేదా మీ కార్బన్ పాదముద్రను తగ్గించడం గురించి నన్ను అడగండి. లేదా మీ రోజువారీ ప్రయాణం మరియు విద్యుత్ వాడకం వివరాలు చెప్పండి, ఖచ్చితమైన ఉద్గారాలను లెక్కిస్తాను!"
        : language === 'hi'
        ? "नमस्ते! मैं आपका AI कार्बन कोच हूँ 🌱।\n\nमुझसे पर्यावरण, जलवायु परिवर्तन, सौर ऊर्जा, या कॉलेज सस्टेनेबिलिटी पर कोई भी प्रश्न पूछें। या अपनी दैनिक यात्रा और बिजली खपत बताएं, मैं आधिकारिक कारकों के आधार पर सटीक गणना करूँगा!"
        : "Hello! I am your AI Carbon Coach 🌱.\n\nAsk me general questions about climate change, carbon footprints, renewable energy, or campus sustainability—or tell me about your daily travel and electricity usage for verified emission tracking!",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const quickPrompts = [
    { label: "🌍 What is carbon footprint?", text: "What is carbon footprint?" },
    { label: "🌡️ Causes of climate change?", text: "What causes climate change?" },
    { label: "⚠️ Why are emissions harmful?", text: "Why are carbon emissions harmful?" },
    { label: "💡 How to reduce footprint?", text: "How can I reduce my carbon footprint?" },
    { label: "☀️ Explain renewable energy", text: "Explain renewable energy." },
    { label: "🏫 Sustainable college?", text: "How can my college become sustainable?" },
    { label: "🚌 12 km bus + 4h AC", text: "I travelled 12 km by bus today and used the AC for 4 hours" },
    { label: "🇮🇳 తెలుగు (కార్బన్ ఫుట్‌ప్రింట్)", text: "కార్బన్ ఫుట్‌ప్రింట్ అంటే ఏమిటి?" },
    { label: "🇮🇳 हिन्दी (जलवायु परिवर्तन)", text: "जलवायु परिवर्तन के मुख्य कारण क्या हैं?" },
  ];

  const handleSend = async (messageText) => {
    const textToSend = messageText || input;
    if (!textToSend.trim() || loading) return;

    const userMsg = {
      role: 'user',
      content: textToSend,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const resp = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: textToSend, session_id: 'default_user' })
      });
      const data = await resp.json();

      const assistantReply = data.response || data.reply || "Activity recorded successfully.";

      const assistantMsg = {
        role: 'assistant',
        content: assistantReply,
        intent: data.intent,
        verified: data.tool_calls && data.tool_calls.length > 0,
        emissions: data.emissions_kg,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => [...prev, assistantMsg]);
      if (onActivityLogged) onActivityLogged(data);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: 'Sorry, I encountered an issue connecting to the carbon engine. Please check if the backend server is active.',
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16, height: 'calc(100vh - 160px)' }}>
      {/* Quick Prompt Chips */}
      <div style={{ display: 'flex', gap: 8, overflowX: 'auto', paddingBottom: 4 }}>
        {quickPrompts.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q.text)}
            className="btn-secondary"
            style={{
              padding: '6px 12px',
              fontSize: '0.78rem',
              whiteSpace: 'nowrap',
              borderRadius: 20,
              background: '#ffffff',
            }}
          >
            <Sparkles size={13} style={{ color: '#059669' }} />
            <span>{q.label}</span>
          </button>
        ))}
      </div>

      {/* Chat Messages Container */}
      <div
        className="card"
        style={{
          flex: 1,
          display: 'flex',
          flexDirection: 'column',
          padding: 20,
          overflow: 'hidden',
          minHeight: 0,
        }}
      >
        <div style={{ flex: 1, overflowY: 'auto', paddingRight: 8, display: 'flex', flexDirection: 'column', gap: 16 }}>
          {messages.map((msg, idx) => {
            const isUser = msg.role === 'user';
            return (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  gap: 12,
                  alignSelf: isUser ? 'flex-end' : 'flex-start',
                  maxWidth: '85%',
                }}
              >
                {!isUser && (
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: 10,
                      background: 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
                      color: 'white',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0,
                      boxShadow: '0 2px 8px rgba(5,150,105,0.2)'
                    }}
                  >
                    <Bot size={20} />
                  </div>
                )}

                <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
                  <div
                    style={{
                      padding: '12px 18px',
                      borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
                      background: isUser ? '#059669' : '#f8fafc',
                      color: isUser ? '#ffffff' : '#1e293b',
                      border: isUser ? 'none' : '1px solid #e2e8f0',
                      fontSize: '0.92rem',
                      lineHeight: 1.6,
                      whiteSpace: 'pre-wrap',
                    }}
                  >
                    {msg.content}
                  </div>

                  {/* Clean verified indicator for calculations without technical jargon */}
                  {!isUser && msg.verified && (
                    <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, fontSize: '0.72rem', color: '#059669', fontWeight: 600 }}>
                      <ShieldCheck size={14} />
                      <span>Verified using official CEA India & DEFRA emission factors</span>
                    </div>
                  )}

                  <span style={{ fontSize: '0.7rem', color: '#94a3b8', alignSelf: isUser ? 'flex-end' : 'flex-start' }}>
                    {msg.timestamp}
                  </span>
                </div>

                {isUser && (
                  <div
                    style={{
                      width: 36,
                      height: 36,
                      borderRadius: 10,
                      background: '#e2e8f0',
                      color: '#475569',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}
                  >
                    <User size={18} />
                  </div>
                )}
              </div>
            );
          })}

          {loading && (
            <div style={{ display: 'flex', gap: 12, alignItems: 'center' }}>
              <div style={{ width: 36, height: 36, borderRadius: 10, background: '#059669', color: 'white', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <Bot size={20} />
              </div>
              <div style={{ background: '#f8fafc', border: '1px solid #e2e8f0', padding: '10px 16px', borderRadius: 12, fontSize: '0.85rem', color: '#64748b' }}>
                Thinking and preparing response...
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input Bar */}
        <form
          onSubmit={(e) => {
            e.preventDefault();
            handleSend();
          }}
          style={{ display: 'flex', gap: 10, marginTop: 14, paddingTop: 14, borderTop: '1px solid #f1f5f9' }}
        >
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask a sustainability question or log activities (e.g., '12 km by bus and 4h AC')..."
            style={{
              flex: 1,
              padding: '12px 18px',
              borderRadius: 12,
              border: '1px solid #cbd5e1',
              fontSize: '0.92rem',
              outline: 'none',
              background: '#f8fafc',
            }}
          />
          <button
            type="submit"
            disabled={loading || !input.trim()}
            className="btn-primary"
            style={{ borderRadius: 12, padding: '0 20px' }}
          >
            <Send size={18} />
            <span>Send</span>
          </button>
        </form>
      </div>
    </div>
  );
}
