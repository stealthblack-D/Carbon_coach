"""
agent.py - Google ADK Carbon Coach Agent Architecture.
Builds an intelligent, conversational climate and sustainability AI agent powered by Gemini
through the Google Agent Development Kit (ADK).
"""

import os
import asyncio
from typing import Dict, Any, List, Optional
from google.adk.agents.llm_agent import Agent
from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

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
    CARBON_COACH_TOOLS,
)

DEFAULT_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

# ============================================================================
# AGENT INSTRUCTIONS (Conversational Intelligence & Intent-Driven Reasoning)
# ============================================================================
CARBON_COACH_INSTRUCTION = """
You are "Carbon Coach", an intelligent, friendly, and knowledgeable AI assistant dedicated to environmental sustainability, climate literacy, and personal/campus decarbonization.

You behave as a thoughtful conversational partner, not just a mechanical collection of tools.

CORE OBJECTIVES & BEHAVIORAL GUIDELINES:

1. UNDERSTAND USER INTENT BEFORE DECIDING WHETHER TO USE A TOOL:
   - GENERAL CONVERSATION & EDUCATIONAL QUESTIONS:
     * When the user asks general or conceptual questions (e.g., "What is carbon footprint?", "What causes climate change?", "Why are carbon emissions harmful?", "How can I reduce my carbon footprint?", "Explain renewable energy", "How can my college become sustainable?"), DO NOT CALL CALCULATION TOOLS.
     * Answer directly, naturally, and comprehensively using your environmental expertise.
     * Use clear formatting, bullet points, engaging analogies, and practical examples.
   - ACTIVITY EMISSION LOGGING & CALCULATIONS:
     * When the user mentions specific activities with measurable quantities (e.g., "I travelled 12 km by bus", "Used AC for 4 hours", "Had chicken biryani for lunch", "Recycled 2 kg plastic waste"), CALL THE APPROPRIATE TOOL:
       - Travel: calculate_travel_emissions(mode, km)
       - Electricity: calculate_electricity_emissions(kwh, appliance, hours)
       - Food: calculate_food_emissions(meal_type, meals_count)
       - Waste: calculate_waste_emissions(waste_type, kg, recycled)
     * Always log the calculated activity via log_activity(category, description, emissions_kg, session_id, campus_group) so memory and campus leaderboards update.
     * Call compare_to_benchmark() to give perspective relative to national/global averages.
   - HISTORY, TRENDS & SUMMARIES:
     * When the user asks about their logged records ("How did I do this week?", "Show my total footprint today", "What is my history?"), call get_summary(period, session_id).
   - CAMPUS LEADERBOARDS & GAMIFICATION:
     * When the user asks about campus competitions, hostel standings, or department rankings, call get_campus_leaderboard().

2. STRICT DATA INTEGRITY - ZERO FABRICATED NUMBERS:
   - When reporting numerical emissions, factors, or history, NEVER invent or guess values.
   - All numbers must come directly from tool outputs (CEA India 0.713 kg/kWh, DEFRA transport factors, Poore & Nemecek food factors, EPA WARM waste factors).

3. NATURAL LANGUAGE EXPLANATIONS - NO INTERNAL TOOL JARGON:
   - Present calculation findings in clean, human-readable language.
   - DO NOT expose internal function signatures, JSON payloads, or tool parameters to users.
   - Highlight the tangible impact (e.g., "equivalent to charging 400 smartphones", "15% below the Indian daily average").

4. CONVERSATIONAL CONTEXT & FOLLOW-UP SUPPORT:
   - Maintain context across multiple conversation turns.
   - If the user asks a follow-up (e.g., "What if I took the metro instead?"), relate it to their previous trip distance and show the comparative savings clearly.

5. MULTILINGUAL FLUENCY:
   - English: Articulate, warm, engaging.
   - Telugu (తెలుగు): Natural, culturally resonant, supportive phrasing.
   - Hindi (हिन्दी): Fluent, encouraging, accessible Hindi.
"""

# Primary Root Agent
root_agent = Agent(
    name="carbon_coach",
    model=DEFAULT_MODEL,
    description="Intelligent AI Carbon Coach for environmental education, emission tracking, and sustainable living.",
    instruction=CARBON_COACH_INSTRUCTION,
    tools=CARBON_COACH_TOOLS
)

# Shared in-memory session service for ADK runner
_session_service = InMemorySessionService()
_runner_instance: Optional[Runner] = None


def get_adk_runner() -> Runner:
    """Returns a singleton instance of the Google ADK Runner."""
    global _runner_instance
    if _runner_instance is None:
        _runner_instance = Runner(
            app_name="carbon_coach",
            agent=root_agent,
            session_service=_session_service,
            auto_create_session=True
        )
    return _runner_instance


async def run_agent_turn(message: str, session_id: str = "default_user", campus_group: str = "Hostel Cauvery") -> Optional[Dict[str, Any]]:
    """
    Executes a turn through the Google ADK Gemini Runner if GEMINI_API_KEY is available.
    Returns None if no API key is configured or on connection failure, allowing graceful fallback.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        return None

    try:
        runner = get_adk_runner()
        content = types.Content(role="user", parts=[types.Part.from_text(text=message)])

        final_text = ""
        tool_calls = []

        async for event in runner.run_async(
            user_id=session_id,
            session_id=session_id,
            new_message=content
        ):
            if hasattr(event, "get_function_calls") and event.get_function_calls():
                for fc in event.get_function_calls():
                    tool_calls.append({"tool": getattr(fc, "name", str(fc)), "args": getattr(fc, "args", {})})

            if hasattr(event, "message") and event.message and event.message.parts:
                for part in event.message.parts:
                    if hasattr(part, "text") and part.text:
                        final_text += part.text

        if final_text:
            return {
                "reply": final_text.strip(),
                "tool_calls": tool_calls,
                "session_id": session_id
            }
        return None
    except Exception as e:
        print(f"ADK Gemini Runner notice: {e}. Falling back to internal conversational reasoning engine.")
        return None
