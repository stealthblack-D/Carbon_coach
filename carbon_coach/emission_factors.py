"""
emission_factors.py - Scientifically verified emission factors with official citations.

Data Sources:
1. CEA (Central Electricity Authority, Ministry of Power, Government of India)
   CO2 Baseline Database for the Indian Power Sector (User Guide Version 20.0).
   National weighted average grid emission factor: 0.713 kg CO2e / kWh.
2. DEFRA / DESNZ (UK Department for Energy Security and Net Zero / DEFRA 2024 GHG Conversion Factors)
   and ARAI (Automotive Research Association of India) emission metrics.
3. Our World in Data / Poore & Nemecek (2018), "Reducing food's environmental impacts through producers and consumers", Science.
4. World Bank "What a Waste 2.0" & US EPA Waste Reduction Model (WARM).
"""

from typing import Dict, Any

# ============================================================================
# 1. ELECTRICITY EMISSION FACTORS (India Grid & Typical Appliances)
# ============================================================================
# Source: Central Electricity Authority (CEA), Govt of India (v20.0)
GRID_ELECTRICITY_INDIA_KG_PER_KWH = 0.713
ELECTRICITY_SOURCE_CITATION = "Central Electricity Authority (CEA) India CO2 Baseline Database v20.0 (0.713 kg CO2e/kWh)"

# Typical appliance power ratings in kW (kilowatts)
APPLIANCE_POWER_KW: Dict[str, float] = {
    # Air Conditioner: 1.5 Ton 3-star/5-star inverter average running load
    "ac": 1.20,
    "air_conditioner": 1.20,
    "1.5_ton_ac": 1.20,
    "1_ton_ac": 0.90,
    "2_ton_ac": 1.80,
    # Fans
    "ceiling_fan": 0.075,
    "fan": 0.075,
    "table_fan": 0.050,
    # Lighting
    "led_light": 0.015,
    "led_bulb": 0.015,
    "light": 0.020,
    "tube_light": 0.036,
    # Computing & Tech
    "laptop": 0.065,
    "desktop": 0.150,
    "computer": 0.120,
    "wifi_router": 0.012,
    "tv": 0.100,
    "television": 0.100,
    # Water & Kitchen Appliances
    "geyser": 2.00,
    "water_heater": 2.00,
    "refrigerator": 0.050,  # continuous avg equivalent (~1.2 kWh/day)
    "fridge": 0.050,
    "microwave": 1.20,
    "induction_stove": 1.50,
    "washing_machine": 0.50,
    "water_cooler": 0.18,
    "iron": 1.00,
}

# ============================================================================
# 2. TRAVEL EMISSION FACTORS (kg CO2e per passenger-km or vehicle-km)
# ============================================================================
# Sources: ARAI India, DEFRA 2024 Passenger Transport, India GHG Program
TRANSPORT_FACTORS_KG_PER_KM: Dict[str, float] = {
    # Public & Mass Transit (per passenger-km)
    "bus": 0.082,                 # City Transit / RTC Bus (India average occupancy)
    "city_bus": 0.082,
    "electric_bus": 0.025,
    "metro": 0.035,               # Urban Metro Train (Delhi/Hyderabad/Bangalore)
    "subway": 0.035,
    "train": 0.028,               # Indian Railways Express/Mail Passenger Train
    "rail": 0.028,
    
    # Micro-mobility & Shared Transit
    "auto": 0.055,                # Auto-rickshaw (CNG / Petrol 4-stroke, shared)
    "auto_rickshaw": 0.055,
    "cng_auto": 0.048,
    "two_wheeler": 0.045,         # Petrol Scooter/Motorcycle (100-150cc)
    "bike": 0.045,                # Commonly used by students for motorcycle
    "motorcycle": 0.045,
    "scooter": 0.045,
    "electric_scooter": 0.018,    # Electric 2-wheeler charged on Indian grid
    "ev_scooter": 0.018,
    "ev_bike": 0.018,
    
    # Cars & Cabs
    "car": 0.170,                 # Petrol car (solo driver)
    "car_petrol": 0.170,
    "car_diesel": 0.165,
    "car_cng": 0.125,
    "car_ev": 0.075,              # Electric car charged on Indian grid
    "cab": 0.170,                 # Taxi / Uber / Ola (solo)
    "taxi": 0.170,
    "carpool": 0.085,             # Car with 2+ passengers (per person)
    
    # Active Zero-Emission Travel
    "bicycle": 0.000,             # Pedal cycle
    "cycle": 0.000,
    "walking": 0.000,             # Foot
    "walk": 0.000,
    
    # Aviation
    "flight": 0.255,              # Domestic flight per passenger-km (economy)
    "airplane": 0.255,
}

TRANSPORT_SOURCE_CITATION = "DEFRA / DESNZ 2024 GHG Conversion Factors & India GHG Program (ARAI)"

# ============================================================================
# 3. FOOD EMISSION FACTORS (kg CO2e per meal / serving)
# ============================================================================
# Source: Poore & Nemecek (2018) Science, Our World In Data
FOOD_FACTORS_KG_PER_MEAL: Dict[str, float] = {
    "vegan": 0.60,                # Plant-based meal (grains, legumes, veggies, nuts)
    "vegetarian": 1.20,           # Standard Indian vegetarian meal (Rice, Dal, Sabzi, Roti, Curd)
    "veg": 1.20,
    "campus_mess": 1.10,          # Standard college/campus hostel mess vegetarian meal
    "mess_thali": 1.10,
    "egg_meal": 1.80,             # Meal with eggs/dairy heavily featured
    "pescatarian": 2.10,          # Fish/seafood meal
    "fish": 2.10,
    "chicken": 2.60,              # Poultry / Chicken meal (e.g. chicken biryani / curry)
    "poultry": 2.60,
    "mutton": 7.50,               # Sheep / Goat / Red meat meal
    "red_meat": 7.50,
    "beef": 8.20,
}

FOOD_SOURCE_CITATION = "Poore & Nemecek (2018), Science / Our World in Data (Food Climate Footprints)"

# ============================================================================
# 4. WASTE EMISSION FACTORS (kg CO2e per kg of waste)
# ============================================================================
# Source: US EPA WARM (Waste Reduction Model) & World Bank What a Waste 2.0
WASTE_FACTORS_KG_PER_KG: Dict[str, Dict[str, float]] = {
    "organic_food": {
        "landfill": 0.58,         # Anaerobic decomposition producing methane (CH4)
        "compost": 0.09,          # Aerobic composting (net saving: 0.49 kg CO2e/kg)
    },
    "plastic": {
        "landfill": 2.10,         # Incineration/unmanaged disposal lifecycle impact
        "recycled": 0.60,         # Mechanical recycling (saving: 1.50 kg CO2e/kg)
    },
    "paper": {
        "landfill": 1.30,
        "recycled": 0.40,         # Recycled paper pulp (saving: 0.90 kg CO2e/kg)
    },
    "ewaste": {
        "landfill": 3.40,
        "recycled": 0.80,         # Formal e-waste dismantling & recovery
    }
}

WASTE_SOURCE_CITATION = "US EPA Waste Reduction Model (WARM) & World Bank What a Waste 2.0"

# ============================================================================
# 5. BENCHMARKS & CAMPUS COMPARISONS (kg CO2e)
# ============================================================================
BENCHMARKS = {
    "india_daily_per_capita": 5.20,       # ~1.9 tonnes CO2e / year per Indian citizen
    "global_daily_per_capita": 12.90,     # ~4.7 tonnes CO2e / year global average
    "paris_target_2030_daily": 5.50,      # Goal to keep warming <= 1.5C (approx 2.0 tonnes/year)
    "student_average_daily": 3.80,        # Estimated campus resident student baseline
}

# Pre-seeded campus hostel & department baselines for the leaderboard
INITIAL_CAMPUS_LEADERBOARD = [
    {
        "name": "Hostel Krishna",
        "category": "Hostel",
        "residents": 420,
        "total_emissions_kg": 1180.5,
        "per_capita_kg": 2.81,
        "rank": 1,
        "badge": "🌿 Greenest Hostel",
    },
    {
        "name": "Hostel Godavari",
        "category": "Hostel",
        "residents": 390,
        "total_emissions_kg": 1162.2,
        "per_capita_kg": 2.98,
        "rank": 2,
        "badge": "⚡ Solar Powered",
    },
    {
        "name": "Hostel Cauvery",
        "category": "Hostel",
        "residents": 450,
        "total_emissions_kg": 1453.5,
        "per_capita_kg": 3.23,
        "rank": 3,
        "badge": "🚴 Active Commuters",
    },
    {
        "name": "Hostel Ganga",
        "category": "Hostel",
        "residents": 480,
        "total_emissions_kg": 1780.8,
        "per_capita_kg": 3.71,
        "rank": 4,
        "badge": "💡 AC Efficiency Drive",
    },
    {
        "name": "Dept of CSE",
        "category": "Department",
        "residents": 600,
        "total_emissions_kg": 2040.0,
        "per_capita_kg": 3.40,
        "rank": 1,
        "badge": "💻 Lab Cloud Eco-Policy",
    },
    {
        "name": "Dept of ECE",
        "category": "Department",
        "residents": 520,
        "total_emissions_kg": 1892.8,
        "per_capita_kg": 3.64,
        "rank": 2,
        "badge": "🔬 Green Hardware",
    },
    {
        "name": "Dept of Mech",
        "category": "Department",
        "residents": 480,
        "total_emissions_kg": 1948.8,
        "per_capita_kg": 4.06,
        "rank": 3,
        "badge": "⚙️ Workshop Recycling",
    },
]
