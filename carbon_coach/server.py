"""
server.py - FastAPI application for Carbon Coach.
Provides REST API endpoints, full-featured web dashboard, tool execution audit log,
and conversational reasoning powered by Google ADK with Gemini.
"""

import os
import re
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from carbon_coach.tools import (
    calculate_travel_emissions,
    calculate_electricity_emissions,
    calculate_food_emissions,
    calculate_waste_emissions,
    log_activity,
    get_summary,
    suggest_reductions,
    get_campus_leaderboard,
    compare_to_benchmark,
    CARBON_COACH_TOOLS
)
from carbon_coach.memory import memory_store
from carbon_coach.multilingual import detect_language, LANG_TE, LANG_HI, LANG_EN
from carbon_coach.knowledge import find_knowledge_topic
from carbon_coach.agent import run_agent_turn

app = FastAPI(
    title="DevFest 2026: Carbon Coach",
    description="AI Agent for measuring, understanding, and reducing carbon emissions.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Request Models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default_user"
    campus_group: str = "Hostel Cauvery"


class ActivityLogRequest(BaseModel):
    category: str
    description: str
    emissions_kg: float
    session_id: str = "default_user"
    campus_group: str = "Hostel Cauvery"


# ============================================================================
# CONVERSATIONAL REASONING & INTENT DISPATCH ENGINE
# ============================================================================
def process_conversational_message(message: str, session_id: str, campus_group: str) -> Dict[str, Any]:
    """
    Intelligently parses user intent:
      1. General Conceptual / Climate Questions -> Answered directly via knowledge base without tools.
      2. Follow-Up Queries -> Resolves context from recent conversation history.
      3. Campus Leaderboard -> Returns standings via get_campus_leaderboard().
      4. History & Summary -> Returns aggregation via get_summary().
      5. Specific Activity -> Calculates exact emissions via scientific tools and logs to memory.
      6. Greetings / Inquiries -> Conversational welcome and guidance.
    """
    lang = detect_language(message)
    msg_lower = message.lower().strip()

    # Record user message in conversational memory
    memory_store.add_chat_message(session_id=session_id, role="user", content=message)

    # ------------------------------------------------------------------------
    # 1. INTENT: General Sustainability, Climate & Environmental Education Questions
    # (Requirement 2 & 5: Answer directly without calling tools)
    # ------------------------------------------------------------------------
    knowledge_match = find_knowledge_topic(message)
    if knowledge_match:
        topic_key, topic_content = knowledge_match
        reply = topic_content.get(lang, topic_content[LANG_EN])

        memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
        return {
            "reply": reply,
            "response": reply,
            "tool_calls": [],
            "language": lang,
            "intent": "general_qa",
            "topic": topic_key,
            "summary": get_summary("all", session_id)
        }

    # ------------------------------------------------------------------------
    # 2. INTENT: Campus Leaderboard
    # ------------------------------------------------------------------------
    if any(k in msg_lower for k in ["leaderboard", "campus", "hostel", "department", "ర్యాంక్", "లీడర్‌బోర్డ్", "लीडरबोर्ड", "रैंक"]):
        board = get_campus_leaderboard()
        tool_calls = [{"tool": "get_campus_leaderboard", "args": {}, "result": board}]

        top_h = board.get("top_hostel", "Hostel Krishna")
        if lang == LANG_TE:
            reply = f"🏆 **క్యాంపస్ లీడర్‌బోర్డ్:** ప్రస్తుతం అత్యల్ప తలసరి ఉద్గారాలతో **{top_h}** అగ్రస్థానంలో ఉంది! మీ హాస్టల్ **{campus_group}** కూడా పోటీలో ఉంది."
        elif lang == LANG_HI:
            reply = f"🏆 **कैंपस लीडरबोर्ड:** सबसे कम प्रति व्यक्ति उत्सर्जन के साथ **{top_h}** शीर्ष पर है! आपका हॉस्टल **{campus_group}** भी अच्छा प्रयास कर रहा है।"
        else:
            reply = f"🏆 **Campus Leaderboard:** Currently, **{top_h}** leads the sustainability challenge with the lowest per capita emissions! Your group is registered as **{campus_group}**."

        memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
        return {
            "reply": reply,
            "response": reply,
            "tool_calls": tool_calls,
            "language": lang,
            "intent": "leaderboard",
            "summary": get_summary("all", session_id),
            "leaderboard": board
        }

    # ------------------------------------------------------------------------
    # 3. INTENT: Summary & Historical Trend Queries ("How did I do this week?")
    # ------------------------------------------------------------------------
    if any(k in msg_lower for k in ["how did i do", "summary", "total", "trend", "week", "ఈ వారం", "మొత్తం", "సమ్మరీ", "कुल", "इस हफ्ते", "history"]):
        period = "week" if any(w in msg_lower for w in ["week", "వారం", "हफ्ते"]) else "all"
        summary = get_summary(period=period, session_id=session_id)
        tool_calls = [{"tool": "get_summary", "args": {"period": period, "session_id": session_id}, "result": summary}]

        tot = summary["total_emissions_kg"]
        cnt = summary["activity_count"]
        cats = ", ".join(f"{k.title()}: {v} kg" for k, v in summary["by_category_kg"].items()) if summary["by_category_kg"] else "None yet"

        if lang == LANG_TE:
            reply = f"📊 **మీ కార్బన్ సారాంశం ({period}):**\n- మొత్తం నమోదైన కార్యకలాపాలు: {cnt}\n- మొత్తం ఉద్గారాలు: **{tot} kg CO₂e**\n- వర్గాల వారీగా: {cats}\n- జాతీయ సగటుతో పోలిక: {summary['benchmark_comparison']['status']}"
        elif lang == LANG_HI:
            reply = f"📊 **आपका कार्बन सारांश ({period}):**\n- कुल दर्ज गतिविधियाँ: {cnt}\n- कुल उत्सर्जन: **{tot} kg CO₂e**\n- श्रेणी अनुसार: {cats}\n- राष्ट्रीय औसत से तुलना: {summary['benchmark_comparison']['status']}"
        else:
            reply = (
                f"📊 **Your Carbon Summary ({period.title()}):**\n\n"
                f"• **Total Footprint:** **{tot} kg CO₂e** across {cnt} recorded activities.\n"
                f"• **Scope Distribution:** {cats}\n"
                f"• **Benchmark Comparison:** {summary['benchmark_comparison']['status']}.\n\n"
                f"💡 *Keep logging to monitor your weekly decarbonization progress!*"
            )

        memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
        return {
            "reply": reply,
            "response": reply,
            "tool_calls": tool_calls,
            "language": lang,
            "intent": "summary",
            "summary": summary
        }

    # ------------------------------------------------------------------------
    # 4. INTENT: Contextual Follow-up (e.g., "What if I took metro instead?")
    # ------------------------------------------------------------------------
    follow_up_triggers = ["what if", "instead", "what about", "how about", "వేరే", "बदले में", "अगर मैं"]
    if any(t in msg_lower for t in follow_up_triggers):
        recent_acts = memory_store.get_activities(session_id=session_id, period="all")
        # Find the most recent travel activity to provide comparative savings
        recent_travel = next((a for a in recent_acts if a["category"] == "travel"), None)

        if recent_travel:
            # Detect alternative mode
            alt_mode = None
            if "metro" in msg_lower or "మెట్రో" in msg_lower or "मेट्रो" in msg_lower:
                alt_mode = "metro"
            elif "bus" in msg_lower or "బస్సు" in msg_lower or "बस" in msg_lower:
                alt_mode = "bus"
            elif "train" in msg_lower or "రైలు" in msg_lower or "ट्रेन" in msg_lower:
                alt_mode = "train"
            elif "walk" in msg_lower or "నడక" in msg_lower or "पैदल" in msg_lower:
                alt_mode = "walking"
            elif "bike" in msg_lower or "cycle" in msg_lower or "సైకిల్" in msg_lower:
                alt_mode = "bicycle"
            elif "car" in msg_lower:
                alt_mode = "car"

            if alt_mode:
                # Extract km from recent activity description
                km_m = re.search(r'(\d+(?:\.\d+)?)\s*km', recent_travel["description"])
                recent_km = float(km_m.group(1)) if km_m else 10.0

                alt_calc = calculate_travel_emissions(mode=alt_mode, km=recent_km)
                prev_emissions = recent_travel["emissions_kg"]
                new_emissions = alt_calc["emissions_kg"]
                diff = round(prev_emissions - new_emissions, 3)

                tool_calls = [{"tool": "calculate_travel_emissions", "args": {"mode": alt_mode, "km": recent_km}, "result": alt_calc}]

                if diff > 0:
                    reply = (
                        f"🌱 **Great follow-up comparison!**\n\n"
                        f"If you travelled those **{recent_km} km** by **{alt_mode.title()}** instead of your previous trip, your emissions would drop to **{new_emissions} kg CO₂e**.\n\n"
                        f"✨ **Net Carbon Saved:** **{diff} kg CO₂e** per trip!\n"
                        f"Over a 30-day month, that habit alone slashes **{round(diff * 30, 1)} kg CO₂e** from your footprint."
                    )
                else:
                    reply = (
                        f"ℹ️ **Mode Comparison for {recent_km} km:**\n\n"
                        f"Travelling by **{alt_mode.title()}** would generate **{new_emissions} kg CO₂e** compared to your recorded **{prev_emissions} kg CO₂e**.\n"
                        f"Public transit (bus/metro) or active commuting remains the greenest choice!"
                    )

                memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
                return {
                    "reply": reply,
                    "response": reply,
                    "tool_calls": tool_calls,
                    "language": lang,
                    "intent": "follow_up",
                    "summary": get_summary("all", session_id)
                }

    # ------------------------------------------------------------------------
    # 5. INTENT: Specific Activity Calculation & Logging (Tools Required)
    # ------------------------------------------------------------------------
    tool_calls = []
    emissions_found = []
    actions_taken = []

    # A. Travel Detection (must have km or clear distance)
    km_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kms|kilometers|కిమీ|किमी)', message, re.IGNORECASE)
    dist_km = float(km_match.group(1)) if km_match else None

    travel_mode = None
    if any(w in msg_lower for w in ["bus", "బస్సు", "बस", "rtc"]):
        travel_mode = "bus"
    elif any(w in msg_lower for w in ["train", "rail", "రైలు", "ट्रेन"]):
        travel_mode = "train"
    elif any(w in msg_lower for w in ["metro", "మెట్రో", "मेट्रो"]):
        travel_mode = "metro"
    elif any(w in msg_lower for w in ["bike", "motorcycle", "scooter", "బైక్", "बाइक", "स्कूटर"]):
        travel_mode = "bike"
    elif any(w in msg_lower for w in ["car", "cab", "taxi", "కారు", "कार", "कैब"]):
        travel_mode = "car"
    elif any(w in msg_lower for w in ["auto", "rickshaw", "ఆటో", "ऑटो"]):
        travel_mode = "auto"
    elif any(w in msg_lower for w in ["walk", "walking", "నడక", "पैदल"]):
        travel_mode = "walking"
    elif any(w in msg_lower for w in ["cycle", "bicycle", "సైకిల్", "साइकिल"]):
        travel_mode = "bicycle"

    if travel_mode and dist_km:
        t_res = calculate_travel_emissions(mode=travel_mode, km=dist_km)
        tool_calls.append({"tool": "calculate_travel_emissions", "args": {"mode": travel_mode, "km": dist_km}, "result": t_res})
        emissions_found.append(t_res)

        desc = f"{dist_km} km by {travel_mode}"
        l_res = log_activity("travel", desc, t_res["emissions_kg"], session_id, campus_group)
        tool_calls.append({"tool": "log_activity", "args": {"category": "travel", "description": desc, "emissions_kg": t_res["emissions_kg"]}, "result": l_res})
        actions_taken.append(f"Logged {desc}: {t_res['emissions_kg']} kg CO₂e")

    # B. Electricity Detection (must have hours or kWh)
    hours_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hour|hours|hrs|hr|గంటలు|గంట|घंटे|घंटा)', message, re.IGNORECASE)
    hours = float(hours_match.group(1)) if hours_match else None

    kwh_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kwh|units|యూనిట్లు|यूनिट)', message, re.IGNORECASE)
    kwh = float(kwh_match.group(1)) if kwh_match else None

    appliance = None
    if any(w in msg_lower for w in ["ac", "air conditioner", "ఏసీ", "ఎయిర్ కండీషనర్", "एसी"]):
        appliance = "ac"
    elif any(w in msg_lower for w in ["fan", "ఫ్యాన్", "पंखा"]):
        appliance = "fan"
    elif any(w in msg_lower for w in ["laptop", "computer", "ల్యాప్‌టాప్", "लैपटॉप"]):
        appliance = "laptop"
    elif any(w in msg_lower for w in ["geyser", "water heater", "గీజర్", "गीज़र"]):
        appliance = "geyser"
    elif any(w in msg_lower for w in ["tv", "television", "టీవీ"]):
        appliance = "tv"

    if kwh:
        e_res = calculate_electricity_emissions(kwh=kwh)
        tool_calls.append({"tool": "calculate_electricity_emissions", "args": {"kwh": kwh}, "result": e_res})
        emissions_found.append(e_res)
        desc = f"{kwh} kWh electricity"
        l_res = log_activity("electricity", desc, e_res["emissions_kg"], session_id, campus_group)
        tool_calls.append({"tool": "log_activity", "args": {"category": "electricity", "description": desc, "emissions_kg": e_res["emissions_kg"]}, "result": l_res})
        actions_taken.append(f"Logged {desc}: {e_res['emissions_kg']} kg CO₂e")
    elif appliance and hours:
        e_res = calculate_electricity_emissions(appliance=appliance, hours=hours)
        tool_calls.append({"tool": "calculate_electricity_emissions", "args": {"appliance": appliance, "hours": hours}, "result": e_res})
        emissions_found.append(e_res)
        desc = f"{appliance.upper()} for {hours} hours"
        l_res = log_activity("electricity", desc, e_res["emissions_kg"], session_id, campus_group)
        tool_calls.append({"tool": "log_activity", "args": {"category": "electricity", "description": desc, "emissions_kg": e_res["emissions_kg"]}, "result": l_res})
        actions_taken.append(f"Logged {desc}: {e_res['emissions_kg']} kg CO₂e")

    # C. Food Activity (only if explicitly mentioning having a meal)
    if any(w in msg_lower for w in ["ate", "had", "eating", "lunch", "dinner", "breakfast", "భోజనం", "తిన్నాను", "खाया", "भोजन"]) and \
       any(w in msg_lower for w in ["chicken", "mutton", "veg", "vegetarian", "vegan", "thali", "biryani", "చికెన్", "चिकन"]):
        meal_type = "chicken" if any(w in msg_lower for w in ["chicken", "biryani", "చికెన్", "चिकन", "mutton"]) else "vegetarian"
        f_res = calculate_food_emissions(meal_type=meal_type, meals_count=1)
        tool_calls.append({"tool": "calculate_food_emissions", "args": {"meal_type": meal_type, "meals_count": 1}, "result": f_res})
        emissions_found.append(f_res)
        desc = f"1 {meal_type} meal"
        l_res = log_activity("food", desc, f_res["emissions_kg"], session_id, campus_group)
        tool_calls.append({"tool": "log_activity", "args": {"category": "food", "description": desc, "emissions_kg": f_res["emissions_kg"]}, "result": l_res})
        actions_taken.append(f"Logged {desc}: {f_res['emissions_kg']} kg CO₂e")

    # D. Waste Activity (must have kg or clear disposal action)
    if any(w in msg_lower for w in ["disposed", "threw", "recycled", "waste", "trash", "వ్యర్థాలు", "చెత్త", "कचरा"]) and \
       any(w in msg_lower for w in ["kg", "kilo", "plastic", "organic", "food waste", "కిలో", "किलो"]):
        w_kg_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:kg|kilo|కిలో|किलो)', message, re.IGNORECASE)
        w_kg = float(w_kg_match.group(1)) if w_kg_match else 1.0
        recycled = any(w in msg_lower for w in ["recycle", "recycled", "రీసైకిల్", "रीसाइकिल", "compost"])
        w_type = "plastic" if "plastic" in msg_lower else "organic_food"

        w_res = calculate_waste_emissions(waste_type=w_type, kg=w_kg, recycled=recycled)
        tool_calls.append({"tool": "calculate_waste_emissions", "args": {"waste_type": w_type, "kg": w_kg, "recycled": recycled}, "result": w_res})
        emissions_found.append(w_res)
        desc = f"{w_kg} kg {w_type} ({'recycled' if recycled else 'landfill'})"
        l_res = log_activity("waste", desc, w_res["emissions_kg"], session_id, campus_group)
        tool_calls.append({"tool": "log_activity", "args": {"category": "waste", "description": desc, "emissions_kg": w_res["emissions_kg"]}, "result": l_res})
        actions_taken.append(f"Logged {desc}: {w_res['emissions_kg']} kg CO₂e")

    # If any specific activity emissions were calculated
    if emissions_found:
        total_msg_emissions = round(sum(e["emissions_kg"] for e in emissions_found), 4)

        highest_cat = emissions_found[0]["category"]
        red_res = suggest_reductions(highest_category=highest_cat, current_emissions_kg=total_msg_emissions)
        tool_calls.append({"tool": "suggest_reductions", "args": {"highest_category": highest_cat, "current_emissions_kg": total_msg_emissions}, "result": red_res})

        bench_res = compare_to_benchmark(total_msg_emissions, period="day")
        tool_calls.append({"tool": "compare_to_benchmark", "args": {"emissions_kg": total_msg_emissions, "period": "day"}, "result": bench_res})

        summary = get_summary(period="all", session_id=session_id)

        tip1 = red_res["suggestions"][0]
        saving_val = tip1.get('estimated_saving_kg_co2e_per_day') or tip1.get('estimated_saving_kg_co2e_per_trip') or 0.42

        breakdown_lines = []
        for e in emissions_found:
            cat = e["category"].title()
            val = e["emissions_kg"]
            src = e.get("source", "")
            breakdown_lines.append(f"• **{cat}:** `{val} kg CO₂e` *(Factor source: {src})*")
        breakdown_str = "\n".join(breakdown_lines)

        if lang == LANG_TE:
            reply = (
                f"✅ **మీ కార్యకలాపాలు విజయవంతంగా నమోదయ్యాయి!**\n\n"
                f"{breakdown_str}\n\n"
                f"🔹 **ఈ నమోదు మొత్తం:** **{total_msg_emissions} kg CO₂e**\n"
                f"🔹 **మీ మొత్తం సెషన్ ఉద్గారాలు:** **{summary['total_emissions_kg']} kg CO₂e** ({campus_group} కి జోడించబడింది)\n\n"
                f"📊 **పోలిక:** భారత జాతీయ రోజువారీ సగటు ~5.2 kg CO₂e. మీ ప్రభావం: {bench_res['status']}.\n\n"
                f"💡 **చిట్కా:** {tip1['action']} (ఆదా: ~{saving_val} kg CO₂e)."
            )
        elif lang == LANG_HI:
            reply = (
                f"✅ **आपकी गतिविधियां सफलतापूर्वक दर्ज कर ली गई हैं!**\n\n"
                f"{breakdown_str}\n\n"
                f"🔹 **इस गतिविधि का कुल उत्सर्जन:** **{total_msg_emissions} kg CO₂e**\n"
                f"🔹 **सत्र का कुल उत्सर्जन:** **{summary['total_emissions_kg']} kg CO₂e** ({campus_group} में जोड़ा गया)\n\n"
                f"📊 **तुलना:** भारतीय राष्ट्रीय दैनिक औसत ~5.2 kg CO₂e है। आपका स्तर: {bench_res['status']}.\n\n"
                f"💡 **सुझाव:** {tip1['action']} (बचत: ~{saving_val} kg CO₂e)।"
            )
        else:
            reply = (
                f"✅ **Activities Tracked & Verified!**\n\n"
                f"{breakdown_str}\n\n"
                f"🔹 **Activity Footprint:** **{total_msg_emissions} kg CO₂e**\n"
                f"🔹 **Session Total:** **{summary['total_emissions_kg']} kg CO₂e** (Credited to {campus_group})\n\n"
                f"📊 **National Benchmark:** Indian daily average is ~5.2 kg CO₂e/day. Today's footprint is: {bench_res['status']}.\n\n"
                f"💡 **Coach Recommendation:** {tip1['action']} (Saves ~{saving_val} kg CO₂e)."
            )

        memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
        return {
            "reply": reply,
            "response": reply,
            "tool_calls": tool_calls,
            "emissions_kg": total_msg_emissions,
            "session_total_kg": summary["total_emissions_kg"],
            "language": lang,
            "intent": "activity_calculation",
            "summary": summary
        }

    # ------------------------------------------------------------------------
    # 6. INTENT: General Greeting or Friendly Conversation (No Tools Called!)
    # ------------------------------------------------------------------------
    if lang == LANG_TE:
        reply = (
            "నమస్కారం! నేను మీ **కార్బన్ కోచ్ (Carbon Coach)** 🌱.\n\n"
            "నేను మీకు రెండు విధాలుగా సహాయం చేయగలను:\n"
            "1. **పర్యావరణ ప్రశ్నలు:** 'కార్బన్ ఫుట్‌ప్రింట్ అంటే ఏమిటి?', 'వాతావరణ మార్పులకు కారణాలేంటి?', 'పునరుత్పాదక శక్తిని వివరించండి' వంటి ప్రశ్నలు అడగవచ్చు.\n"
            "2. **ఉద్గారాల లెక్కింపు:** మీ ప్రయాణం లేదా విద్యుత్ వాడకం గురించి చెప్పండి (ఉదా: *'ఈరోజు 12 కిమీ బస్సులో ప్రయాణించాను మరియు 4 గంటలు ఏసీ వాడాను'*).\n\n"
            "నేను మీకు ఖచ్చితమైన సమాధానాలు మరియు పొదుపు చిట్కాలను అందిస్తాను!"
        )
    elif lang == LANG_HI:
        reply = (
            "नमस्ते! मैं आपका **कार्बन कोच (Carbon Coach)** हूँ 🌱।\n\n"
            "मैं आपकी दो तरह से सहायता कर सकता हूँ:\n"
            "1. **पर्यावरण और जलवायु संबंधी प्रश्न:** जैसे 'कार्बन फुटप्रिंट क्या है?', 'जलवायु परिवर्तन के कारण क्या हैं?', 'कॉलेज को सस्टेनेबल कैसे बनाएं?'।\n"
            "2. **दैनिक उत्सर्जन ट्रैकिंग:** अपनी दैनिक गतिविधियों को बताएं (जैसे: *'मैंने 12 किमी बस से यात्रा की और 4 घंटे एसी चलाया'*).\n\n"
            "बताइए आज आप क्या जानना या ट्रैक करना चाहते हैं?"
        )
    else:
        reply = (
            "Hello! I am your **Carbon Coach** 🌱.\n\n"
            "I can assist you in two key ways:\n"
            "1. **Climate & Sustainability Guidance:** Ask me anything conceptual, such as *'What is carbon footprint?'*, *'What causes climate change?'*, *'Explain renewable energy'*, or *'How can my college become sustainable?'*\n"
            "2. **Precision Emission Tracking:** Tell me about your daily routine (e.g., *'I travelled 12 km by bus and used the AC for 4 hours'*), and I will calculate your verified emissions and suggest personalized reduction tips.\n\n"
            "What would you like to explore or log today?"
        )

    memory_store.add_chat_message(session_id=session_id, role="assistant", content=reply)
    return {
        "reply": reply,
        "response": reply,
        "tool_calls": [],
        "language": lang,
        "intent": "greeting",
        "summary": get_summary("all", session_id)
    }


# ============================================================================
# API ROUTES
# ============================================================================
@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Main conversational endpoint:
    First attempts execution via Google ADK Gemini Runner if GEMINI_API_KEY is configured.
    Gracefully falls back to deterministic conversational intelligence engine.
    """
    # 1. Try Google ADK Gemini agent execution
    adk_result = await run_agent_turn(
        message=req.message,
        session_id=req.session_id,
        campus_group=req.campus_group
    )
    if adk_result and adk_result.get("reply"):
        memory_store.add_chat_message(req.session_id, "user", req.message)
        memory_store.add_chat_message(req.session_id, "assistant", adk_result["reply"])
        return JSONResponse(content={
            "reply": adk_result["reply"],
            "response": adk_result["reply"],
            "tool_calls": adk_result.get("tool_calls", []),
            "session_id": req.session_id,
            "engine": "google_adk_gemini",
            "summary": get_summary("all", req.session_id)
        })

    # 2. Conversational reasoning engine fallback
    res = process_conversational_message(
        message=req.message,
        session_id=req.session_id,
        campus_group=req.campus_group
    )
    return JSONResponse(content=res)


@app.get("/api/summary")
async def summary_endpoint(session_id: str = "default_user", period: str = "all"):
    """Returns total emissions and category breakdowns."""
    summary = get_summary(period=period, session_id=session_id)
    return JSONResponse(content=summary)


@app.get("/api/activities")
async def activities_endpoint(session_id: str = "default_user", period: str = "all"):
    """Returns list of activities logged in the session."""
    activities = memory_store.get_activities(session_id=session_id, period=period)
    return JSONResponse(content={"activities": activities})


@app.get("/api/campus")
async def campus_endpoint():
    """Returns campus hostel & department leaderboards."""
    board = get_campus_leaderboard()
    return JSONResponse(content=board)


@app.get("/api/reductions")
async def reductions_endpoint(category: str = ""):
    """Returns actionable reduction tips with exact kg savings."""
    tips = suggest_reductions(highest_category=category)
    return JSONResponse(content=tips)


@app.post("/api/clear")
async def clear_endpoint(session_id: str = "default_user"):
    """Clears session memory."""
    memory_store.clear_session(session_id=session_id)
    return JSONResponse(content={"status": "cleared", "session_id": session_id})


@app.get("/health")
async def health_check():
    """Health check for Cloud Run and container orchestration."""
    return {"status": "healthy", "service": "carbon-coach", "version": "1.0.0"}


# Serve modern React SaaS frontend (dist) if present, else fallback to static
react_dist_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist"))
static_dir = os.path.join(os.path.dirname(__file__), "static")

if os.path.exists(react_dist_dir) and os.path.exists(os.path.join(react_dist_dir, "index.html")):
    app.mount("/assets", StaticFiles(directory=os.path.join(react_dist_dir, "assets")), name="react-assets")

    @app.get("/")
    async def serve_index():
        index_path = os.path.join(react_dist_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())

    @app.get("/legacy")
    async def serve_legacy():
        index_path = os.path.join(static_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
elif os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    @app.get("/")
    async def serve_index():
        index_path = os.path.join(static_dir, "index.html")
        with open(index_path, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("carbon_coach.server:app", host="0.0.0.0", port=port, reload=False)
