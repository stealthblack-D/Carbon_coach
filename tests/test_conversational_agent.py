"""
test_conversational_agent.py - Tests for Carbon Coach Conversational Intelligence.
Verifies that:
1. General sustainability and climate questions are answered directly using conversational knowledge without calling calculation tools.
2. Specific activity queries trigger the appropriate calculation tools and log activities.
3. Follow-up questions resolve context from recent conversation memory.
4. No internal tool execution details or raw JSON are exposed to users.
5. Multilingual inputs (English, Telugu, Hindi) receive natural language responses.
"""

import pytest
from carbon_coach.server import process_conversational_message
from carbon_coach.memory import CarbonMemory
from carbon_coach.tools import calculate_travel_emissions


@pytest.fixture(autouse=True)
def clean_test_session():
    """Ensure clean test session for each test."""
    from carbon_coach.memory import memory_store
    memory_store.clear_session(session_id="test_conversation_user")
    yield
    memory_store.clear_session(session_id="test_conversation_user")


def test_general_question_what_is_carbon_footprint():
    """Requirement 5: 'What is carbon footprint?' answered directly with no calculation tool calls."""
    res = process_conversational_message(
        message="What is carbon footprint?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "carbon footprint" in res["reply"].lower()
    assert "5.2" in res["reply"] or "greenhouse" in res["reply"].lower()


def test_general_question_what_causes_climate_change():
    """Requirement 5: 'What causes climate change?' answered directly without tools."""
    res = process_conversational_message(
        message="What causes climate change?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "fossil fuels" in res["reply"].lower()
    assert "greenhouse effect" in res["reply"].lower()


def test_general_question_why_are_carbon_emissions_harmful():
    """Requirement 5: 'Why are carbon emissions harmful?' answered directly without tools."""
    res = process_conversational_message(
        message="Why are carbon emissions harmful?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "global warming" in res["reply"].lower() or "ocean acidification" in res["reply"].lower()


def test_general_question_how_can_i_reduce_my_carbon_footprint():
    """Requirement 5: 'How can I reduce my carbon footprint?' answered directly without tools."""
    res = process_conversational_message(
        message="How can I reduce my carbon footprint?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "public transit" in res["reply"].lower() or "ac thermostat" in res["reply"].lower()


def test_general_question_explain_renewable_energy():
    """Requirement 5: 'Explain renewable energy.' answered directly without tools."""
    res = process_conversational_message(
        message="Explain renewable energy.",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "solar" in res["reply"].lower()
    assert "wind" in res["reply"].lower()


def test_general_question_how_can_my_college_become_sustainable():
    """Requirement 5: 'How can my college become sustainable?' answered directly without tools."""
    res = process_conversational_message(
        message="How can my college become sustainable?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "solar" in res["reply"].lower()
    assert "hostel" in res["reply"].lower() or "campus" in res["reply"].lower()


def test_activity_query_calls_tools_and_explains_naturally():
    """Requirement 6 & 10: Quantitative activity must call calculation tools and explain naturally."""
    res = process_conversational_message(
        message="I travelled 12 km by bus today and used the AC for 4 hours",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "activity_calculation"
    assert len(res["tool_calls"]) >= 2

    # Check tools were called
    called_tool_names = [tc["tool"] for tc in res["tool_calls"]]
    assert "calculate_travel_emissions" in called_tool_names
    assert "calculate_electricity_emissions" in called_tool_names
    assert "log_activity" in called_tool_names

    # Check emissions calculation (12 * 0.082 = 0.984 travel + 4 * 1.2 * 0.713 = 3.4224 electricity = 4.4064 kg)
    assert res["emissions_kg"] == pytest.approx(4.4064, rel=1e-3)

    # Check natural language explanation
    assert "4.406" in res["reply"]
    assert "Activities Tracked & Verified" in res["reply"]
    assert "DEFRA" in res["reply"]
    assert "CEA" in res["reply"]


def test_contextual_follow_up_query():
    """Requirement 8: Follow-up question uses session memory context to compute comparative savings."""
    # Turn 1: Log a travel activity (12 km by bus)
    process_conversational_message(
        message="I travelled 12 km by bus today",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )

    # Turn 2: Follow-up question asking about alternative mode
    follow_up_res = process_conversational_message(
        message="What if I took the metro instead?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )

    assert follow_up_res["intent"] == "follow_up"
    assert len(follow_up_res["tool_calls"]) > 0
    assert follow_up_res["tool_calls"][0]["tool"] == "calculate_travel_emissions"
    # Metro is 12 km * 0.029 = 0.348 kg CO2e
    assert "metro" in follow_up_res["reply"].lower()
    assert "saved" in follow_up_res["reply"].lower()


def test_multilingual_general_question_telugu():
    """Requirement 5: Telugu questions get natural responses in Telugu."""
    res = process_conversational_message(
        message="కార్బన్ ఫుట్‌ప్రింట్ అంటే ఏమిటి?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "కార్బన్" in res["reply"]
    assert "గ్రీన్‌హౌస్" in res["reply"] or "వాతావరణం" in res["reply"]


def test_multilingual_general_question_hindi():
    """Requirement 5: Hindi questions get natural responses in Hindi."""
    res = process_conversational_message(
        message="जलवायु परिवर्तन के मुख्य कारण क्या हैं?",
        session_id="test_conversation_user",
        campus_group="Hostel Krishna"
    )
    assert res["intent"] == "general_qa"
    assert len(res["tool_calls"]) == 0
    assert "जलवायु परिवर्तन" in res["reply"]
    assert "जीवाश्म ईंधन" in res["reply"] or "ग्रीनहाउस" in res["reply"]
