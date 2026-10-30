"""
test_golden_cases.py - Golden evaluation cases for Carbon Coach.
Verifies calculation accuracy, absence of fabricated numbers, memory consistency,
campus leaderboard logic, and multilingual detection.
"""

import pytest
import os
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
)
from carbon_coach.memory import CarbonMemory
from carbon_coach.multilingual import detect_language, LANG_EN, LANG_TE, LANG_HI
from carbon_coach.emission_factors import (
    GRID_ELECTRICITY_INDIA_KG_PER_KWH,
    TRANSPORT_FACTORS_KG_PER_KM,
    FOOD_FACTORS_KG_PER_MEAL,
    WASTE_FACTORS_KG_PER_KG,
    BENCHMARKS,
)


@pytest.fixture
def temp_memory(tmp_path):
    """Provides a fresh isolated database for testing memory."""
    db_file = str(tmp_path / "test_carbon.db")
    mem = CarbonMemory(db_path=db_file)
    return mem


# ============================================================================
# 1. TRAVEL EMISSION TESTS
# ============================================================================
def test_travel_emissions_bus_12km():
    """Golden Case: 12 km by bus = 12 * 0.082 = 0.984 kg CO2e."""
    result = calculate_travel_emissions(mode="bus", km=12.0)
    assert result["status"] == "success"
    assert result["category"] == "travel"
    assert result["distance_km"] == 12.0
    assert result["factor_kg_per_km"] == pytest.approx(0.082, rel=1e-3)
    assert result["emissions_kg"] == pytest.approx(0.984, rel=1e-3)
    assert "DEFRA" in result["source"]


def test_travel_emissions_active_zero():
    """Walking and cycling must produce 0.000 kg CO2e."""
    cycle = calculate_travel_emissions(mode="bicycle", km=8.5)
    assert cycle["emissions_kg"] == 0.0

    walk = calculate_travel_emissions(mode="walking", km=3.0)
    assert walk["emissions_kg"] == 0.0


def test_travel_emissions_car_vs_bike():
    """Verify car vs motorcycle emissions."""
    car = calculate_travel_emissions(mode="car", km=20.0)
    bike = calculate_travel_emissions(mode="bike", km=20.0)

    assert car["emissions_kg"] == pytest.approx(3.40, rel=1e-3)
    assert bike["emissions_kg"] == pytest.approx(0.90, rel=1e-3)
    assert car["emissions_kg"] > bike["emissions_kg"]


def test_travel_emissions_negative_km():
    """Edge Case: Negative distances must be rejected."""
    result = calculate_travel_emissions(mode="bus", km=-5.0)
    assert "error" in result
    assert result["emissions_kg"] == 0.0


# ============================================================================
# 2. ELECTRICITY EMISSION TESTS
# ============================================================================
def test_electricity_emissions_ac_4hours():
    """Golden Case: 1.5-ton AC (1.2 kW) for 4 hours = 4.8 kWh * 0.713 = 3.4224 kg CO2e."""
    result = calculate_electricity_emissions(appliance="ac", hours=4.0)
    assert result["status"] == "success"
    assert result["category"] == "electricity"
    assert result["hours"] == 4.0
    assert result["energy_kwh"] == pytest.approx(4.8, rel=1e-3)
    assert result["grid_factor_kg_per_kwh"] == pytest.approx(0.713, rel=1e-3)
    assert result["emissions_kg"] == pytest.approx(3.4224, rel=1e-3)
    assert "CEA" in result["source"]


def test_electricity_emissions_direct_kwh():
    """Direct kWh calculation: 10 kWh * 0.713 = 7.130 kg CO2e."""
    result = calculate_electricity_emissions(kwh=10.0)
    assert result["energy_kwh"] == 10.0
    assert result["emissions_kg"] == pytest.approx(7.130, rel=1e-3)


# ============================================================================
# 3. HACKATHON CORE COMBINED CASE
# ============================================================================
def test_hackathon_challenge_statement_case():
    """
    User: 'I travelled 12 km by bus today and used the AC for 4 hours.'
    Bus: 12 * 0.082 = 0.984 kg CO2e
    AC: 4 * 1.2 * 0.713 = 3.4224 kg CO2e
    Total: 4.4064 kg CO2e
    """
    travel = calculate_travel_emissions(mode="bus", km=12.0)
    elec = calculate_electricity_emissions(appliance="ac", hours=4.0)

    total_emissions = travel["emissions_kg"] + elec["emissions_kg"]
    assert total_emissions == pytest.approx(4.4064, rel=1e-4)

    # Compare against Indian student baseline (3.8 kg/day)
    bench = compare_to_benchmark(total_emissions, period="day")
    assert bench["user_emissions_kg"] == pytest.approx(4.41, rel=1e-2)
    assert bench["status"] == "sustainable"  # <= 5.5 Paris target, but slightly above student avg


# ============================================================================
# 4. FOOD & WASTE TESTS
# ============================================================================
def test_food_emissions_comparison():
    """Vegetarian (1.2 kg) vs Chicken (2.6 kg) meal."""
    veg = calculate_food_emissions("vegetarian", meals_count=2)
    assert veg["emissions_kg"] == pytest.approx(2.40, rel=1e-3)

    chicken = calculate_food_emissions("chicken", meals_count=1)
    assert chicken["emissions_kg"] == pytest.approx(2.60, rel=1e-3)
    assert len(chicken["alternative_savings"]) > 0


def test_waste_emissions_recycling_savings():
    """Recycling 2 kg plastic saves 1.50 kg CO2e/kg = 3.0 kg CO2e."""
    recycled = calculate_waste_emissions("plastic", kg=2.0, recycled=True)
    landfill = calculate_waste_emissions("plastic", kg=2.0, recycled=False)

    assert recycled["emissions_kg"] == pytest.approx(1.20, rel=1e-3)
    assert landfill["emissions_kg"] == pytest.approx(4.20, rel=1e-3)
    assert recycled["savings_from_recycling_kg"] == pytest.approx(3.00, rel=1e-3)


# ============================================================================
# 5. MEMORY & SUMMARY TESTS
# ============================================================================
def test_memory_logging_and_summary(temp_memory):
    """Verifies that activities are recorded and category breakdowns are exact."""
    session = "test_eval_session"

    temp_memory.log_activity("travel", "12 km bus", 0.984, session_id=session)
    temp_memory.log_activity("electricity", "4h AC", 3.4224, session_id=session)
    temp_memory.log_activity("food", "Veg lunch", 1.20, session_id=session)

    summary = temp_memory.get_summary(session_id=session, period="all")
    assert summary["activity_count"] == 3
    assert summary["total_emissions_kg"] == pytest.approx(5.6064, rel=1e-4)
    assert summary["highest_category"] == "electricity"
    assert "electricity" in summary["by_category_kg"]
    assert "travel" in summary["by_category_kg"]
    assert "food" in summary["by_category_kg"]


# ============================================================================
# 6. CAMPUS LEADERBOARD TESTS
# ============================================================================
def test_campus_leaderboard_ranking():
    """Verifies that campus groups are ranked by per capita emissions (lowest first)."""
    res = get_campus_leaderboard()
    assert res["status"] == "success"
    assert "hostel_leaderboard" in res
    assert "department_leaderboard" in res
    assert len(res["hostel_leaderboard"]) >= 3

    # Check ascending order of per capita emissions
    hostels = res["hostel_leaderboard"]
    for i in range(len(hostels) - 1):
        assert hostels[i]["per_capita_kg"] <= hostels[i+1]["per_capita_kg"]


# ============================================================================
# 7. REDUCTION SUGGESTIONS TESTS
# ============================================================================
def test_reduction_suggestions_have_savings():
    """All suggestions must have non-zero estimated savings and citations."""
    reductions = suggest_reductions(highest_category="electricity", current_emissions_kg=5.0)
    assert reductions["status"] == "success"
    assert len(reductions["suggestions"]) >= 2
    for tip in reductions["suggestions"]:
        saving = tip.get("estimated_saving_kg_co2e_per_day") or tip.get("estimated_saving_kg_co2e_per_trip")
        assert saving > 0.0
        assert "source" in tip


# ============================================================================
# 8. MULTILINGUAL TESTS
# ============================================================================
def test_language_detection():
    """Detects Telugu, Hindi, and English correctly."""
    assert detect_language("I travelled 12 km by bus") == LANG_EN
    assert detect_language("నేను 12 కిమీ బస్సులో ప్రయాణించాను") == LANG_TE
    assert detect_language("मैंने 12 किमी बस से यात्रा की") == LANG_HI
