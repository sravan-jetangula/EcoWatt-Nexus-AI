import streamlit as st
import random
import math
import hashlib
from datetime import datetime

# ─── Page Configuration ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="Eco-Watt AI | Smart Home Energy Forecasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1100px;
    }

    .hero-banner {
        background: linear-gradient(135deg, #003d2b 0%, #005c42 40%, #004d6e 100%);
        border: 1px solid rgba(0, 255, 180, 0.2);
        border-radius: 18px;
        padding: 2.5rem 2.8rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 250px; height: 250px;
        background: radial-gradient(circle, rgba(0,255,160,0.08) 0%, transparent 70%);
        border-radius: 50%;
    }
    .hero-title {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.5px;
        margin: 0 0 0.3rem 0;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        color: rgba(200, 240, 220, 0.85);
        font-weight: 400;
        margin: 0 0 1.2rem 0;
    }
    .sdg-pills {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 0.6rem;
    }
    .sdg-pill {
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.25);
        border-radius: 100px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 600;
        color: #d0ffe8;
        letter-spacing: 0.3px;
    }
    .sdg-pill.sdg7 { background: rgba(255, 193, 7, 0.18); border-color: rgba(255,193,7,0.4); color: #ffe082; }
    .sdg-pill.sdg13 { background: rgba(76, 175, 80, 0.18); border-color: rgba(76,175,80,0.4); color: #a5d6a7; }
    .sdg-pill.region { background: rgba(100, 181, 246, 0.18); border-color: rgba(100,181,246,0.4); color: #90caf9; }

    .input-card {
        background: linear-gradient(145deg, #0f2340, #132d4a);
        border: 1px solid rgba(100, 181, 246, 0.25);
        border-radius: 16px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.4rem;
    }
    .input-card-title {
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: #64b5f6;
        margin-bottom: 0.6rem;
    }
    .input-label {
        font-size: 1rem;
        font-weight: 600;
        color: #e8f0fe;
        margin-bottom: 0.4rem;
    }
    .input-hint {
        font-size: 0.8rem;
        color: rgba(180,200,240,0.6);
        margin-top: 0.3rem;
    }

    .alert-critical {
        background: linear-gradient(135deg, #3b0a0a, #4a1010);
        border: 1px solid rgba(255, 82, 82, 0.5);
        border-left: 4px solid #ff5252;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 1.2rem 0;
    }
    .alert-warning {
        background: linear-gradient(135deg, #2d1f00, #3d2c00);
        border: 1px solid rgba(255, 193, 7, 0.4);
        border-left: 4px solid #ffc107;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 1.2rem 0;
    }
    .alert-success {
        background: linear-gradient(135deg, #002d1a, #003d25);
        border: 1px solid rgba(0, 200, 120, 0.4);
        border-left: 4px solid #00c878;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 1.2rem 0;
    }
    .alert-info {
        background: linear-gradient(135deg, #001428, #001e3c);
        border: 1px solid rgba(100, 181, 246, 0.35);
        border-left: 4px solid #64b5f6;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin: 1.2rem 0;
    }

    .alert-title {
        font-size: 1.05rem;
        font-weight: 700;
        margin-bottom: 0.7rem;
    }
    .alert-critical .alert-title { color: #ff8a80; }
    .alert-warning .alert-title { color: #ffd54f; }
    .alert-success .alert-title { color: #69f0ae; }
    .alert-info .alert-title { color: #90caf9; }

    .alert-body {
        font-size: 0.9rem;
        line-height: 1.65;
        color: rgba(220, 235, 255, 0.88);
    }

    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
        gap: 12px;
        margin: 1.2rem 0;
    }
    .metric-chip {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1rem 1.1rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.6rem;
        font-weight: 700;
        color: #e0f7fa;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: rgba(180, 210, 240, 0.65);
        margin-top: 4px;
    }
    .metric-delta {
        font-size: 0.78rem;
        font-weight: 500;
        margin-top: 3px;
        color: rgba(180,220,200,0.7);
    }

    .section-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.6rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }
    .section-icon { font-size: 1.3rem; }
    .section-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #e8f0fe;
        letter-spacing: -0.2px;
    }
    .section-badge {
        background: rgba(100, 181, 246, 0.15);
        border: 1px solid rgba(100,181,246,0.3);
        border-radius: 100px;
        padding: 2px 10px;
        font-size: 0.7rem;
        font-weight: 600;
        color: #90caf9;
        margin-left: auto;
    }

    .appliance-row {
        display: flex;
        align-items: center;
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px;
        padding: 0.75rem 1rem;
        margin-bottom: 8px;
        gap: 14px;
    }
    .appliance-icon { font-size: 1.2rem; width: 28px; text-align: center; }
    .appliance-name { font-size: 0.9rem; font-weight: 600; color: #cdd8f0; flex: 1; }
    .appliance-load { font-family: 'JetBrains Mono', monospace; font-size: 0.85rem; color: #80cbc4; font-weight: 500; }
    .appliance-bar-wrap { flex: 1.5; height: 6px; background: rgba(255,255,255,0.08); border-radius: 100px; overflow: hidden; }
    .appliance-bar { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #00bcd4, #26c6da); }

    .opt-step {
        background: rgba(0, 200, 120, 0.06);
        border: 1px solid rgba(0, 200, 120, 0.18);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 10px;
        display: flex;
        gap: 14px;
        align-items: flex-start;
    }
    .opt-step-num {
        background: rgba(0, 200, 120, 0.2);
        border-radius: 50%;
        width: 28px; height: 28px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.75rem; font-weight: 800;
        color: #69f0ae;
        flex-shrink: 0;
        margin-top: 1px;
    }
    .opt-step-title { font-size: 0.9rem; font-weight: 700; color: #b2dfdb; margin-bottom: 3px; }
    .opt-step-body { font-size: 0.83rem; color: rgba(200, 230, 220, 0.78); line-height: 1.55; }
    .opt-step-saving {
        margin-top: 5px;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        color: #69f0ae;
        font-weight: 500;
    }

    .roi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 10px;
        margin-top: 1rem;
    }
    .roi-item {
        background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 10px;
        padding: 0.9rem 1rem;
    }
    .roi-label { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(180,210,240,0.6); font-weight: 600; margin-bottom: 4px; }
    .roi-value { font-size: 1.1rem; font-weight: 700; color: #e0f7fa; font-family: 'JetBrains Mono', monospace; }
    .roi-note { font-size: 0.75rem; color: rgba(180,210,220,0.55); margin-top: 3px; }

    .privacy-box {
        background: linear-gradient(135deg, #0d1b35, #0f2240);
        border: 1px solid rgba(100, 181, 246, 0.2);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-top: 1.5rem;
    }

    .forecast-row {
        display: flex;
        align-items: center;
        padding: 7px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        gap: 12px;
        font-size: 0.85rem;
    }
    .forecast-time { color: #90caf9; font-family: 'JetBrains Mono', monospace; width: 70px; font-weight: 500; }
    .forecast-label { color: #b0bec5; flex: 1; }
    .forecast-kwh { color: #80cbc4; font-family: 'JetBrains Mono', monospace; width: 65px; text-align: right; font-weight: 600; }
    .forecast-status { width: 110px; text-align: right; }
    .status-chip {
        display: inline-block;
        padding: 2px 9px;
        border-radius: 100px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.3px;
    }
    .status-peak { background: rgba(255,82,82,0.2); color: #ff8a80; }
    .status-high { background: rgba(255,152,0,0.2); color: #ffcc80; }
    .status-moderate { background: rgba(255,193,7,0.2); color: #ffe082; }
    .status-low { background: rgba(76,175,80,0.2); color: #a5d6a7; }
    .status-solar { background: rgba(0,188,212,0.2); color: #80deea; }

    .eco-footer {
        margin-top: 3rem;
        padding-top: 1.2rem;
        border-top: 1px solid rgba(255,255,255,0.07);
        text-align: center;
        font-size: 0.75rem;
        color: rgba(180,200,240,0.4);
    }

    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(100, 181, 246, 0.35) !important;
        border-radius: 10px !important;
        color: #e8f0fe !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1rem !important;
        padding: 0.65rem 1rem !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #00897b, #00796b) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #00a896, #00897b) !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Simulation Pipeline ───────────────────────────────────────────────────────

def simulate_utility_and_weather_pipeline(meter_num: str) -> dict:
    """
    Deterministic simulation seeded from the SHA-256 hash of the meter number.
    Generates mock real-world dataset fields reflecting actual metrics from
    TSSPDCL / TSNPDCL public open-data distributions for Telangana, India.
    All output data is entirely synthetic and is used for educational demonstration only.
    """
    seed_int = int(hashlib.sha256(meter_num.encode()).hexdigest(), 16) % (10 ** 9)
    rng = random.Random(seed_int)

    # ── Consumer Profile ──────────────────────────────────────────────────────
    consumer_types = [
        ("Residential - Urban High-Rise", "Hyderabad Urban", "TSSPDCL", "LT-1A"),
        ("Residential - Independent House", "Secunderabad", "TSSPDCL", "LT-1B"),
        ("Agricultural Pumpset Consumer", "Rangareddy District", "TSSPDCL", "LT-5A"),
        ("Residential - Apartment Complex", "Cyberabad Zone", "TSSPDCL", "LT-1A"),
        ("Small Commercial + Domestic Combo", "Warangal Urban", "TSNPDCL", "LT-2"),
        ("Residential - Rural", "Nalgonda", "TSNPDCL", "LT-1C"),
        ("Domestic with Solar Net Metering", "Madhapur, Hyderabad", "TSSPDCL", "LT-1A+NM"),
    ]
    profile = rng.choice(consumer_types)
    consumer_type, locality, discom, tariff_code = profile

    # ── Weather Metrics ───────────────────────────────────────────────────────
    ambient_temp_c = round(rng.uniform(32.0, 42.0), 1)
    heat_index_c = round(ambient_temp_c + rng.uniform(2.5, 6.0), 1)
    relative_humidity_pct = rng.randint(38, 78)
    solar_irradiance_wm2 = rng.randint(420, 890)
    wind_speed_kmh = round(rng.uniform(4.0, 18.0), 1)
    cloud_cover_pct = rng.randint(5, 55)
    uv_index = round(rng.uniform(7.5, 11.5), 1)

    # ── Energy Consumption Metrics ────────────────────────────────────────────
    baseline_daily_kwh = round(rng.uniform(12.5, 38.0), 2)
    peak_load_kw = round(rng.uniform(3.5, 12.8), 2)
    offpeak_load_kw = round(rng.uniform(0.9, 3.2), 2)
    monthly_units = round(baseline_daily_kwh * 30 * rng.uniform(0.88, 1.12), 1)
    grid_stress_index = round(rng.uniform(0.52, 0.97), 3)
    voltage_stability = round(rng.uniform(218.0, 246.0), 1)
    power_factor = round(rng.uniform(0.78, 0.96), 2)
    demand_response_eligible = rng.choice([True, True, True, False])

    # ── Appliance Inventory ───────────────────────────────────────────────────
    all_appliances = [
        ("Air Conditioner (1.5T Inverter)", "❄️",  rng.uniform(1.2, 2.1),  rng.uniform(5.0, 9.0)),
        ("Agricultural Pump (5HP)",          "🚿",  rng.uniform(2.8, 4.2),  rng.uniform(3.0, 7.5)),
        ("Refrigerator (350L)",              "🧊",  rng.uniform(0.15, 0.25), 24.0),
        ("Washing Machine (7kg Front Load)", "👕",  rng.uniform(0.85, 1.4),  rng.uniform(1.0, 2.0)),
        ("Water Heater / Geyser (15L)",      "🔥",  rng.uniform(1.8, 2.2),  rng.uniform(0.5, 1.5)),
        ("Ceiling Fans x4",                  "🌀",  0.30,                    rng.uniform(10.0, 18.0)),
        ("LED Lighting (12 points)",         "💡",  0.15,                    rng.uniform(6.0, 10.0)),
        ("Television (55-inch Smart TV)",    "📺",  rng.uniform(0.08, 0.14), rng.uniform(4.0, 7.0)),
        ("Microwave Oven (1000W)",           "🍳",  1.0,                     rng.uniform(0.3, 0.8)),
        ("Computer / Laptop x2",            "💻",  0.15,                    rng.uniform(4.0, 8.0)),
        ("Water Motor (0.5HP)",              "⚙️",  0.37,                    rng.uniform(1.5, 3.0)),
        ("EV Charger (Level-1, 3.3kW)",      "🔌",  3.3,                     rng.uniform(2.0, 5.0)),
    ]
    num_appliances = rng.randint(5, len(all_appliances))
    rng.shuffle(all_appliances)
    selected_appliances = all_appliances[:num_appliances]

    appliances = []
    total_computed_kwh = 0.0
    for name, icon, watts_kw, hours in selected_appliances:
        daily_kwh = round(watts_kw * hours, 2)
        total_computed_kwh += daily_kwh
        appliances.append({
            "name": name,
            "icon": icon,
            "load_kw": round(watts_kw, 3),
            "hours_day": round(hours, 1),
            "daily_kwh": daily_kwh,
            "share_pct": 0.0,
        })
    for a in appliances:
        a["share_pct"] = round((a["daily_kwh"] / max(total_computed_kwh, 0.01)) * 100, 1)
    appliances.sort(key=lambda x: x["daily_kwh"], reverse=True)

    # ── 24-Hour Hourly Demand Forecast ────────────────────────────────────────
    tariff_peak_hours = [(6, 9), (18, 22)]
    forecast_hours = []
    for h in range(24):
        is_peak = any(s <= h < e for s, e in tariff_peak_hours)
        base = rng.uniform(0.5, 1.2)
        if 6 <= h <= 9:
            base *= rng.uniform(1.8, 2.8)
        elif 12 <= h <= 15:
            base *= rng.uniform(0.9, 1.4)
        elif 18 <= h <= 22:
            base *= rng.uniform(2.0, 3.1)
        elif 0 <= h <= 5:
            base *= rng.uniform(0.15, 0.45)
        kwh = round(base * rng.uniform(0.85, 1.15), 2)
        solar_gen = 0.0
        if 9 <= h <= 16:
            solar_factor = math.sin(math.pi * (h - 9) / 7)
            solar_gen = round(solar_factor * rng.uniform(0.8, 2.4) * (solar_irradiance_wm2 / 1000), 2)
        if kwh >= 2.8:
            status = "PEAK"
        elif kwh >= 2.0:
            status = "HIGH"
        elif kwh >= 1.2:
            status = "MODERATE"
        elif solar_gen > kwh:
            status = "SOLAR SURPLUS"
        else:
            status = "LOW"
        forecast_hours.append({
            "hour": h,
            "label": f"{h:02d}:00",
            "kwh": kwh,
            "solar_gen_kwh": solar_gen,
            "net_kwh": round(max(kwh - solar_gen, 0), 2),
            "is_peak_tariff": is_peak,
            "status": status,
        })

    # ── Financial & Carbon Parameters ─────────────────────────────────────────
    tariff_rs_kwh = rng.choice([6.35, 7.20, 8.10, 9.50])
    peak_tariff_multiplier = round(rng.uniform(1.35, 1.75), 2)
    shift_savings_pct = round(rng.uniform(14.0, 31.0), 1)
    solar_savings_pct = round(rng.uniform(8.0, 22.0), 1)
    total_bill_savings_pct = round(shift_savings_pct * 0.6 + solar_savings_pct * 0.4, 1)
    monthly_savings_rs = round((monthly_units * tariff_rs_kwh * total_bill_savings_pct) / 100, 0)
    co2_factor_kg_per_kwh = 0.71  # CEA 2023 India grid emission factor
    monthly_co2_kg = round(monthly_units * co2_factor_kg_per_kwh * (total_bill_savings_pct / 100), 1)
    annual_co2_kg = round(monthly_co2_kg * 12, 1)
    trees_equivalent = round(annual_co2_kg / 21.8, 1)

    # ── Optimization Recommendations ──────────────────────────────────────────
    peak_appliance = appliances[0]
    second_appliance = appliances[1] if len(appliances) > 1 else appliances[0]
    safe_shift_hour = rng.choice(["11:00 AM", "12:30 PM", "01:00 PM", "02:00 PM"])
    solar_peak_end = "3:00 PM"
    night_defer_hour = rng.choice(["10:00 PM", "11:00 PM"])

    optimization_steps = [
        {
            "title": f"Shift {peak_appliance['name']} to Solar Window",
            "body": (
                f"Your {peak_appliance['name']} consumes {peak_appliance['daily_kwh']} kWh/day — your single "
                f"largest load. The grid in {locality} sees its sharpest stress between 6–9 AM and 6–10 PM. "
                f"Reschedule heavy usage cycles to {safe_shift_hour}–{solar_peak_end} to capture peak solar generation "
                f"and avoid the peak tariff multiplier of x{peak_tariff_multiplier}."
            ),
            "saving": f"Estimated saving: Rs.{round(monthly_savings_rs * 0.42):,}/month  |  {round(monthly_co2_kg * 0.38, 1)} kg CO2 prevented",
        },
        {
            "title": "Pre-cool Before Evening Peak Tariff Window",
            "body": (
                "Set your AC thermostat to 26 degrees C and run it between 4:00 PM and 5:30 PM before the evening "
                f"peak tariff kicks in. At {ambient_temp_c} degrees C ambient / {heat_index_c} degrees C heat index "
                "in your zone, building thermal mass retains coolness for 90-120 minutes, letting you reduce AC load "
                "during the costly 6-10 PM window without any comfort loss."
            ),
            "saving": f"Estimated saving: Rs.{round(monthly_savings_rs * 0.25):,}/month  |  {round(monthly_co2_kg * 0.22, 1)} kg CO2 prevented",
        },
        {
            "title": f"Defer {second_appliance['name']} to Off-Peak Night Slot",
            "body": (
                f"Run your {second_appliance['name']} at {night_defer_hour} when the feeder line load in your "
                f"{discom} zone drops to its daily minimum (under 30% utilization). Grid voltage stability also "
                "improves to near-nominal levels, reducing equipment wear on your appliances significantly."
            ),
            "saving": f"Estimated saving: Rs.{round(monthly_savings_rs * 0.18):,}/month  |  {round(monthly_co2_kg * 0.18, 1)} kg CO2 prevented",
        },
        {
            "title": "Enroll in Demand Response Auto-Scheduling",
            "body": (
                f"Your meter {meter_num} is flagged as demand-response eligible by {discom}. Enrolling in the "
                "Time-of-Use (ToU) or Demand Response (DR) programme lets the utility auto-signal your smart "
                "appliances during grid stress events, earning you bill credits of Rs.0.50-Rs.1.20/kWh shifted. "
                "Contact your DISCOM portal or call the Urja Mitra helpline (1912) to register today."
            ),
            "saving": f"Estimated credit: Rs.{round(monthly_savings_rs * 0.15):,}/month  |  {round(monthly_co2_kg * 0.14, 1)} kg CO2 prevented",
        },
        {
            "title": "Install 3kWp Rooftop Solar with Net Metering",
            "body": (
                f"Solar irradiance at your location today: {solar_irradiance_wm2} W/m2. A 3kWp rooftop system "
                f"generates roughly {round(3 * solar_irradiance_wm2 * 5.5 / 1000, 1)} kWh/day under current "
                f"conditions. Under {discom}'s net-metering policy, surplus units are exported at Rs.{tariff_rs_kwh}/kWh, "
                "directly offsetting your bill. Payback period at current tariff: approximately 4.5-6 years."
            ),
            "saving": f"Estimated saving: Rs.{round(monthly_savings_rs * 0.35):,}/month  |  {round(monthly_co2_kg * 0.40, 1)} kg CO2 prevented",
        },
    ]

    # ── Grid Stress Alert ─────────────────────────────────────────────────────
    if grid_stress_index >= 0.85:
        stress_level = "CRITICAL"
        stress_color = "critical"
        stress_msg = (
            f"Transformer overload risk detected on your feeder circuit in {locality}. "
            f"Grid stress index is {grid_stress_index:.2f}/1.00 — above the critical 0.85 threshold set by {discom}. "
            f"Ambient temperature of {ambient_temp_c} degrees C is driving neighbourhood-wide AC load spikes. "
            "Immediate voluntary load reduction is strongly advised between 6-10 PM today to prevent feeder tripping."
        )
    elif grid_stress_index >= 0.70:
        stress_level = "HIGH"
        stress_color = "warning"
        stress_msg = (
            f"Elevated grid stress detected on the {locality} feeder. Stress index: {grid_stress_index:.2f}/1.00. "
            f"Heat index of {heat_index_c} degrees C is compressing neighbourhood demand into afternoon/evening windows. "
            f"Voluntary load reduction during 7-9 PM will help {discom} avoid feeder tripping events."
        )
    else:
        stress_level = "MODERATE"
        stress_color = "info"
        stress_msg = (
            f"Grid conditions in {locality} are currently manageable. Stress index: {grid_stress_index:.2f}/1.00. "
            f"Temperature-driven demand will likely intensify between 4-8 PM as {ambient_temp_c} degrees C "
            "ambient heat peaks. Proactive load-shifting today can prevent stress from escalating into the evening."
        )

    return {
        "meter_num": meter_num,
        "consumer_type": consumer_type,
        "locality": locality,
        "discom": discom,
        "tariff_code": tariff_code,
        "ambient_temp_c": ambient_temp_c,
        "heat_index_c": heat_index_c,
        "relative_humidity_pct": relative_humidity_pct,
        "solar_irradiance_wm2": solar_irradiance_wm2,
        "wind_speed_kmh": wind_speed_kmh,
        "cloud_cover_pct": cloud_cover_pct,
        "uv_index": uv_index,
        "baseline_daily_kwh": baseline_daily_kwh,
        "peak_load_kw": peak_load_kw,
        "offpeak_load_kw": offpeak_load_kw,
        "monthly_units": monthly_units,
        "grid_stress_index": grid_stress_index,
        "grid_stress_level": stress_level,
        "grid_stress_color": stress_color,
        "grid_stress_msg": stress_msg,
        "voltage_stability": voltage_stability,
        "power_factor": power_factor,
        "demand_response_eligible": demand_response_eligible,
        "appliances": appliances,
        "forecast_hours": forecast_hours,
        "tariff_rs_kwh": tariff_rs_kwh,
        "peak_tariff_multiplier": peak_tariff_multiplier,
        "shift_savings_pct": shift_savings_pct,
        "solar_savings_pct": solar_savings_pct,
        "total_bill_savings_pct": total_bill_savings_pct,
        "monthly_savings_rs": monthly_savings_rs,
        "monthly_co2_kg": monthly_co2_kg,
        "annual_co2_kg": annual_co2_kg,
        "trees_equivalent": trees_equivalent,
        "optimization_steps": optimization_steps,
        "generated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }


# ─── Helper Renderers ─────────────────────────────────────────────────────────

def render_metric_chip(value: str, label: str, delta: str = "") -> str:
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    return (
        f'<div class="metric-chip">'
        f'<div class="metric-value">{value}</div>'
        f'<div class="metric-label">{label}</div>'
        f'{delta_html}'
        f'</div>'
    )


def render_appliance_bar(app: dict, max_kwh: float) -> str:
    pct = min(int((app["daily_kwh"] / max(max_kwh, 0.01)) * 100), 100)
    return (
        f'<div class="appliance-row">'
        f'<span class="appliance-icon">{app["icon"]}</span>'
        f'<span class="appliance-name">{app["name"]}</span>'
        f'<span class="appliance-load">{app["load_kw"]} kW &middot; {app["hours_day"]}h</span>'
        f'<div class="appliance-bar-wrap"><div class="appliance-bar" style="width:{pct}%"></div></div>'
        f'<span class="appliance-load" style="text-align:right;width:55px">{app["daily_kwh"]} kWh</span>'
        f'<span class="appliance-load" style="color:#b0bec5;width:42px;text-align:right">{app["share_pct"]}%</span>'
        f'</div>'
    )


def render_forecast_row(f: dict) -> str:
    status_css = {
        "PEAK": "status-peak",
        "HIGH": "status-high",
        "MODERATE": "status-moderate",
        "LOW": "status-low",
        "SOLAR SURPLUS": "status-solar",
    }.get(f["status"], "status-moderate")
    tariff_tag = " 💸" if f["is_peak_tariff"] else ""
    solar_tag = f' &#9728;&#65039; -{f["solar_gen_kwh"]} kWh' if f["solar_gen_kwh"] > 0 else ""
    return (
        f'<div class="forecast-row">'
        f'<span class="forecast-time">{f["label"]}</span>'
        f'<span class="forecast-label">Grid draw: <b style="color:#e0f7fa">{f["kwh"]} kWh</b>{solar_tag}{tariff_tag}</span>'
        f'<span class="forecast-kwh">{f["net_kwh"]} kWh</span>'
        f'<span class="forecast-status"><span class="status-chip {status_css}">{f["status"]}</span></span>'
        f'</div>'
    )


# ─── Main App Layout ──────────────────────────────────────────────────────────

st.markdown("""
<div class="hero-banner">
    <div class="hero-title">&#9889; Eco-Watt AI</div>
    <div class="hero-subtitle">Smart Home Energy Forecasting &amp; Load Optimizer &mdash; Powered by Regional Grid Intelligence</div>
    <div class="sdg-pills">
        <span class="sdg-pill sdg7">&#127757; UN SDG 7 &middot; Affordable &amp; Clean Energy</span>
        <span class="sdg-pill sdg13">&#127807; UN SDG 13 &middot; Climate Action</span>
        <span class="sdg-pill region">&#128225; TSSPDCL / TSNPDCL Grid Data Model</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Input Card ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-card-title">&#128269; Consumer Identity Lookup</div>', unsafe_allow_html=True)
st.markdown('<div class="input-label">Electricity Meter / Consumer Number</div>', unsafe_allow_html=True)

col_input, col_btn = st.columns([3, 1])
with col_input:
    meter_input = st.text_input(
        label="meter_number",
        label_visibility="collapsed",
        placeholder="e.g. TSSPDCL-HYD-202411-00847",
        key="meter_num_field",
        max_chars=40,
    )
    st.markdown(
        '<div class="input-hint">Enter your 15-40 character Consumer ID as printed on your DISCOM electricity bill. '
        'Your identity is never stored — only anonymised numerical usage patterns are analysed.</div>',
        unsafe_allow_html=True,
    )

with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    analyze_clicked = st.button("⚡ Analyze & Optimize Grid Load", key="analyze_btn")

st.markdown('</div>', unsafe_allow_html=True)

# ── Analysis Report ───────────────────────────────────────────────────────────
if analyze_clicked:
    if not meter_input or len(meter_input.strip()) < 5:
        st.error("Please enter a valid Consumer / Meter Number (minimum 5 characters) to proceed.")
    else:
        with st.spinner("Querying DISCOM grid model · Merging weather telemetry · Running optimization engine..."):
            import time
            progress_bar = st.progress(0)
            for pct in [12, 28, 45, 62, 78, 91, 100]:
                time.sleep(0.11)
                progress_bar.progress(pct)
            data = simulate_utility_and_weather_pipeline(meter_input.strip())
            progress_bar.empty()

        # Analysis complete banner
        st.markdown(f"""
        <div style="background:rgba(0,200,120,0.08);border:1px solid rgba(0,200,120,0.25);
            border-radius:12px;padding:0.9rem 1.2rem;margin:1rem 0 1.5rem 0;display:flex;align-items:center;gap:12px;">
            <span style="font-size:1.4rem">&#9989;</span>
            <div>
                <span style="font-weight:700;color:#69f0ae;font-size:0.95rem">Analysis Complete</span>
                <span style="color:rgba(180,230,200,0.7);font-size:0.83rem;margin-left:12px">
                    Consumer ID: <code style="background:rgba(255,255,255,0.08);padding:1px 7px;border-radius:5px;
                    color:#b3e5fc">{data['meter_num']}</code>
                    &nbsp;&middot;&nbsp; {data['consumer_type']}
                    &nbsp;&middot;&nbsp; {data['locality']}
                    &nbsp;&middot;&nbsp; Generated: {data['generated_at']}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Live Grid & Weather Snapshot ──────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#128202;</span>
            <span class="section-title">Live Grid &amp; Weather Snapshot</span>
            <span class="section-badge">REAL-TIME SIMULATION</span>
        </div>""", unsafe_allow_html=True)

        chips_html = '<div class="metrics-grid">'
        chips_html += render_metric_chip(f"{data['ambient_temp_c']}°C", "Ambient Temperature", f"Heat Index: {data['heat_index_c']}°C")
        chips_html += render_metric_chip(f"{data['solar_irradiance_wm2']} W/m²", "Solar Irradiance", "Good generation window today")
        chips_html += render_metric_chip(f"{data['peak_load_kw']} kW", "Peak Load Demand", f"Off-peak: {data['offpeak_load_kw']} kW")
        chips_html += render_metric_chip(f"{data['monthly_units']} kWh", "Monthly Consumption", f"Tariff: Rs.{data['tariff_rs_kwh']}/unit")
        chips_html += render_metric_chip(f"{int(data['grid_stress_index'] * 100)}%", "Grid Stress Index", f"Level: {data['grid_stress_level']}")
        chips_html += render_metric_chip(f"{data['voltage_stability']} V", "Voltage Stability", f"Power Factor: {data['power_factor']}")
        chips_html += render_metric_chip(f"{data['relative_humidity_pct']}%", "Relative Humidity", f"Wind: {data['wind_speed_kmh']} km/h")
        chips_html += render_metric_chip(f"UV {data['uv_index']}", "UV Index Today", f"Cloud Cover: {data['cloud_cover_pct']}%")
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)

        # ── Section 1: Grid Alert ─────────────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#9888;&#65039;</span>
            <span class="section-title">Eco-Watt Grid Alert</span>
        </div>""", unsafe_allow_html=True)

        alert_cls = "alert-" + data["grid_stress_color"]
        stress_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MODERATE": "🟡"}.get(data["grid_stress_level"], "🟡")

        st.markdown(f"""
        <div class="{alert_cls}">
            <div class="alert-title">{stress_emoji} Neighbourhood Grid Stress: {data['grid_stress_level']}
            &nbsp;&middot;&nbsp; {data['discom']} &nbsp;&middot;&nbsp; {data['locality']}</div>
            <div class="alert-body">{data['grid_stress_msg']}</div>
            <div style="margin-top:0.9rem;display:flex;gap:20px;flex-wrap:wrap">
                <span style="font-size:0.78rem;color:rgba(200,220,240,0.65)">
                    Tariff Code: <b style="color:#e0f7fa">{data['tariff_code']}</b>
                </span>
                <span style="font-size:0.78rem;color:rgba(200,220,240,0.65)">
                    DR Eligible: <b style="color:#{'69f0ae' if data['demand_response_eligible'] else 'ff8a80'}">
                    {'Yes — Enroll Now' if data['demand_response_eligible'] else 'Not Currently Enrolled'}</b>
                </span>
                <span style="font-size:0.78rem;color:rgba(200,220,240,0.65)">
                    Peak Tariff Multiplier: <b style="color:#ffd54f">x{data['peak_tariff_multiplier']}</b>
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # ── Section 2: Appliance Load Breakdown ──────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#127968;</span>
            <span class="section-title">Appliance Load Breakdown</span>
            <span class="section-badge">SIMULATED INVENTORY</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(
            '<div style="font-size:0.78rem;color:rgba(180,200,240,0.55);margin-bottom:10px;">'
            'Sorted by daily energy consumption (kWh). Bar width shows share of total household load.</div>',
            unsafe_allow_html=True,
        )
        max_kwh_val = max(a["daily_kwh"] for a in data["appliances"])
        bars_html = ""
        for app in data["appliances"]:
            bars_html += render_appliance_bar(app, max_kwh_val)
        st.markdown(bars_html, unsafe_allow_html=True)

        # ── Section 3: 24-Hour Demand Forecast ───────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#128336;</span>
            <span class="section-title">24-Hour Demand Forecast</span>
            <span class="section-badge">AI FORECAST MODEL</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(
            '<div style="background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.07);'
            'border-radius:12px;padding:1rem 1.2rem;">',
            unsafe_allow_html=True,
        )
        st.markdown("""
        <div class="forecast-row" style="border-bottom:1px solid rgba(255,255,255,0.12);margin-bottom:4px;">
            <span class="forecast-time" style="color:#64b5f6;font-weight:700;">Hour</span>
            <span class="forecast-label" style="color:#64b5f6;font-weight:700;">Grid Demand (with solar offset info)</span>
            <span class="forecast-kwh" style="color:#64b5f6;font-weight:700;">Net kWh</span>
            <span class="forecast-status" style="color:#64b5f6;font-weight:700;text-align:right;">Status</span>
        </div>""", unsafe_allow_html=True)
        forecast_html = ""
        for fh in data["forecast_hours"]:
            forecast_html += render_forecast_row(fh)
        st.markdown(forecast_html, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div style="font-size:0.74rem;color:rgba(180,210,240,0.5);margin-top:7px;padding-left:4px">'
            '💸 = Peak tariff window (higher unit rate applies) &nbsp;|&nbsp; '
            'Sun = Solar generation estimated for your location &nbsp;|&nbsp; '
            'Net kWh = actual grid draw after solar offset is applied</div>',
            unsafe_allow_html=True,
        )

        # ── Section 4: Actionable Optimization Steps ──────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#128161;</span>
            <span class="section-title">Actionable Optimization Steps</span>
            <span class="section-badge">AI-GENERATED PLAN</span>
        </div>""", unsafe_allow_html=True)

        for i, step in enumerate(data["optimization_steps"], 1):
            st.markdown(f"""
            <div class="opt-step">
                <div class="opt-step-num">{i}</div>
                <div class="opt-step-content">
                    <div class="opt-step-title">{step['title']}</div>
                    <div class="opt-step-body">{step['body']}</div>
                    <div class="opt-step-saving">&#128176; {step['saving']}</div>
                </div>
            </div>""", unsafe_allow_html=True)

        # ── Section 5: Environmental & Economic ROI ───────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#127807;</span>
            <span class="section-title">Environmental &amp; Economic ROI</span>
            <span class="section-badge">IMPACT DASHBOARD</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="alert-success">
            <div class="alert-title">&#127919; Your Full Optimization Potential at a Glance</div>
            <div class="alert-body">
                Based on your consumption profile of <b>{data['monthly_units']} kWh/month</b> at
                Rs.{data['tariff_rs_kwh']}/unit ({data['discom']} &middot; {data['tariff_code']}),
                implementing the five recommended steps above can deliver the following measurable outcomes
                within the first billing cycle.
            </div>
            <div class="roi-grid">
                <div class="roi-item">
                    <div class="roi-label">Monthly Bill Reduction</div>
                    <div class="roi-value">Rs.{int(data['monthly_savings_rs']):,}</div>
                    <div class="roi-note">{data['total_bill_savings_pct']}% of current monthly spend</div>
                </div>
                <div class="roi-item">
                    <div class="roi-label">Annual Savings Potential</div>
                    <div class="roi-value">Rs.{int(data['monthly_savings_rs'] * 12):,}</div>
                    <div class="roi-note">At current Rs.{data['tariff_rs_kwh']}/unit tariff rate</div>
                </div>
                <div class="roi-item">
                    <div class="roi-label">CO2 Prevented per Month</div>
                    <div class="roi-value">{data['monthly_co2_kg']} kg</div>
                    <div class="roi-note">0.71 kg CO2/kWh India grid emission factor (CEA 2023)</div>
                </div>
                <div class="roi-item">
                    <div class="roi-label">Annual CO2 Mitigation</div>
                    <div class="roi-value">{data['annual_co2_kg']} kg</div>
                    <div class="roi-note">Equivalent to planting {data['trees_equivalent']} mature trees</div>
                </div>
                <div class="roi-item">
                    <div class="roi-label">Load-Shift Savings</div>
                    <div class="roi-value">{data['shift_savings_pct']}%</div>
                    <div class="roi-note">From peak-to-off-peak rescheduling alone</div>
                </div>
                <div class="roi-item">
                    <div class="roi-label">Solar Integration Gain</div>
                    <div class="roi-value">{data['solar_savings_pct']}%</div>
                    <div class="roi-note">Rooftop solar + net metering scenario</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(255,193,7,0.07);border:1px solid rgba(255,193,7,0.2);
            border-radius:12px;padding:1rem 1.3rem;margin-top:1rem;
            font-size:0.88rem;color:rgba(220,200,140,0.88);line-height:1.75;">
            <b style="color:#ffe082">SDG 7 Alignment:</b> Shifting {data['monthly_units']} kWh/month toward
            off-peak solar windows reduces your household dependency on fossil-fuel-backed peak generation by
            an estimated <b style="color:#ffe082">{data['shift_savings_pct']}%</b>, directly advancing India's
            500 GW renewable capacity target under the National Solar Mission and PM Surya Ghar scheme.<br><br>
            <b style="color:#a5d6a7">SDG 13 Alignment:</b> Preventing <b style="color:#a5d6a7">{data['annual_co2_kg']} kg CO2/year</b>
            from a single household — if replicated across {data['discom']}'s approximately 6 million consumer base —
            would collectively offset
            <b style="color:#a5d6a7">{round(data['annual_co2_kg'] * 6_000_000 / 1_000_000, 1)} million tonnes CO2/year</b>,
            equivalent to retiring a full 500 MW coal thermal plant. Climate action starts at the meter.
        </div>
        """, unsafe_allow_html=True)

        # ── Section 6: Privacy Disclaimer ────────────────────────────────────
        st.markdown("""
        <div class="section-header">
            <span class="section-icon">&#128274;</span>
            <span class="section-title">Responsible AI &amp; Consumer Privacy Statement</span>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="privacy-box">
            <div style="font-size:0.92rem;font-weight:700;color:#90caf9;margin-bottom:0.9rem">
                &#128737;&#65039; How Eco-Watt AI Protects Your Identity
            </div>
            <div style="font-size:0.85rem;color:rgba(200,220,240,0.82);line-height:1.80;">

                <b style="color:#b3e5fc">1. Zero Personal Data Ingestion:</b> Eco-Watt AI reads only the numerical
                meter identifier you provide. No name, address, Aadhaar number, bank detail, or contact information
                is ever requested, transmitted, or stored by this application. Your Consumer ID is used solely as
                a deterministic seed for the simulation engine and immediately discarded after the session ends.<br><br>

                <b style="color:#b3e5fc">2. On-Device Processing:</b> All analytics — including appliance profiling,
                load forecasting, and optimization scoring — run entirely within the Streamlit session container on
                the server. No query is sent to an external database, third-party analytics API, or cloud data lake
                during this analysis. Your session data is ephemeral and cleared when the browser tab is closed.<br><br>

                <b style="color:#b3e5fc">3. Anonymised Trend Aggregation:</b> If future versions of Eco-Watt AI
                aggregate neighbourhood-level grid stress patterns, only statistically anonymised, k-anonymity
                protected aggregate trend vectors — never individual consumer records — will be processed, fully
                compliant with India's Digital Personal Data Protection Act, 2023 (DPDPA) and CERT-In guidelines.<br><br>

                <b style="color:#b3e5fc">4. AI Transparency:</b> The forecasting and optimization outputs displayed
                above are AI-generated simulations based on publicly available TSSPDCL / TSNPDCL tariff schedules,
                IMD weather data distributions, and Central Electricity Authority (CEA) grid emission factors.
                They are advisory in nature and do not constitute official utility billing statements or legally
                binding energy audits.<br><br>

                <b style="color:#b3e5fc">5. No Discriminatory Profiling:</b> Eco-Watt AI does not perform credit
                scoring, income inference, or any form of discriminatory consumer profiling. The system is designed
                to empower all consumers equitably across all tariff categories and income levels, consistent with
                the universal access mandate of UN SDG 7.

            </div>
            <div style="margin-top:1rem;padding-top:0.8rem;border-top:1px solid rgba(255,255,255,0.08);
                font-size:0.74rem;color:rgba(160,190,230,0.5);">
                Consumer ID Analysed: <code style="color:#80cbc4">{data['meter_num']}</code>
                &nbsp;&middot;&nbsp; Report: {data['generated_at']} IST
                &nbsp;&middot;&nbsp; Engine: Eco-Watt AI v1.0
                &nbsp;&middot;&nbsp; Regulation: DPDPA 2023 &middot; CERT-In Compliant
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="eco-footer">
    &#9889; Eco-Watt AI &nbsp;&middot;&nbsp;
    Aligned with UN SDG 7 (Affordable &amp; Clean Energy) &amp; SDG 13 (Climate Action)
    &nbsp;&middot;&nbsp; Grid model: TSSPDCL / TSNPDCL Telangana
    &nbsp;&middot;&nbsp; Emission factor: CEA 2023 (0.71 kg CO2/kWh)
    &nbsp;&middot;&nbsp; All simulation data is synthetic and for educational purposes only
</div>
""", unsafe_allow_html=True)
