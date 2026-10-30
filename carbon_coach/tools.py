"""
tools.py - Python tools for Carbon Coach.
Performs exact mathematical carbon emission calculations based on official emission factors.
NO made-up numbers: all outputs cite sources and return deterministic figures.
"""

from typing import Dict, Any, Optional
from carbon_coach.emission_factors import (
    GRID_ELECTRICITY_INDIA_KG_PER_KWH,
    ELECTRICITY_SOURCE_CITATION,
    APPLIANCE_POWER_KW,
    TRANSPORT_FACTORS_KG_PER_KM,
    TRANSPORT_SOURCE_CITATION,
    FOOD_FACTORS_KG_PER_MEAL,
    FOOD_SOURCE_CITATION,
    WASTE_FACTORS_KG_PER_KG,
    WASTE_SOURCE_CITATION,
    BENCHMARKS,
)
from carbon_coach.memory import memory_store


def calculate_travel_emissions(mode: str, km: float) -> Dict[str, Any]:
    """
    Calculates carbon emissions in kg CO2e for travel based on mode of transport and distance in kilometers.

    Args:
        mode: The transportation mode (e.g. 'bus', 'train', 'metro', 'car', 'bike', 'motorcycle',
              'auto', 'auto_rickshaw', 'electric_scooter', 'walking', 'bicycle', 'flight').
        km: The distance traveled in kilometers (must be positive).

    Returns:
        dict with exact emissions_kg, mode, km, factor_kg_per_km, source citation, and alternative savings.
    """
    if km < 0:
        return {"error": "Distance (km) cannot be negative.", "emissions_kg": 0.0}

    mode_normalized = mode.strip().lower().replace("-", "_").replace(" ", "_")

    # Match or fallback
    factor = TRANSPORT_FACTORS_KG_PER_KM.get(mode_normalized)
    matched_mode = mode_normalized

    if factor is None:
        # fuzzy matching
        for key, val in TRANSPORT_FACTORS_KG_PER_KM.items():
            if key in mode_normalized or mode_normalized in key:
                factor = val
                matched_mode = key
                break

    if factor is None:
        # Default to average public bus if unrecognized
        factor = TRANSPORT_FACTORS_KG_PER_KM["bus"]
        matched_mode = f"{mode} (defaulted to public bus)"

    emissions_kg = round(km * factor, 4)

    # Calculate potential savings if user switches to a greener mode
    savings_tips = []
    if matched_mode in ("car", "car_petrol", "cab", "taxi"):
        bus_emissions = round(km * TRANSPORT_FACTORS_KG_PER_KM["bus"], 4)
        metro_emissions = round(km * TRANSPORT_FACTORS_KG_PER_KM["metro"], 4)
        savings_tips.append(f"Switching to bus saves {round(emissions_kg - bus_emissions, 4)} kg CO2e.")
        savings_tips.append(f"Switching to metro saves {round(emissions_kg - metro_emissions, 4)} kg CO2e.")
    elif matched_mode in ("auto", "auto_rickshaw", "two_wheeler", "bike", "motorcycle", "scooter"):
        if km <= 5:
            savings_tips.append(f"Walking or cycling saves all {emissions_kg} kg CO2e (100% reduction).")
        bus_emissions = round(km * TRANSPORT_FACTORS_KG_PER_KM["bus"], 4)
        if emissions_kg > bus_emissions:
            savings_tips.append(f"Public bus saves {round(emissions_kg - bus_emissions, 4)} kg CO2e.")

    return {
        "status": "success",
        "category": "travel",
        "mode": matched_mode,
        "distance_km": round(km, 2),
        "factor_kg_per_km": factor,
        "emissions_kg": emissions_kg,
        "source": TRANSPORT_SOURCE_CITATION,
        "alternative_savings": savings_tips,
        "formula": f"{km} km * {factor} kg CO2e/km = {emissions_kg} kg CO2e"
    }


def calculate_electricity_emissions(
    kwh: float = 0.0,
    appliance: str = "",
    hours: float = 0.0
) -> Dict[str, Any]:
    """
    Calculates carbon emissions in kg CO2e for electricity use, either by raw kWh or by appliance and hours of use.

    Args:
        kwh: Total energy in kilowatt-hours (if known directly).
        appliance: Name of appliance (e.g. 'ac', '1.5_ton_ac', 'fan', 'led_light', 'laptop', 'geyser', 'refrigerator', 'tv').
        hours: Number of hours the appliance was active.

    Returns:
        dict with exact emissions_kg, energy_kwh, appliance, hours, source citation, and actionable tips.
    """
    calculated_kwh = 0.0
    appliance_used = "direct_kwh"
    power_kw = 0.0

    if kwh > 0:
        calculated_kwh = kwh
    elif appliance and hours > 0:
        appliance_norm = appliance.strip().lower().replace("-", "_").replace(" ", "_")
        power_kw = APPLIANCE_POWER_KW.get(appliance_norm)

        if power_kw is None:
            # Fuzzy match
            for key, val in APPLIANCE_POWER_KW.items():
                if key in appliance_norm or appliance_norm in key:
                    power_kw = val
                    appliance_norm = key
                    break

        if power_kw is None:
            power_kw = 0.50  # Average appliance fallback (500W)
            appliance_norm = f"{appliance} (estimated at 0.5 kW)"

        appliance_used = appliance_norm
        calculated_kwh = round(power_kw * hours, 4)
    else:
        return {"error": "Must provide either positive kwh or appliance with hours.", "emissions_kg": 0.0}

    emissions_kg = round(calculated_kwh * GRID_ELECTRICITY_INDIA_KG_PER_KWH, 4)

    # Reduction tips
    reduction_tips = []
    if "ac" in appliance_used:
        # Increasing set temp from 18C to 24C saves ~24% power (~0.04 kW per degree)
        savings_kwh = round(calculated_kwh * 0.24, 4)
        savings_kg = round(savings_kwh * GRID_ELECTRICITY_INDIA_KG_PER_KWH, 4)
        reduction_tips.append(
            f"Setting AC to 24°C instead of 18°C saves ~24% power: saving {savings_kg} kg CO2e ({savings_kwh} kWh)."
        )
        # Using a timer to cut 1 hour
        if hours > 1:
            one_hr_kg = round(power_kw * 1.0 * GRID_ELECTRICITY_INDIA_KG_PER_KWH, 4)
            reduction_tips.append(f"Turning off AC 1 hour earlier saves {one_hr_kg} kg CO2e daily.")
    elif "geyser" in appliance_used:
        reduction_tips.append("Switching to a 10-minute shower cuts water heater emissions by ~50%.")

    return {
        "status": "success",
        "category": "electricity",
        "appliance": appliance_used,
        "hours": round(hours, 2),
        "power_rating_kw": power_kw if power_kw > 0 else None,
        "energy_kwh": round(calculated_kwh, 4),
        "grid_factor_kg_per_kwh": GRID_ELECTRICITY_INDIA_KG_PER_KWH,
        "emissions_kg": emissions_kg,
        "source": ELECTRICITY_SOURCE_CITATION,
        "reduction_tips": reduction_tips,
        "formula": f"{round(calculated_kwh, 4)} kWh * {GRID_ELECTRICITY_INDIA_KG_PER_KWH} kg CO2e/kWh = {emissions_kg} kg CO2e"
    }


def calculate_food_emissions(meal_type: str, meals_count: int = 1) -> Dict[str, Any]:
    """
    Calculates carbon emissions in kg CO2e for meals based on dietary type and number of meals.

    Args:
        meal_type: Type of meal (e.g. 'vegan', 'vegetarian', 'veg', 'campus_mess', 'egg_meal', 'chicken', 'mutton', 'red_meat').
        meals_count: Number of meals (default 1).

    Returns:
        dict with exact emissions_kg, meal_type, meals_count, source citation, and alternative meal savings.
    """
    if meals_count <= 0:
        return {"error": "meals_count must be at least 1", "emissions_kg": 0.0}

    meal_norm = meal_type.strip().lower().replace("-", "_").replace(" ", "_")
    factor = FOOD_FACTORS_KG_PER_MEAL.get(meal_norm)
    matched = meal_norm

    if factor is None:
        for key, val in FOOD_FACTORS_KG_PER_MEAL.items():
            if key in meal_norm or meal_norm in key:
                factor = val
                matched = key
                break

    if factor is None:
        factor = FOOD_FACTORS_KG_PER_MEAL["vegetarian"]
        matched = f"{meal_type} (defaulted to standard vegetarian thali)"

    emissions_kg = round(factor * meals_count, 4)

    # Compare with vegan / vegetarian
    savings_tips = []
    veg_factor = FOOD_FACTORS_KG_PER_MEAL["vegetarian"]
    vegan_factor = FOOD_FACTORS_KG_PER_MEAL["vegan"]

    if factor > veg_factor:
        veg_emissions = round(veg_factor * meals_count, 4)
        savings_tips.append(
            f"Choosing a vegetarian meal would save {round(emissions_kg - veg_emissions, 4)} kg CO2e."
        )
    if factor > vegan_factor:
        vegan_emissions = round(vegan_factor * meals_count, 4)
        savings_tips.append(
            f"Choosing a plant-based/vegan meal would save {round(emissions_kg - vegan_emissions, 4)} kg CO2e."
        )

    return {
        "status": "success",
        "category": "food",
        "meal_type": matched,
        "meals_count": meals_count,
        "factor_kg_per_meal": factor,
        "emissions_kg": emissions_kg,
        "source": FOOD_SOURCE_CITATION,
        "alternative_savings": savings_tips,
        "formula": f"{meals_count} meals * {factor} kg CO2e/meal = {emissions_kg} kg CO2e"
    }


def calculate_waste_emissions(waste_type: str, kg: float, recycled: bool = False) -> Dict[str, Any]:
    """
    Calculates carbon emissions in kg CO2e for waste generated and potential savings from recycling or composting.

    Args:
        waste_type: Type of waste ('organic_food', 'plastic', 'paper', 'ewaste').
        kg: Weight of waste in kilograms.
        recycled: Whether the waste was recycled or composted (True) or sent to landfill (False).

    Returns:
        dict with exact emissions_kg, disposal_method, savings_kg, and source citation.
    """
    if kg < 0:
        return {"error": "Weight in kg cannot be negative.", "emissions_kg": 0.0}

    waste_norm = waste_type.strip().lower().replace("-", "_").replace(" ", "_")

    key = "organic_food"
    if "plastic" in waste_norm:
        key = "plastic"
    elif "paper" in waste_norm:
        key = "paper"
    elif "ewaste" in waste_norm or "electronic" in waste_norm:
        key = "ewaste"

    rates = WASTE_FACTORS_KG_PER_KG[key]
    disposal = "recycled" if (recycled or (key == "organic_food" and recycled)) else "landfill"
    if key == "organic_food" and recycled:
        disposal = "compost"

    factor = rates[disposal]
    emissions_kg = round(kg * factor, 4)

    # Calculate savings compared to unmanaged landfill
    landfill_emissions = round(kg * rates["landfill"], 4)
    savings_kg = round(max(0.0, landfill_emissions - emissions_kg), 4) if recycled else 0.0

    return {
        "status": "success",
        "category": "waste",
        "waste_type": key,
        "weight_kg": round(kg, 3),
        "disposal_method": disposal,
        "factor_kg_per_kg": factor,
        "emissions_kg": emissions_kg,
        "savings_from_recycling_kg": savings_kg,
        "source": WASTE_SOURCE_CITATION,
        "formula": f"{kg} kg * {factor} kg CO2e/kg = {emissions_kg} kg CO2e"
    }


def log_activity(
    category: str,
    description: str,
    emissions_kg: float,
    session_id: str = "default_user",
    campus_group: str = "Hostel Cauvery"
) -> Dict[str, Any]:
    """
    Logs an activity into session memory so that totals and trends are remembered.

    Args:
        category: Activity category ('travel', 'electricity', 'food', 'waste').
        description: Plain language description (e.g. '12 km by bus', '4 hours AC usage').
        emissions_kg: The verified emission in kg CO2e (must come from a calculation tool).
        session_id: User/session identifier.
        campus_group: Hostel or Department name for the campus leaderboard (e.g. 'Hostel Krishna', 'Dept of CSE').

    Returns:
        dict confirming activity logged and updated session total.
    """
    res = memory_store.log_activity(
        category=category,
        description=description,
        emissions_kg=emissions_kg,
        session_id=session_id,
        campus_group=campus_group
    )
    summary = memory_store.get_summary(session_id=session_id, period="all")
    res["session_total_emissions_kg"] = summary["total_emissions_kg"]
    return res


def get_summary(period: str = "all", session_id: str = "default_user") -> Dict[str, Any]:
    """
    Retrieves the summary of emissions logged in the session over a specified period.

    Args:
        period: Time period to summarize ('today', 'week', 'month', 'all').
        session_id: User/session identifier.

    Returns:
        dict with total_emissions_kg, activity_count, by_category_kg breakdown, percentages, and benchmark comparison.
    """
    summary = memory_store.get_summary(session_id=session_id, period=period)
    total = summary["total_emissions_kg"]

    # Add comparison to Indian daily per-capita benchmark
    bench = BENCHMARKS["india_daily_per_capita"]
    diff_kg = round(total - bench, 4)
    status_msg = "below" if diff_kg < 0 else "above"

    summary["benchmark_comparison"] = {
        "india_daily_average_kg": bench,
        "difference_kg": abs(diff_kg),
        "status": f"{abs(diff_kg)} kg {status_msg} the national daily per capita average ({bench} kg)."
    }
    return summary


def suggest_reductions(
    highest_category: str = "",
    current_emissions_kg: float = 0.0
) -> Dict[str, Any]:
    """
    Provides personalized high-impact suggestions to reduce carbon footprint with exact estimated savings.

    Args:
        highest_category: The user's highest emission category ('travel', 'electricity', 'food', 'waste', or '').
        current_emissions_kg: Current logged emissions to contextualize recommendations.

    Returns:
        dict containing tailored reduction actions, each with verified estimated savings in kg CO2e.
    """
    suggestions = []

    cat = highest_category.lower().strip()

    if cat in ("electricity", "energy", "power") or not cat:
        suggestions.append({
            "action": "Raise AC temperature setting to 24°C from 18°C",
            "category": "electricity",
            "estimated_saving_kg_co2e_per_day": 0.82,
            "annual_saving_kg_co2e": 246.0,
            "cost_saving": "Saves ~24% on electricity bill",
            "source": "CEA India & BEE (Bureau of Energy Efficiency) guidelines"
        })
        suggestions.append({
            "action": "Turn off AC 1 hour before waking up using sleep timer",
            "category": "electricity",
            "estimated_saving_kg_co2e_per_day": 0.86,
            "annual_saving_kg_co2e": 258.0,
            "source": "CEA India Baseline v20"
        })

    if cat in ("travel", "transport") or not cat:
        suggestions.append({
            "action": "Replace 10 km solo auto/car ride with city RTC bus or campus shuttle",
            "category": "travel",
            "estimated_saving_kg_co2e_per_trip": 0.88,
            "weekly_saving_kg_co2e": 4.40,
            "source": "DEFRA Transport Conversion Factors"
        })
        suggestions.append({
            "action": "Use bicycle or walking for trips under 2 km on campus",
            "category": "travel",
            "estimated_saving_kg_co2e_per_trip": 0.09,
            "weekly_saving_kg_co2e": 0.63,
            "source": "Zero tailpipe emission"
        })

    if cat in ("food", "diet") or not cat:
        suggestions.append({
            "action": "Swap one chicken meal for a wholesome vegetarian mess thali",
            "category": "food",
            "estimated_saving_kg_co2e_per_meal": 1.40,
            "weekly_saving_kg_co2e": 4.20,
            "source": "Poore & Nemecek (2018), Science"
        })
        suggestions.append({
            "action": "Zero food waste in mess: finish everything on your plate",
            "category": "food/waste",
            "estimated_saving_kg_co2e_per_day": 0.29,
            "source": "EPA WARM Food Waste Model"
        })

    if cat in ("waste", "plastic") or not cat:
        suggestions.append({
            "action": "Carry a reusable steel water bottle instead of single-use PET bottles",
            "category": "waste",
            "estimated_saving_kg_co2e_per_month": 3.15,
            "source": "World Bank What a Waste 2.0"
        })

    total_potential_daily_saving = sum(
        s.get("estimated_saving_kg_co2e_per_day", 0.0) or s.get("estimated_saving_kg_co2e_per_trip", 0.0)
        for s in suggestions
    )

    return {
        "status": "success",
        "focus_category": cat or "all",
        "total_potential_daily_saving_kg": round(total_potential_daily_saving, 2),
        "suggestions": suggestions
    }


def get_campus_leaderboard() -> Dict[str, Any]:
    """
    Returns the live campus hostel and department carbon leaderboard.
    Compares per-capita daily emissions to foster positive eco-competition.

    Returns:
        dict containing ranked hostels, departments, and greenest groups.
    """
    board = memory_store.get_campus_leaderboard()
    hostels = [b for b in board if b["category"] == "Hostel"]
    departments = [b for b in board if b["category"] == "Department"]

    top_hostel = hostels[0]["name"] if hostels else "None"
    top_dept = departments[0]["name"] if departments else "None"

    return {
        "status": "success",
        "top_hostel": top_hostel,
        "top_department": top_dept,
        "hostel_leaderboard": hostels,
        "department_leaderboard": departments,
        "campus_residents_tracked": sum(b["residents"] for b in board)
    }


def compare_to_benchmark(emissions_kg: float, period: str = "day") -> Dict[str, Any]:
    """
    Compares an emission total to Indian and global per capita benchmarks.

    Args:
        emissions_kg: Total emissions in kg CO2e.
        period: Time unit ('day', 'week', 'month', 'year').

    Returns:
        dict with benchmark comparisons and climate impact analysis.
    """
    multiplier = 1.0
    if period == "week":
        multiplier = 7.0
    elif period == "month":
        multiplier = 30.0
    elif period == "year":
        multiplier = 365.0

    india_bench = round(BENCHMARKS["india_daily_per_capita"] * multiplier, 2)
    global_bench = round(BENCHMARKS["global_daily_per_capita"] * multiplier, 2)
    paris_bench = round(BENCHMARKS["paris_target_2030_daily"] * multiplier, 2)
    student_bench = round(BENCHMARKS["student_average_daily"] * multiplier, 2)

    return {
        "user_emissions_kg": round(emissions_kg, 2),
        "period": period,
        "benchmarks_kg": {
            "india_average": india_bench,
            "global_average": global_bench,
            "paris_2030_target": paris_bench,
            "campus_student_average": student_bench,
        },
        "vs_india_average_pct": round(((emissions_kg - india_bench) / india_bench) * 100, 1) if india_bench > 0 else 0,
        "vs_global_average_pct": round(((emissions_kg - global_bench) / global_bench) * 100, 1) if global_bench > 0 else 0,
        "status": "sustainable" if emissions_kg <= paris_bench else "elevated"
    }


# Export list of ADK callable tool functions
CARBON_COACH_TOOLS = [
    calculate_travel_emissions,
    calculate_electricity_emissions,
    calculate_food_emissions,
    calculate_waste_emissions,
    log_activity,
    get_summary,
    suggest_reductions,
    get_campus_leaderboard,
    compare_to_benchmark
]
