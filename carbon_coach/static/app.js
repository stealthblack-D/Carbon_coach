// app.js - Frontend reactivity for Carbon Coach

let sessionId = "session_" + Math.random().toString(36).substring(2, 9);
let currentLang = "en";
let categoryChart = null;

// DOM Elements
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const campusGroupSelect = document.getElementById("campusGroupSelect");
const clearBtn = document.getElementById("clearBtn");
const statTotalEmissions = document.getElementById("statTotalEmissions");
const statActivitiesCount = document.getElementById("statActivitiesCount");
const statBenchmarkStatus = document.getElementById("statBenchmarkStatus");
const leaderboardList = document.getElementById("leaderboardList");
const chartPlaceholder = document.getElementById("chartPlaceholder");

// Language buttons
const langEn = document.getElementById("langEn");
const langTe = document.getElementById("langTe");
const langHi = document.getElementById("langHi");

// Init
document.addEventListener("DOMContentLoaded", () => {
  initChart();
  refreshSummary();
  refreshLeaderboard();
  setupEventListeners();
});

function setupEventListeners() {
  chatForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = messageInput.value.trim();
    if (!text) return;
    messageInput.value = "";
    await sendMessage(text);
  });

  // Quick Chips
  document.querySelectorAll(".chip").forEach((chip) => {
    chip.addEventListener("click", () => {
      const prompt = chip.getAttribute("data-prompt");
      messageInput.value = prompt;
      messageInput.focus();
    });
  });

  // Language switcher
  langEn.addEventListener("click", () => setLanguage("en"));
  langTe.addEventListener("click", () => setLanguage("te"));
  langHi.addEventListener("click", () => setLanguage("hi"));

  // Clear Session
  clearBtn.addEventListener("click", async () => {
    if (confirm("Reset current carbon tracking session?")) {
      await fetch(`/api/clear?session_id=${sessionId}`, { method: "POST" });
      chatMessages.innerHTML = `
        <div class="flex items-start gap-3 chat-bubble-enter">
          <div class="w-8 h-8 rounded-full bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center text-sm">
            🌱
          </div>
          <div class="bg-slate-800 border border-slate-700/80 rounded-2xl rounded-tl-none p-3.5 max-w-[85%] text-sm leading-relaxed text-slate-200">
            <p class="font-semibold text-emerald-400 mb-1">Session Reset</p>
            <p>Your session history has been cleared. Ready to track new activities!</p>
          </div>
        </div>
      `;
      refreshSummary();
      refreshLeaderboard();
    }
  });

  campusGroupSelect.addEventListener("change", () => {
    refreshLeaderboard();
  });
}

function setLanguage(lang) {
  currentLang = lang;
  [langEn, langTe, langHi].forEach((btn) => {
    btn.classList.remove("bg-emerald-600", "text-white");
    btn.classList.add("text-slate-400");
  });
  if (lang === "en") {
    langEn.classList.add("bg-emerald-600", "text-white");
    messageInput.placeholder = "Describe your activities (e.g. 12 km by bus and 4 hrs AC)...";
  } else if (lang === "te") {
    langTe.classList.add("bg-emerald-600", "text-white");
    messageInput.placeholder = "మీ కార్యకలాపాలను తెలపండి (ఉదా: 12 కిమీ బస్సు మరియు 4 గంటల ఏసీ)...";
  } else if (lang === "hi") {
    langHi.classList.add("bg-emerald-600", "text-white");
    messageInput.placeholder = "अपनी गतिविधियाँ बताएं (जैसे: 12 किमी बस और 4 घंटे एसी)...";
  }
}

// Send Message to Agent API
async function sendMessage(text) {
  // Append user bubble
  appendUserMessage(text);

  // Append typing indicator
  const typingId = appendTypingIndicator();

  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: text,
        session_id: sessionId,
        campus_group: campusGroupSelect.value
      })
    });
    const data = await res.json();
    removeTypingIndicator(typingId);

    // Append agent response
    appendAgentResponse(data);

    // Refresh charts & leaderboard
    if (data.summary) {
      updateSummaryUI(data.summary);
    }
    refreshLeaderboard();
  } catch (err) {
    removeTypingIndicator(typingId);
    appendSystemError("Failed to communicate with Carbon Coach server.");
    console.error(err);
  }
}

function appendUserMessage(text) {
  const div = document.createElement("div");
  div.className = "flex justify-end chat-bubble-enter";
  div.innerHTML = `
    <div class="bg-emerald-600 text-white rounded-2xl rounded-tr-none px-4 py-2.5 max-w-[80%] text-sm shadow-md">
      ${escapeHtml(text)}
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendTypingIndicator() {
  const id = "typing_" + Date.now();
  const div = document.createElement("div");
  div.id = id;
  div.className = "flex items-start gap-3 chat-bubble-enter";
  div.innerHTML = `
    <div class="w-8 h-8 rounded-full bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center text-sm">
      🌱
    </div>
    <div class="bg-slate-800 border border-slate-700/80 rounded-2xl rounded-tl-none p-3 max-w-[80%] flex items-center gap-1.5">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce"></span>
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.2s]"></span>
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-bounce [animation-delay:0.4s]"></span>
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return id;
}

function removeTypingIndicator(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function appendAgentResponse(data) {
  const div = document.createElement("div");
  div.className = "flex items-start gap-3 chat-bubble-enter";

  // Build Tool Execution Inspector Accordion
  let toolInspectorHtml = "";
  if (data.tool_calls && data.tool_calls.length > 0) {
    const toolDetails = data.tool_calls.map((tc) => {
      const toolName = tc.tool;
      const argsStr = JSON.stringify(tc.args, null, 2);
      const resStr = JSON.stringify(tc.result, null, 2);
      return `
        <div class="p-2 bg-slate-900/80 rounded border border-slate-800 text-[11px] mb-2 font-mono">
          <div class="flex items-center justify-between text-emerald-400 font-bold mb-1">
            <span>⚙️ ${escapeHtml(toolName)}()</span>
          </div>
          <div class="text-slate-400 text-[10px] mb-1">Args: ${escapeHtml(argsStr)}</div>
          <div class="text-emerald-300 text-[10px]">Result: ${escapeHtml(resStr)}</div>
        </div>
      `;
    }).join("");

    toolInspectorHtml = `
      <details class="mt-3 pt-2 border-t border-slate-700/60 text-xs">
        <summary class="cursor-pointer text-slate-400 hover:text-emerald-400 transition font-medium flex items-center gap-1 select-none">
          <span>🔍 Inspect Verified Tool Executions (${data.tool_calls.length})</span>
        </summary>
        <div class="mt-2 space-y-1">
          ${toolDetails}
        </div>
      </details>
    `;
  }

  // Format markdown bolding & newlines
  const formattedReply = formatMarkdown(data.reply);

  div.innerHTML = `
    <div class="w-8 h-8 rounded-full bg-emerald-600/30 border border-emerald-500/40 flex items-center justify-center text-sm shrink-0">
      🌱
    </div>
    <div class="bg-slate-800 border border-slate-700/80 rounded-2xl rounded-tl-none p-4 max-w-[85%] text-sm leading-relaxed text-slate-200 shadow-md">
      <div>${formattedReply}</div>
      ${toolInspectorHtml}
    </div>
  `;

  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function appendSystemError(msg) {
  const div = document.createElement("div");
  div.className = "flex justify-center chat-bubble-enter";
  div.innerHTML = `
    <div class="bg-rose-900/40 border border-rose-500/40 text-rose-300 rounded-lg px-3 py-1.5 text-xs">
      ⚠️ ${escapeHtml(msg)}
    </div>
  `;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Refresh Summary & Category Chart
async function refreshSummary() {
  try {
    const res = await fetch(`/api/summary?session_id=${sessionId}&period=all`);
    const summary = await res.json();
    updateSummaryUI(summary);
  } catch (err) {
    console.error("Failed to fetch summary:", err);
  }
}

function updateSummaryUI(summary) {
  statTotalEmissions.textContent = summary.total_emissions_kg.toFixed(2);
  statActivitiesCount.textContent = `${summary.activity_count} activities logged`;

  // Compare against Paris target (5.50 kg)
  const target = 5.50;
  if (summary.total_emissions_kg > target) {
    statBenchmarkStatus.textContent = `Exceeds budget (+${(summary.total_emissions_kg - target).toFixed(2)} kg)`;
    statBenchmarkStatus.className = "text-[11px] text-amber-400 mt-1 block";
  } else {
    statBenchmarkStatus.textContent = `Within 1.5°C Paris budget 🌿`;
    statBenchmarkStatus.className = "text-[11px] text-emerald-400 mt-1 block";
  }

  // Update Donut Chart
  const categories = Object.keys(summary.by_category_kg || {});
  const values = Object.values(summary.by_category_kg || {});

  if (categories.length > 0) {
    chartPlaceholder.style.display = "none";
    categoryChart.data.labels = categories.map((c) => c.toUpperCase());
    categoryChart.data.datasets[0].data = values;
    categoryChart.update();
  } else {
    chartPlaceholder.style.display = "block";
    categoryChart.data.labels = [];
    categoryChart.data.datasets[0].data = [];
    categoryChart.update();
  }
}

// Refresh Campus Leaderboard
async function refreshLeaderboard() {
  try {
    const res = await fetch("/api/campus");
    const data = await res.json();
    renderLeaderboard(data.hostel_leaderboard || []);
  } catch (err) {
    console.error("Failed to fetch leaderboard:", err);
  }
}

function renderLeaderboard(hostels) {
  if (!hostels || hostels.length === 0) {
    leaderboardList.innerHTML = `<div class="text-slate-500 text-center py-2">No leaderboard data available</div>`;
    return;
  }

  const selectedGroup = campusGroupSelect.value;

  leaderboardList.innerHTML = hostels.map((h, i) => {
    const isSelected = h.name === selectedGroup;
    const rankMedal = i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${h.rank}`;
    return `
      <div class="flex items-center justify-between p-2 rounded-lg border transition ${
        isSelected
          ? "bg-emerald-950/40 border-emerald-500/50 shadow-sm"
          : "bg-slate-900/60 border-slate-800"
      }">
        <div class="flex items-center gap-2">
          <span class="text-sm font-bold w-6 text-center">${rankMedal}</span>
          <div>
            <div class="font-medium text-slate-200 ${isSelected ? "text-emerald-300 font-semibold" : ""}">
              ${escapeHtml(h.name)}
            </div>
            <div class="text-[10px] text-slate-400">${escapeHtml(h.badge)}</div>
          </div>
        </div>
        <div class="text-right">
          <span class="font-bold text-slate-100">${h.per_capita_kg}</span>
          <span class="text-[10px] text-slate-400 block">kg/person</span>
        </div>
      </div>
    `;
  }).join("");
}

// Chart.js initialization
function initChart() {
  const ctx = document.getElementById("categoryChart").getContext("2d");
  categoryChart = new Chart(ctx, {
    type: "doughnut",
    data: {
      labels: [],
      datasets: [
        {
          data: [],
          backgroundColor: [
            "#10b981", // Emerald (Travel)
            "#06b6d4", // Cyan (Electricity)
            "#f59e0b", // Amber (Food)
            "#8b5cf6", // Purple (Waste)
          ],
          borderWidth: 2,
          borderColor: "#0f172a"
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: {
          position: "bottom",
          labels: {
            color: "#94a3b8",
            font: { size: 10, family: "sans-serif" },
            boxWidth: 10,
            padding: 8
          }
        }
      },
      cutout: "70%"
    }
  });
}

function escapeHtml(str) {
  if (typeof str !== "string") return str;
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function formatMarkdown(text) {
  if (!text) return "";
  let res = escapeHtml(text);
  // Bold
  res = res.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");
  // Italics
  res = res.replace(/\*(.*?)\*/g, "<em>$1</em>");
  // Inline code
  res = res.replace(/`([^`]+)`/g, "<code class='bg-slate-900 px-1.5 py-0.5 rounded text-emerald-300 font-mono text-[11px]'>$1</code>");
  // Line breaks
  res = res.replace(/\n/g, "<br>");
  return res;
}
