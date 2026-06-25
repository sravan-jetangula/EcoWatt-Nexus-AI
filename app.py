cat > /home/claude/eco-watt-ai/app.py << 'PYEOF'
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

    html, body, [class*="css"], [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #080f1e !important;
    }

    [data-testid="stAppViewContainer"] > .main {
        background-color: #080f1e !important;
    }

    section[data-testid="stSidebar"] {
        background-color: #080f1e !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 3rem !important;
        max-width: 1120px !important;
    }

    /* Force all Streamlit default text to be bright */
    p, span, div, label {
        color: #dce8f8;
    }

    /* ── Hero Banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #013d2e 0%, #015c42 45%, #013d5e 100%);
        border: 1px solid rgba(0, 255, 160, 0.22);
        border-radius: 18px;
        padding: 2.4rem 2.6rem;
        margin-bottom: 1.8rem;
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50px; right: -50px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(0,255,160,0.09) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-title {
        font-size: 2.35rem;
        font-weight: 800;
        color: #ffffff !important;
        letter-spacing: -0.5px;
        margin: 0 0 0.25rem 0;
        line-height: 1.15;
    }
    .hero-subtitle {
        font-size: 1.0rem;
        color: rgba(200, 245, 225, 0.90) !important;
        font-weight: 400;
        margin: 0 0 1.1rem 0;
    }
    .sdg-pills { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 0.5rem; }
    .sdg-pill {
        border-radius: 100px;
        padding: 4px 14px;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.2px;
    }
    .sdg7  { background: rgba(255,193,7,0.20);  border: 1px solid rgba(255,193,7,0.50);  color: #ffe57f !important; }
    .sdg13 { background: rgba(76,175,80,0.20);  border: 1px solid rgba(76,175,80,0.50);  color: #b9f6ca !important; }
    .regi  { background: rgba(100,181,246,0.20); border: 1px solid rgba(100,181,246,0.50); color: #b3e5fc !important; }

    /* ── Input Card ── */
    .input-card {
        background: linear-gradient(145deg, #0c1e38, #102840);
        border: 1px solid rgba(100, 181, 246, 0.28);
        border-radius: 16px;
        padding: 1.7rem 2rem;
        margin-bottom: 1.4rem;
    }
    .input-card-title {
        font-size: 0.73rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.6px;
        color: #64b5f6 !important;
        margin-bottom: 0.55rem;
    }
    .input-label {
        font-size: 1.0rem;
        font-weight: 600;
        color: #e8f4ff !important;
        margin-bottom: 0.35rem;
    }
    .input-hint {
        font-size: 0.8rem;
        color: rgba(180, 210, 250, 0.65) !important;
        margin-top: 0.4rem;
        line-height: 1.5;
    }

    /* ── Section Headers ── */
    .sec-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 1.9rem 0 0.95rem 0;
        padding-bottom: 0.55rem;
        border-bottom: 1px solid rgba(255,255,255,0.10);
    }
    .sec-icon  { font-size: 1.25rem; }
    .sec-title { font-size: 1.12rem; font-weight: 700; color: #e8f4ff !important; }
    .sec-badge {
        margin-left: auto;
        background: rgba(100,181,246,0.14);
        border: 1px solid rgba(100,181,246,0.30);
        border-radius: 100px;
        padding: 2px 10px;
        font-size: 0.68rem;
        font-weight: 700;
        color: #90caf9 !important;
        letter-spacing: 0.3px;
    }

    /* ── Metrics Grid ── */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
        gap: 11px;
        margin: 1.1rem 0;
    }
    .metric-chip {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 12px;
        padding: 1rem 1.05rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.55rem;
        font-weight: 700;
        color: #e0f7fa !important;
        line-height: 1.2;
    }
    .metric-label {
        font-size: 0.70rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: rgba(178, 212, 248, 0.72) !important;
        margin-top: 5px;
    }
    .metric-sub {
        font-size: 0.76rem;
        color: rgba(178, 212, 248, 0.55) !important;
        margin-top: 3px;
    }

    /* ── Alert Boxes ── */
    .alert-critical {
        background: linear-gradient(135deg, #380a0a, #480f0f);
        border: 1px solid rgba(255,82,82,0.50);
        border-left: 4px solid #ff5252;
        border-radius: 14px;
        padding: 1.35rem 1.55rem;
        margin: 1.15rem 0;
    }
    .alert-warning {
        background: linear-gradient(135deg, #2b1d00, #3b2900);
        border: 1px solid rgba(255,193,7,0.42);
        border-left: 4px solid #ffc107;
        border-radius: 14px;
        padding: 1.35rem 1.55rem;
        margin: 1.15rem 0;
    }
    .alert-success {
        background: linear-gradient(135deg, #002918, #003822);
        border: 1px solid rgba(0,200,120,0.42);
        border-left: 4px solid #00c878;
        border-radius: 14px;
        padding: 1.35rem 1.55rem;
        margin: 1.15rem 0;
    }
    .alert-info {
        background: linear-gradient(135deg, #001225, #001a38);
        border: 1px solid rgba(100,181,246,0.36);
        border-left: 4px solid #64b5f6;
        border-radius: 14px;
        padding: 1.35rem 1.55rem;
        margin: 1.15rem 0;
    }
    .alert-title {
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }
    .alert-critical .alert-title { color: #ff8a80 !important; }
    .alert-warning  .alert-title { color: #ffd54f !important; }
    .alert-success  .alert-title { color: #69f0ae !important; }
    .alert-info     .alert-title { color: #90caf9 !important; }
    .alert-body {
        font-size: 0.90rem;
        line-height: 1.68;
        color: rgba(224, 238, 255, 0.92) !important;
    }
    .alert-meta {
        margin-top: 0.85rem;
        display: flex;
        gap: 20px;
        flex-wrap: wrap;
        font-size: 0.78rem;
        color: rgba(200,222,250,0.65) !important;
    }
    .alert-meta b { color: #e0f0ff !important; }

    /* ── Appliance Rows ── */
    .appliance-row {
        display: flex;
        align-items: center;
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 10px;
        padding: 0.72rem 1rem;
        margin-bottom: 7px;
        gap: 13px;
    }
    .app-icon  { font-size: 1.15rem; width: 26px; text-align: center; flex-shrink: 0; }
    .app-name  { font-size: 0.89rem; font-weight: 600; color: #d4e2f8 !important; flex: 1; }
    .app-spec  { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #80cbc4 !important; font-weight: 500; min-width: 110px; }
    .app-bar-wrap { flex: 1.5; height: 6px; background: rgba(255,255,255,0.09); border-radius: 100px; overflow: hidden; }
    .app-bar { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #00acc1, #26c6da); }
    .app-kwh  { font-family: 'JetBrains Mono', monospace; font-size: 0.84rem; color: #b2ebf2 !important; font-weight: 600; min-width: 58px; text-align: right; }
    .app-pct  { font-family: 'JetBrains Mono', monospace; font-size: 0.80rem; color: rgba(180,210,230,0.60) !important; min-width: 40px; text-align: right; }

    /* ── Forecast Table ── */
    .fc-table { background: rgba(255,255,255,0.025); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1rem 1.1rem; }
    .fc-header {
        display: flex; align-items: center; gap: 12px;
        padding-bottom: 7px; margin-bottom: 3px;
        border-bottom: 1px solid rgba(255,255,255,0.13);
        font-size: 0.74rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 0.6px; color: #64b5f6 !important;
    }
    .fc-row {
        display: flex; align-items: center; gap: 12px;
        padding: 6px 0;
        border-bottom: 1px solid rgba(255,255,255,0.05);
        font-size: 0.84rem;
    }
    .fc-time  { font-family: 'JetBrains Mono', monospace; color: #90caf9 !important; font-weight: 600; min-width: 52px; }
    .fc-info  { flex: 1; color: #c8daf4 !important; }
    .fc-info b { color: #e8f4ff !important; }
    .fc-net   { font-family: 'JetBrains Mono', monospace; color: #80cbc4 !important; font-weight: 700; min-width: 62px; text-align: right; }
    .fc-stat  { min-width: 105px; text-align: right; }
    .chip { display: inline-block; padding: 2px 9px; border-radius: 100px; font-size: 0.68rem; font-weight: 700; }
    .chip-peak     { background: rgba(255,82,82,0.22);   color: #ff8a80 !important; }
    .chip-high     { background: rgba(255,152,0,0.22);   color: #ffcc80 !important; }
    .chip-moderate { background: rgba(255,193,7,0.22);   color: #ffe082 !important; }
    .chip-low      { background: rgba(76,175,80,0.22);   color: #b9f6ca !important; }
    .chip-solar    { background: rgba(0,188,212,0.22);   color: #80deea !important; }

    /* ── Optimization Steps ── */
    .opt-step {
        background: rgba(0,200,120,0.065);
        border: 1px solid rgba(0,200,120,0.20);
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 10px;
        display: flex; gap: 14px; align-items: flex-start;
    }
    .opt-num {
        background: rgba(0,200,120,0.22);
        border-radius: 50%; width: 28px; height: 28px;
        display: flex; align-items: center; justify-content: center;
        font-size: 0.76rem; font-weight: 800; color: #69f0ae !important;
        flex-shrink: 0; margin-top: 1px;
    }
    .opt-title { font-size: 0.90rem; font-weight: 700; color: #b2dfdb !important; margin-bottom: 4px; }
    .opt-body  { font-size: 0.84rem; color: rgba(210, 235, 225, 0.85) !important; line-height: 1.58; }
    .opt-save  { margin-top: 6px; font-size: 0.76rem; font-family: 'JetBrains Mono', monospace; color: #69f0ae !important; font-weight: 600; }

    /* ── ROI Grid ── */
    .roi-grid  { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 1rem; }
    .roi-card  { background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.10); border-radius: 10px; padding: 0.9rem 1rem; }
    .roi-label { font-size: 0.70rem; text-transform: uppercase; letter-spacing: 0.8px; color: rgba(178,210,248,0.62) !important; font-weight: 700; margin-bottom: 4px; }
    .roi-value { font-size: 1.12rem; font-weight: 700; color: #e0f7fa !important; font-family: 'JetBrains Mono', monospace; }
    .roi-note  { font-size: 0.74rem; color: rgba(178,210,230,0.58) !important; margin-top: 3px; }

    /* ── SDG Impact Box ── */
    .sdg-impact {
        background: rgba(255,193,7,0.07);
        border: 1px solid rgba(255,193,7,0.22);
        border-radius: 12px;
        padding: 1rem 1.3rem;
        margin-top: 1rem;
        font-size: 0.88rem;
        line-height: 1.78;
        color: rgba(230, 215, 165, 0.92) !important;
    }
    .sdg-impact .lbl7  { color: #ffe57f !important; font-weight: 700; }
    .sdg-impact .lbl13 { color: #b9f6ca !important; font-weight: 700; }
    .sdg-impact .val   { font-weight: 700; }

    /* ── Privacy Box ── */
    .priv-box {
        background: linear-gradient(135deg, #0a1830, #0d2040);
        border: 1px solid rgba(100,181,246,0.22);
        border-radius: 14px;
        padding: 1.5rem 1.8rem;
        margin-top: 0.5rem;
    }
    .priv-heading {
        font-size: 0.92rem;
        font-weight: 700;
        color: #90caf9 !important;
        margin-bottom: 1rem;
    }
    .priv-item {
        margin-bottom: 0.9rem;
        font-size: 0.86rem;
        line-height: 1.78;
        color: rgba(210, 228, 255, 0.88) !important;
    }
    .priv-label {
        font-weight: 700;
        color: #b3e5fc !important;
    }
    .priv-footer {
        margin-top: 1rem;
        padding-top: 0.75rem;
        border-top: 1px solid rgba(255,255,255,0.09);
        font-size: 0.73rem;
        color: rgba(160,195,240,0.52) !important;
    }
    .priv-footer code { color: #80cbc4 !important; background: rgba(255,255,255,0.07); padding: 1px 6px; border-radius: 4px; }

    /* ── Complete Banner ── */
    .done-banner {
        background: rgba(0,200,120,0.09);
        border: 1px solid rgba(0,200,120,0.28);
        border-radius: 12px;
        padding: 0.85rem 1.2rem;
        margin: 1rem 0 1.5rem 0;
        display: flex; align-items: center; gap: 12px;
        font-size: 0.88rem;
    }
    .done-banner .done-ok  { font-size: 1.35rem; }
    .done-banner .done-ttl { font-weight: 700; color: #69f0ae !important; font-size: 0.96rem; }
    .done-banner .done-sub { color: rgba(180,235,210,0.72) !important; margin-left: 10px; }
    .done-banner code      { background: rgba(255,255,255,0.09); padding: 1px 7px; border-radius: 5px; color: #b3e5fc !important; font-family: 'JetBrains Mono', monospace; }

    /* ── Footer ── */
    .eco-footer {
        margin-top: 3rem;
        padding-top: 1.1rem;
        border-top: 1px solid rgba(255,255,255,0.08);
        text-align: center;
        font-size: 0.74rem;
        color: rgba(170,200,245,0.42) !important;
    }

    /* ── Forecast legend ── */
    .fc-legend {
        font-size: 0.73rem;
        color: rgba(170,200,245,0.52) !important;
        margin-top: 7px;
        padding-left: 2px;
    }

    /* ── Streamlit widget overrides ── */
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid rgba(100,181,246,0.38) !important;
        border-radius: 10px !important;
        color: #e8f4ff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.0rem !important;
        padding: 0.65rem 1rem !important;
    }
    .stTextInput > div > div > input::placeholder {
        color: rgba(140,175,220,0.45) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: rgba(100,181,246,0.72) !important;
        box-shadow: 0 0 0 2px rgba(100,181,246,0.14) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #007a6e, #006b60) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.65rem 1.5rem !important;
        font-weight: 700 !important;
        font-size: 0.93rem !important;
        width: 100% !important;
        letter-spacing: 0.1px !important;
        transition: all 0.18s ease !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #009688, #007a6e) !important;
        box-shadow: 0 4px 18px rgba(0,150,136,0.38) !important;
    }
    [data-testid="stSpinner"] { color: #69f0ae !important; }
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #00897b, #26c6da) !important;
        border-radius: 100px !important;
    }
</style>
""", unsafe_allow_html=True)


# ─── Simulation Pipeline ───────────────────────────────────────────────────────
def simulate_utility_and_weather_pipeline(meter_num: str) -> dict:
    """
    Deterministic simulation seeded from the SHA-256 hash of the meter number.
    Generates mock real-world dataset fields reflecting actual metrics from
    TSSPDCL / TSNPDCL public open-data distributions for Telangana, India.
    All output data is entirely synthetic for educational demonstration only.
    """
    seed_int = int(hashlib.sha256(meter_num.encode()).hexdigest(), 16) % (10 ** 9)
    rng = random.Random(seed_int)

    # ── Consumer Profile
    consumer_types = [
        ("Residential - Urban High-Rise",      "Hyderabad Urban",     "TSSPDCL", "LT-1A"),
        ("Residential - Independent House",    "Secunderabad",        "TSSPDCL", "LT-1B"),
        ("Agricultural Pumpset Consumer",      "Rangareddy District", "TSSPDCL", "LT-5A"),
        ("Residential - Apartment Complex",    "Cyberabad Zone",      "TSSPDCL", "LT-1A"),
        ("Small Commercial + Domestic Combo",  "Warangal Urban",      "TSNPDCL", "LT-2"),
        ("Residential - Rural",                "Nalgonda",            "TSNPDCL", "LT-1C"),
        ("Domestic with Solar Net Metering",   "Madhapur, Hyderabad", "TSSPDCL", "LT-1A+NM"),
    ]
    consumer_type, locality, discom, tariff_code = rng.choice(consumer_types)

    # ── Weather
    ambient_temp_c        = round(rng.uniform(32.0, 42.0), 1)
    heat_index_c          = round(ambient_temp_c + rng.uniform(2.5, 6.0), 1)
    relative_humidity_pct = rng.randint(38, 78)
    solar_irradiance_wm2  = rng.randint(420, 890)
    wind_speed_kmh        = round(rng.uniform(4.0, 18.0), 1)
    cloud_cover_pct       = rng.randint(5, 55)
    uv_index              = round(rng.uniform(7.5, 11.5), 1)

    # ── Energy Metrics
    baseline_daily_kwh   = round(rng.uniform(12.5, 38.0), 2)
    peak_load_kw         = round(rng.uniform(3.5, 12.8), 2)
    offpeak_load_kw      = round(rng.uniform(0.9, 3.2), 2)
    monthly_units        = round(baseline_daily_kwh * 30 * rng.uniform(0.88, 1.12), 1)
    grid_stress_index    = round(rng.uniform(0.52, 0.97), 3)
    voltage_stability    = round(rng.uniform(218.0, 246.0), 1)
    power_factor         = round(rng.uniform(0.78, 0.96), 2)
    demand_response_ok   = rng.choice([True, True, True, False])

    # ── Appliance Inventory
    all_appliances = [
        ("Air Conditioner (1.5T Inverter)", "❄️",  rng.uniform(1.2, 2.1),  rng.uniform(5.0, 9.0)),
        ("Agricultural Pump (5HP)",         "🚿",  rng.uniform(2.8, 4.2),  rng.uniform(3.0, 7.5)),
        ("Refrigerator (350L)",             "🧊",  rng.uniform(0.15, 0.25), 24.0),
        ("Washing Machine (7kg)",           "👕",  rng.uniform(0.85, 1.4),  rng.uniform(1.0, 2.0)),
        ("Water Heater / Geyser (15L)",     "🔥",  rng.uniform(1.8, 2.2),  rng.uniform(0.5, 1.5)),
        ("Ceiling Fans x4",                 "🌀",  0.30,                    rng.uniform(10.0, 18.0)),
        ("LED Lighting (12 points)",        "💡",  0.15,                    rng.uniform(6.0, 10.0)),
        ("Television (55-inch Smart TV)",   "📺",  rng.uniform(0.08, 0.14), rng.uniform(4.0, 7.0)),
        ("Microwave Oven (1000W)",          "🍳",  1.0,                     rng.uniform(0.3, 0.8)),
        ("Computer / Laptop x2",           "💻",  0.15,                    rng.uniform(4.0, 8.0)),
        ("Water Motor (0.5HP)",             "⚙️",  0.37,                    rng.uniform(1.5, 3.0)),
        ("EV Charger (Level-1, 3.3kW)",     "🔌",  3.3,                     rng.uniform(2.0, 5.0)),
    ]
    num_appliances = rng.randint(5, len(all_appliances))
    rng.shuffle(all_appliances)
    selected = all_appliances[:num_appliances]

    appliances = []
    total_kwh = 0.0
    for name, icon, kw, hrs in selected:
        dkwh = round(kw * hrs, 2)
        total_kwh += dkwh
        appliances.append({"name": name, "icon": icon, "load_kw": round(kw, 3),
                           "hours_day": round(hrs, 1), "daily_kwh": dkwh, "share_pct": 0.0})
    for a in appliances:
        a["share_pct"] = round((a["daily_kwh"] / max(total_kwh, 0.01)) * 100, 1)
    appliances.sort(key=lambda x: x["daily_kwh"], reverse=True)

    # ── 24-Hour Forecast
    peak_windows = [(6, 9), (18, 22)]
    forecast_hours = []
    for h in range(24):
        is_peak = any(s <= h < e for s, e in peak_windows)
        base = rng.uniform(0.5, 1.2)
        if   6 <= h <= 9:  base *= rng.uniform(1.8, 2.8)
        elif 12 <= h <= 15: base *= rng.uniform(0.9, 1.4)
        elif 18 <= h <= 22: base *= rng.uniform(2.0, 3.1)
        elif 0 <= h <= 5:   base *= rng.uniform(0.15, 0.45)
        kwh = round(base * rng.uniform(0.85, 1.15), 2)
        solar = 0.0
        if 9 <= h <= 16:
            sf = math.sin(math.pi * (h - 9) / 7)
            solar = round(sf * rng.uniform(0.8, 2.4) * (solar_irradiance_wm2 / 1000), 2)
        if   kwh >= 2.8:       status = "PEAK"
        elif kwh >= 2.0:       status = "HIGH"
        elif kwh >= 1.2:       status = "MODERATE"
        elif solar > kwh:      status = "SOLAR SURPLUS"
        else:                  status = "LOW"
        forecast_hours.append({
            "label": f"{h:02d}:00", "kwh": kwh, "solar": solar,
            "net_kwh": round(max(kwh - solar, 0), 2),
            "is_peak": is_peak, "status": status,
        })

    # ── Financial & Carbon
    tariff        = rng.choice([6.35, 7.20, 8.10, 9.50])
    peak_mult     = round(rng.uniform(1.35, 1.75), 2)
    shift_pct     = round(rng.uniform(14.0, 31.0), 1)
    solar_pct     = round(rng.uniform(8.0, 22.0), 1)
    total_save_pct= round(shift_pct * 0.6 + solar_pct * 0.4, 1)
    monthly_rs    = round((monthly_units * tariff * total_save_pct) / 100, 0)
    co2_month_kg  = round(monthly_units * 0.71 * (total_save_pct / 100), 1)
    co2_year_kg   = round(co2_month_kg * 12, 1)
    trees         = round(co2_year_kg / 21.8, 1)

    # ── Optimization Steps
    pa  = appliances[0]
    pa2 = appliances[1] if len(appliances) > 1 else appliances[0]
    shift_hr  = rng.choice(["11:00 AM", "12:30 PM", "01:00 PM", "02:00 PM"])
    night_hr  = rng.choice(["10:00 PM", "11:00 PM"])

    opt_steps = [
        {
            "title": f"Shift {pa['name']} to the Solar Generation Window",
            "body": (
                f"Your {pa['name']} consumes {pa['daily_kwh']} kWh/day — your single largest load. "
                f"The grid in {locality} sees sharpest stress between 6–9 AM and 6–10 PM. "
                f"Reschedule heavy cycles to {shift_hr}–3:00 PM to capture peak solar and avoid the "
                f"peak tariff multiplier of x{peak_mult}."
            ),
            "saving": f"Rs.{round(monthly_rs * 0.42):,}/month  ·  {round(co2_month_kg * 0.38, 1)} kg CO2 prevented",
        },
        {
            "title": "Pre-cool Your Home Before the Evening Peak Tariff Window",
            "body": (
                f"Run your AC at 26°C between 4:00 PM–5:30 PM before the evening peak tariff kicks in. "
                f"At {ambient_temp_c}°C ambient / {heat_index_c}°C heat index, building thermal mass retains "
                "coolness for 90–120 minutes, letting you cut AC load during the costly 6–10 PM band "
                "with zero comfort loss."
            ),
            "saving": f"Rs.{round(monthly_rs * 0.25):,}/month  ·  {round(co2_month_kg * 0.22, 1)} kg CO2 prevented",
        },
        {
            "title": f"Defer {pa2['name']} to the Off-Peak Night Slot",
            "body": (
                f"Run your {pa2['name']} at {night_hr} when the feeder line load in your "
                f"{discom} zone drops to its daily minimum (under 30% utilization). Grid voltage "
                "stabilizes to near-nominal levels, also reducing wear on appliance components."
            ),
            "saving": f"Rs.{round(monthly_rs * 0.18):,}/month  ·  {round(co2_month_kg * 0.18, 1)} kg CO2 prevented",
        },
        {
            "title": "Enroll in Demand Response Auto-Scheduling",
            "body": (
                f"Meter {meter_num} is flagged demand-response eligible by {discom}. Enrolling in the "
                "Time-of-Use (ToU) or DR programme lets the utility auto-signal your smart appliances "
                "during stress events, earning credits of Rs.0.50–Rs.1.20/kWh shifted. "
                "Call Urja Mitra helpline 1912 to register today."
            ),
            "saving": f"Rs.{round(monthly_rs * 0.15):,}/month  ·  {round(co2_month_kg * 0.14, 1)} kg CO2 prevented",
        },
        {
            "title": "Install 3 kWp Rooftop Solar + Net Metering",
            "body": (
                f"Solar irradiance today: {solar_irradiance_wm2} W/m². A 3 kWp system generates roughly "
                f"{round(3 * solar_irradiance_wm2 * 5.5 / 1000, 1)} kWh/day under current conditions. "
                f"Under {discom}'s net-metering policy, surplus is exported at Rs.{tariff}/kWh. "
                "Payback period: approximately 4.5–6 years."
            ),
            "saving": f"Rs.{round(monthly_rs * 0.35):,}/month  ·  {round(co2_month_kg * 0.40, 1)} kg CO2 prevented",
        },
    ]

    # ── Grid Stress Alert
    if grid_stress_index >= 0.85:
        sl, sc = "CRITICAL", "critical"
        smsg = (
            f"Transformer overload risk on your feeder in {locality}. "
            f"Grid stress index {grid_stress_index:.2f}/1.00 — above the 0.85 critical threshold set by {discom}. "
            f"Ambient temperature of {ambient_temp_c}°C is driving neighbourhood-wide AC load spikes. "
            "Immediate voluntary load reduction strongly advised between 6–10 PM today."
        )
    elif grid_stress_index >= 0.70:
        sl, sc = "HIGH", "warning"
        smsg = (
            f"Elevated grid stress on the {locality} feeder. Stress index: {grid_stress_index:.2f}/1.00. "
            f"Heat index of {heat_index_c}°C is compressing demand into afternoon/evening windows. "
            f"Voluntary load reduction during 7–9 PM will help {discom} avoid feeder tripping."
        )
    else:
        sl, sc = "MODERATE", "info"
        smsg = (
            f"Grid conditions in {locality} are currently manageable. Stress index: {grid_stress_index:.2f}/1.00. "
            f"Temperature-driven demand will intensify between 4–8 PM as {ambient_temp_c}°C ambient heat peaks. "
            "Proactive load-shifting today prevents stress from escalating into the evening."
        )

    return {
        "meter_num": meter_num, "consumer_type": consumer_type,
        "locality": locality, "discom": discom, "tariff_code": tariff_code,
        "ambient_temp_c": ambient_temp_c, "heat_index_c": heat_index_c,
        "relative_humidity_pct": relative_humidity_pct, "solar_irradiance_wm2": solar_irradiance_wm2,
        "wind_speed_kmh": wind_speed_kmh, "cloud_cover_pct": cloud_cover_pct, "uv_index": uv_index,
        "baseline_daily_kwh": baseline_daily_kwh, "peak_load_kw": peak_load_kw,
        "offpeak_load_kw": offpeak_load_kw, "monthly_units": monthly_units,
        "grid_stress_index": grid_stress_index, "stress_level": sl, "stress_color": sc, "stress_msg": smsg,
        "voltage_stability": voltage_stability, "power_factor": power_factor,
        "demand_response_ok": demand_response_ok, "appliances": appliances,
        "forecast_hours": forecast_hours, "tariff": tariff, "peak_mult": peak_mult,
        "shift_pct": shift_pct, "solar_pct": solar_pct, "total_save_pct": total_save_pct,
        "monthly_rs": monthly_rs, "co2_month_kg": co2_month_kg,
        "co2_year_kg": co2_year_kg, "trees": trees, "opt_steps": opt_steps,
        "generated_at": datetime.now().strftime("%d %b %Y, %I:%M %p"),
    }


# ─── Helpers ──────────────────────────────────────────────────────────────────
def metric_chip(val, label, sub=""):
    sub_html = f'<div class="metric-sub">{sub}</div>' if sub else ""
    return (f'<div class="metric-chip">'
            f'<div class="metric-value">{val}</div>'
            f'<div class="metric-label">{label}</div>{sub_html}</div>')

def app_row(a, max_kwh):
    pct = min(int(a["daily_kwh"] / max(max_kwh, 0.01) * 100), 100)
    return (f'<div class="appliance-row">'
            f'<span class="app-icon">{a["icon"]}</span>'
            f'<span class="app-name">{a["name"]}</span>'
            f'<span class="app-spec">{a["load_kw"]} kW &middot; {a["hours_day"]}h</span>'
            f'<div class="app-bar-wrap"><div class="app-bar" style="width:{pct}%"></div></div>'
            f'<span class="app-kwh">{a["daily_kwh"]} kWh</span>'
            f'<span class="app-pct">{a["share_pct"]}%</span>'
            f'</div>')

def fc_row(f):
    chip_map = {"PEAK":"chip-peak","HIGH":"chip-high","MODERATE":"chip-moderate",
                "LOW":"chip-low","SOLAR SURPLUS":"chip-solar"}
    chip_cls = chip_map.get(f["status"], "chip-moderate")
    tariff_tag = " 💸" if f["is_peak"] else ""
    solar_tag  = f' ☀️ <span style="color:#80deea;font-size:0.78rem">-{f["solar"]} kWh</span>' if f["solar"] > 0 else ""
    return (f'<div class="fc-row">'
            f'<span class="fc-time">{f["label"]}</span>'
            f'<span class="fc-info">Grid draw: <b>{f["kwh"]} kWh</b>{solar_tag}{tariff_tag}</span>'
            f'<span class="fc-net">{f["net_kwh"]} kWh</span>'
            f'<span class="fc-stat"><span class="chip {chip_cls}">{f["status"]}</span></span>'
            f'</div>')


# ─── Layout ───────────────────────────────────────────────────────────────────

# Hero
st.markdown("""
<div class="hero-banner">
  <div class="hero-title">&#9889; Eco-Watt AI</div>
  <div class="hero-subtitle">Smart Home Energy Forecasting &amp; Load Optimizer &mdash; Powered by Regional Grid Intelligence</div>
  <div class="sdg-pills">
    <span class="sdg-pill sdg7">&#127757; UN SDG 7 &middot; Affordable &amp; Clean Energy</span>
    <span class="sdg-pill sdg13">&#127807; UN SDG 13 &middot; Climate Action</span>
    <span class="sdg-pill regi">&#128225; TSSPDCL / TSNPDCL Grid Data Model</span>
  </div>
</div>
""", unsafe_allow_html=True)

# Input Card
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="input-card-title">&#128269; Consumer Identity Lookup</div>', unsafe_allow_html=True)
st.markdown('<div class="input-label">Electricity Meter / Consumer Number</div>', unsafe_allow_html=True)

col_inp, col_btn = st.columns([3, 1])
with col_inp:
    meter_input = st.text_input(
        label="meter_number", label_visibility="collapsed",
        placeholder="e.g. TSSPDCL-HYD-202411-00847",
        key="meter_num_field", max_chars=40,
    )
    st.markdown(
        '<div class="input-hint">Enter your Consumer ID as printed on your DISCOM electricity bill. '
        'Your identity is never stored — only anonymised numerical usage patterns are analysed.</div>',
        unsafe_allow_html=True)
with col_btn:
    st.markdown("<br>", unsafe_allow_html=True)
    clicked = st.button("⚡ Analyze & Optimize Grid Load", key="analyze_btn")
st.markdown('</div>', unsafe_allow_html=True)

# ── Report ────────────────────────────────────────────────────────────────────
if clicked:
    if not meter_input or len(meter_input.strip()) < 5:
        st.error("Please enter a valid Consumer / Meter Number (minimum 5 characters) to proceed.")
    else:
        with st.spinner("Querying DISCOM grid model · Merging weather telemetry · Running optimization engine..."):
            import time
            pb = st.progress(0)
            for p in [12, 28, 45, 62, 78, 91, 100]:
                time.sleep(0.11)
                pb.progress(p)
            d = simulate_utility_and_weather_pipeline(meter_input.strip())
            pb.empty()

        # Done banner
        st.markdown(f"""
        <div class="done-banner">
          <span class="done-ok">&#9989;</span>
          <div>
            <span class="done-ttl">Analysis Complete</span>
            <span class="done-sub">
              Consumer ID: <code>{d['meter_num']}</code>
              &nbsp;&middot;&nbsp; {d['consumer_type']}
              &nbsp;&middot;&nbsp; {d['locality']}
              &nbsp;&middot;&nbsp; {d['generated_at']}
            </span>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── 1. Live Snapshot
        st.markdown('<div class="sec-header"><span class="sec-icon">&#128202;</span>'
                    '<span class="sec-title">Live Grid &amp; Weather Snapshot</span>'
                    '<span class="sec-badge">REAL-TIME SIMULATION</span></div>', unsafe_allow_html=True)

        chips = '<div class="metrics-grid">'
        chips += metric_chip(f"{d['ambient_temp_c']}°C",            "Ambient Temperature",  f"Heat Index: {d['heat_index_c']}°C")
        chips += metric_chip(f"{d['solar_irradiance_wm2']} W/m²",   "Solar Irradiance",     "Good generation window")
        chips += metric_chip(f"{d['peak_load_kw']} kW",             "Peak Load Demand",     f"Off-peak: {d['offpeak_load_kw']} kW")
        chips += metric_chip(f"{d['monthly_units']} kWh",           "Monthly Consumption",  f"Tariff: Rs.{d['tariff']}/unit")
        chips += metric_chip(f"{int(d['grid_stress_index']*100)}%", "Grid Stress Index",    f"Level: {d['stress_level']}")
        chips += metric_chip(f"{d['voltage_stability']} V",         "Voltage Stability",    f"Power Factor: {d['power_factor']}")
        chips += metric_chip(f"{d['relative_humidity_pct']}%",      "Relative Humidity",    f"Wind: {d['wind_speed_kmh']} km/h")
        chips += metric_chip(f"UV {d['uv_index']}",                 "UV Index Today",       f"Cloud Cover: {d['cloud_cover_pct']}%")
        chips += '</div>'
        st.markdown(chips, unsafe_allow_html=True)

        # ── 2. Grid Alert
        st.markdown('<div class="sec-header"><span class="sec-icon">&#9888;&#65039;</span>'
                    '<span class="sec-title">Eco-Watt Grid Alert</span></div>', unsafe_allow_html=True)

        stress_emoji = {"CRITICAL": "🔴", "HIGH": "🟠", "MODERATE": "🟡"}.get(d["stress_level"], "🟡")
        dr_color = "#69f0ae" if d["demand_response_ok"] else "#ff8a80"
        dr_text  = "Yes — Enroll Now" if d["demand_response_ok"] else "Not Enrolled"

        st.markdown(f"""
        <div class="alert-{d['stress_color']}">
          <div class="alert-title">{stress_emoji} Neighbourhood Grid Stress: {d['stress_level']}
            &nbsp;&middot;&nbsp; {d['discom']} &nbsp;&middot;&nbsp; {d['locality']}</div>
          <div class="alert-body">{d['stress_msg']}</div>
          <div class="alert-meta">
            <span>Tariff Code: <b>{d['tariff_code']}</b></span>
            <span>DR Eligible: <b style="color:{dr_color}">{dr_text}</b></span>
            <span>Peak Tariff Multiplier: <b style="color:#ffd54f">x{d['peak_mult']}</b></span>
          </div>
        </div>""", unsafe_allow_html=True)

        # ── 3. Appliance Breakdown
        st.markdown('<div class="sec-header"><span class="sec-icon">&#127968;</span>'
                    '<span class="sec-title">Appliance Load Breakdown</span>'
                    '<span class="sec-badge">SIMULATED INVENTORY</span></div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:0.77rem;color:rgba(178,210,248,0.55);margin-bottom:9px;">'
                    'Sorted by daily kWh. Bar width = share of total household load.</div>', unsafe_allow_html=True)

        max_kwh_val = max(a["daily_kwh"] for a in d["appliances"])
        rows_html = "".join(app_row(a, max_kwh_val) for a in d["appliances"])
        st.markdown(rows_html, unsafe_allow_html=True)

        # ── 4. 24-Hour Forecast
        st.markdown('<div class="sec-header"><span class="sec-icon">&#128336;</span>'
                    '<span class="sec-title">24-Hour Demand Forecast</span>'
                    '<span class="sec-badge">AI FORECAST MODEL</span></div>', unsafe_allow_html=True)

        fc_html = ('<div class="fc-table">'
                   '<div class="fc-header">'
                   '<span style="min-width:52px">Hour</span>'
                   '<span style="flex:1">Grid Demand (with solar offset)</span>'
                   '<span style="min-width:62px;text-align:right">Net kWh</span>'
                   '<span style="min-width:105px;text-align:right">Status</span>'
                   '</div>')
        for fh in d["forecast_hours"]:
            fc_html += fc_row(fh)
        fc_html += '</div>'
        st.markdown(fc_html, unsafe_allow_html=True)
        st.markdown('<div class="fc-legend">💸 = Peak tariff window &nbsp;|&nbsp; '
                    '☀️ = Solar generation offset &nbsp;|&nbsp; Net kWh = grid draw after solar</div>',
                    unsafe_allow_html=True)

        # ── 5. Optimization Steps
        st.markdown('<div class="sec-header"><span class="sec-icon">&#128161;</span>'
                    '<span class="sec-title">Actionable Optimization Steps</span>'
                    '<span class="sec-badge">AI-GENERATED PLAN</span></div>', unsafe_allow_html=True)

        for i, step in enumerate(d["opt_steps"], 1):
            st.markdown(f"""
            <div class="opt-step">
              <div class="opt-num">{i}</div>
              <div>
                <div class="opt-title">{step['title']}</div>
                <div class="opt-body">{step['body']}</div>
                <div class="opt-save">&#128176; Estimated saving: {step['saving']}</div>
              </div>
            </div>""", unsafe_allow_html=True)

        # ── 6. Environmental & Economic ROI
        st.markdown('<div class="sec-header"><span class="sec-icon">&#127807;</span>'
                    '<span class="sec-title">Environmental &amp; Economic ROI</span>'
                    '<span class="sec-badge">IMPACT DASHBOARD</span></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="alert-success">
          <div class="alert-title">&#127919; Your Full Optimization Potential at a Glance</div>
          <div class="alert-body">
            Based on your profile of <b>{d['monthly_units']} kWh/month</b> at Rs.{d['tariff']}/unit
            ({d['discom']} &middot; {d['tariff_code']}), implementing all five steps above can deliver
            the following outcomes within your first billing cycle.
          </div>
          <div class="roi-grid">
            <div class="roi-card">
              <div class="roi-label">Monthly Bill Reduction</div>
              <div class="roi-value">Rs.{int(d['monthly_rs']):,}</div>
              <div class="roi-note">{d['total_save_pct']}% of current monthly spend</div>
            </div>
            <div class="roi-card">
              <div class="roi-label">Annual Savings Potential</div>
              <div class="roi-value">Rs.{int(d['monthly_rs'] * 12):,}</div>
              <div class="roi-note">At current Rs.{d['tariff']}/unit tariff</div>
            </div>
            <div class="roi-card">
              <div class="roi-label">CO2 Prevented per Month</div>
              <div class="roi-value">{d['co2_month_kg']} kg</div>
              <div class="roi-note">0.71 kg CO2/kWh India grid emission factor (CEA 2023)</div>
            </div>
            <div class="roi-card">
              <div class="roi-label">Annual CO2 Mitigation</div>
              <div class="roi-value">{d['co2_year_kg']} kg</div>
              <div class="roi-note">Equivalent to planting {d['trees']} mature trees</div>
            </div>
            <div class="roi-card">
              <div class="roi-label">Load-Shift Savings</div>
              <div class="roi-value">{d['shift_pct']}%</div>
              <div class="roi-note">From peak-to-off-peak rescheduling alone</div>
            </div>
            <div class="roi-card">
              <div class="roi-label">Solar Integration Gain</div>
              <div class="roi-value">{d['solar_pct']}%</div>
              <div class="roi-note">Rooftop solar + net metering scenario</div>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sdg-impact">
          <span class="lbl7">SDG 7 Alignment:</span> Shifting {d['monthly_units']} kWh/month toward
          off-peak solar windows reduces fossil-fuel dependency by an estimated
          <span class="val" style="color:#ffe57f">{d['shift_pct']}%</span>, directly advancing
          India's 500 GW renewable target under the National Solar Mission and PM Surya Ghar scheme.<br><br>
          <span class="lbl13">SDG 13 Alignment:</span> Preventing
          <span class="val" style="color:#b9f6ca">{d['co2_year_kg']} kg CO2/year</span> from one household —
          replicated across {d['discom']}'s ~6 million consumers — offsets
          <span class="val" style="color:#b9f6ca">{round(d['co2_year_kg'] * 6_000_000 / 1_000_000, 1)} million
          tonnes CO2/year</span>, equivalent to retiring a 500 MW coal plant.
          Climate action starts at the meter.
        </div>""", unsafe_allow_html=True)

        # ── 7. Privacy Statement
        st.markdown('<div class="sec-header"><span class="sec-icon">&#128274;</span>'
                    '<span class="sec-title">Responsible AI &amp; Consumer Privacy Statement</span>'
                    '</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="priv-box">
          <div class="priv-heading">&#128737;&#65039; How Eco-Watt AI Protects Your Identity</div>

          <div class="priv-item">
            <span class="priv-label">1. Zero Personal Data Ingestion:</span>
            Eco-Watt AI reads only the numerical meter identifier you provide. No name, address,
            Aadhaar number, bank detail, or contact information is ever requested, transmitted, or
            stored. Your Consumer ID is used solely as a deterministic seed for the simulation
            engine and discarded once the session ends.
          </div>

          <div class="priv-item">
            <span class="priv-label">2. On-Device Processing:</span>
            All analytics — appliance profiling, load forecasting, optimization scoring — run
            entirely within the Streamlit session container. No query is sent to any external
            database, third-party API, or cloud data lake. Session data is ephemeral and cleared
            when the browser tab is closed.
          </div>

          <div class="priv-item">
            <span class="priv-label">3. Anonymised Trend Aggregation:</span>
            Future aggregate analysis will use only statistically anonymised, k-anonymity protected
            trend vectors — never individual consumer records — fully compliant with India's Digital
            Personal Data Protection Act, 2023 (DPDPA) and CERT-In guidelines.
          </div>

          <div class="priv-item">
            <span class="priv-label">4. AI Transparency:</span>
            All outputs are AI-generated simulations based on publicly available TSSPDCL / TSNPDCL
            tariff schedules, IMD weather distributions, and CEA grid emission factors. They are
            advisory in nature and do not constitute official utility billing statements or legally
            binding energy audits.
          </div>

          <div class="priv-item" style="margin-bottom:0">
            <span class="priv-label">5. No Discriminatory Profiling:</span>
            Eco-Watt AI performs no credit scoring, income inference, or consumer profiling of any
            kind. The system is designed to empower consumers equitably across all tariff categories
            and income levels, consistent with the universal access mandate of UN SDG 7.
          </div>

          <div class="priv-footer">
            Consumer ID Analysed: <code>{d['meter_num']}</code>
            &nbsp;&middot;&nbsp; Report: {d['generated_at']} IST
            &nbsp;&middot;&nbsp; Engine: Eco-Watt AI v1.0
            &nbsp;&middot;&nbsp; DPDPA 2023 &middot; CERT-In Compliant
          </div>
        </div>""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="eco-footer">
  &#9889; Eco-Watt AI &nbsp;&middot;&nbsp;
  UN SDG 7 (Affordable &amp; Clean Energy) &amp; SDG 13 (Climate Action)
  &nbsp;&middot;&nbsp; Grid model: TSSPDCL / TSNPDCL Telangana
  &nbsp;&middot;&nbsp; Emission factor: CEA 2023 (0.71 kg CO2/kWh)
  &nbsp;&middot;&nbsp; All simulation data is synthetic and for educational purposes only
</div>
""", unsafe_allow_html=True)
PYEOF
echo "Done — $(wc -l < /home/claude/eco-watt-ai/app.py) lines written"


