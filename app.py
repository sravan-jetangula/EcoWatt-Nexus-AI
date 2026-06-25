import streamlit as st
import random
import math
import hashlib
from datetime import datetime
import time

st.set_page_config(
    page_title="Eco-Watt AI | Smart Home Energy Forecasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CRITICAL: Force dark background on EVERY Streamlit layer ──────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* Force dark background on ALL Streamlit containers */
html,
body,
[data-testid="stApp"],
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMainBlockContainer"],
[data-testid="block-container"],
.main,
.block-container,
section[data-testid="stSidebar"],
div[data-testid="stVerticalBlock"],
div[data-testid="stHorizontalBlock"],
[class*="css"] {
    background-color: #0b1120 !important;
    color: #e8eaf6 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Streamlit default white overrides */
.stApp { background: #0b1120 !important; }
[data-testid="stAppViewContainer"] > .main { background: #0b1120 !important; }
[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 3rem !important;
    max-width: 1080px !important;
    background: #0b1120 !important;
}

/* Override any white card backgrounds Streamlit injects */
div[data-testid="stVerticalBlock"] > div { background: transparent !important; }
div[data-testid="element-container"] { background: transparent !important; }

/* ── Hero ── */
.hero {
    background: linear-gradient(135deg, #004d35 0%, #006849 45%, #00527a 100%);
    border: 1px solid rgba(0,255,170,0.22);
    border-radius: 20px;
    padding: 2.6rem 3rem;
    margin-bottom: 1.6rem;
}
.hero-title { font-size:2.5rem; font-weight:800; color:#ffffff; letter-spacing:-0.6px; margin:0 0 0.35rem; line-height:1.1; }
.hero-sub   { font-size:1.05rem; color:rgba(220,255,240,0.90); margin:0 0 1.1rem; font-weight:400; }
.pills      { display:flex; gap:10px; flex-wrap:wrap; }
.pill       { border-radius:100px; padding:5px 14px; font-size:0.78rem; font-weight:700; letter-spacing:0.2px; }
.pill-gold  { background:rgba(255,193,7,0.22);  border:1px solid rgba(255,193,7,0.55);  color:#ffe57f; }
.pill-green { background:rgba(76,200,80,0.20);  border:1px solid rgba(100,220,100,0.50); color:#b9f6ca; }
.pill-blue  { background:rgba(100,181,246,0.20); border:1px solid rgba(100,181,246,0.50); color:#b3e5fc; }

/* ── Input card ── */
.input-card {
    background: linear-gradient(145deg, #0d1f3c, #112a4e) !important;
    border: 1px solid rgba(100,181,246,0.30);
    border-radius: 18px;
    padding: 1.8rem 2rem;
    margin-bottom: 1.4rem;
}
.card-eyebrow { font-size:0.7rem; font-weight:800; text-transform:uppercase; letter-spacing:2px; color:#64b5f6; margin-bottom:0.55rem; }
.card-label   { font-size:1rem; font-weight:700; color:#e8eaf6; margin-bottom:0.35rem; }
.card-hint    { font-size:0.79rem; color:rgba(180,210,255,0.65); line-height:1.55; margin-top:0.4rem; }

/* ── Text input override ── */
.stTextInput > div > div > input {
    background: rgba(255,255,255,0.07) !important;
    border: 1.5px solid rgba(100,181,246,0.42) !important;
    border-radius: 10px !important;
    color: #e8eaf6 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.98rem !important;
    padding: 0.65rem 1rem !important;
    caret-color: #64b5f6 !important;
}
.stTextInput > div > div > input::placeholder { color: rgba(180,210,255,0.40) !important; }
.stTextInput > div > div > input:focus {
    border-color: rgba(100,181,246,0.80) !important;
    box-shadow: 0 0 0 3px rgba(100,181,246,0.14) !important;
    outline: none !important;
}
/* Fix label color */
.stTextInput label { color: #e8eaf6 !important; }

/* ── Button ── */
.stButton > button {
    background: linear-gradient(135deg, #00897b, #00695c) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
    font-size: 0.88rem !important;
    width: 100% !important;
    padding: 0.72rem 1rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #00a896, #00897b) !important;
    box-shadow: 0 4px 20px rgba(0,137,123,0.45) !important;
}

/* ── Progress bar ── */
div[data-testid="stProgressBar"] > div { background: rgba(255,255,255,0.10) !important; }
div[data-testid="stProgressBar"] > div > div { background: linear-gradient(90deg,#00897b,#26c6da) !important; border-radius:100px !important; }
[data-testid="stStatusWidget"] { color: #e8eaf6 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #26c6da !important; }

/* ── Success banner ── */
.success-banner {
    background: rgba(0,200,120,0.10);
    border: 1px solid rgba(0,200,120,0.32);
    border-radius: 13px;
    padding: 0.9rem 1.3rem;
    margin: 1rem 0 1.6rem;
    display: flex;
    align-items: center;
    gap: 12px;
}
.sb-icon  { font-size:1.4rem; flex-shrink:0; }
.sb-title { font-size:0.96rem; font-weight:800; color:#69f0ae; }
.sb-sub   { font-size:0.82rem; color:rgba(180,240,210,0.78); margin-top:2px; }
.mono-tag {
    font-family:'JetBrains Mono',monospace; font-size:0.83rem;
    background:rgba(255,255,255,0.10); border-radius:5px;
    padding:1px 7px; color:#b3e5fc;
}

/* ── Section header ── */
.sec-hdr { display:flex; align-items:center; gap:10px; margin:2rem 0 0.9rem; padding-bottom:0.55rem; border-bottom:1px solid rgba(255,255,255,0.10); }
.sec-icon  { font-size:1.25rem; }
.sec-title { font-size:1.12rem; font-weight:800; color:#e8eaf6; }
.sec-badge { margin-left:auto; background:rgba(100,181,246,0.15); border:1px solid rgba(100,181,246,0.35); border-radius:100px; padding:2px 11px; font-size:0.68rem; font-weight:800; letter-spacing:0.5px; color:#90caf9; }

/* ── Metric chips ── */
.mgrid { display:grid; grid-template-columns:repeat(auto-fit,minmax(180px,1fr)); gap:11px; margin-bottom:0.5rem; }
.mchip { background:rgba(255,255,255,0.06); border:1px solid rgba(255,255,255,0.13); border-radius:13px; padding:1rem 1.1rem; text-align:center; }
.mval   { font-family:'JetBrains Mono',monospace; font-size:1.5rem; font-weight:700; color:#e0f7fa; line-height:1.15; }
.mlabel { font-size:0.70rem; font-weight:700; text-transform:uppercase; letter-spacing:0.9px; color:rgba(200,225,255,0.65); margin-top:4px; }
.mdelta { font-size:0.77rem; font-weight:500; color:rgba(200,230,255,0.68); margin-top:3px; }

/* ── Alert cards ── */
.alert { border-radius:14px; padding:1.35rem 1.6rem; margin:0.8rem 0; }
.alert-red   { background:linear-gradient(135deg,#3a0a0a,#4a1212); border:1px solid rgba(255,82,82,0.45);  border-left:4px solid #ff5252; }
.alert-amber { background:linear-gradient(135deg,#2c1e00,#3c2c00); border:1px solid rgba(255,193,7,0.40);  border-left:4px solid #ffc107; }
.alert-green { background:linear-gradient(135deg,#002b19,#003a24); border:1px solid rgba(0,230,118,0.35);  border-left:4px solid #00e676; }
.alert-blue  { background:linear-gradient(135deg,#001428,#001e3e); border:1px solid rgba(100,181,246,0.32); border-left:4px solid #64b5f6; }

.alert-title { font-size:1rem; font-weight:800; margin-bottom:0.65rem; }
.alert-red   .alert-title { color:#ff8a80; }
.alert-amber .alert-title { color:#ffd54f; }
.alert-green .alert-title { color:#69f0ae; }
.alert-blue  .alert-title { color:#90caf9; }
.alert-body  { font-size:0.88rem; line-height:1.72; color:rgba(235,245,255,0.92); }
.alert-meta  { margin-top:0.85rem; display:flex; gap:20px; flex-wrap:wrap; }
.alert-meta span { font-size:0.78rem; color:rgba(210,230,255,0.72); }
.alert-meta b    { color:#e8eaf6; }

/* ── Appliance rows ── */
.app-row { display:flex; align-items:center; background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09); border-radius:10px; padding:0.72rem 1rem; margin-bottom:7px; gap:12px; }
.app-icon  { font-size:1.15rem; width:26px; text-align:center; flex-shrink:0; }
.app-name  { font-size:0.88rem; font-weight:600; color:#cfd8dc; flex:1; min-width:0; }
.app-spec  { font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:#80cbc4; white-space:nowrap; }
.bar-wrap  { flex:1.4; height:6px; background:rgba(255,255,255,0.10); border-radius:100px; overflow:hidden; min-width:60px; }
.bar-fill  { height:100%; border-radius:100px; background:linear-gradient(90deg,#00bcd4,#4dd0e1); }
.app-kwh   { font-family:'JetBrains Mono',monospace; font-size:0.80rem; color:#e0f7fa; font-weight:600; white-space:nowrap; width:52px; text-align:right; }
.app-pct   { font-family:'JetBrains Mono',monospace; font-size:0.78rem; color:rgba(200,225,255,0.60); width:38px; text-align:right; }

/* ── Forecast table ── */
.fc-wrap { background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.09); border-radius:13px; padding:1rem 1.2rem; }
.fc-row  { display:flex; align-items:center; padding:6px 0; border-bottom:1px solid rgba(255,255,255,0.05); gap:10px; font-size:0.84rem; }
.fc-head { border-bottom:1px solid rgba(255,255,255,0.15) !important; padding-bottom:8px !important; margin-bottom:3px; }
.fc-time { font-family:'JetBrains Mono',monospace; width:58px; color:#90caf9; font-weight:600; flex-shrink:0; }
.fc-desc { flex:1; color:rgba(215,235,255,0.88); }
.fc-net  { font-family:'JetBrains Mono',monospace; width:64px; text-align:right; color:#80cbc4; font-weight:600; flex-shrink:0; }
.fc-stat { width:112px; text-align:right; flex-shrink:0; }
.chip    { display:inline-block; padding:2px 9px; border-radius:100px; font-size:0.67rem; font-weight:800; letter-spacing:0.4px; }
.ch-peak  { background:rgba(255,82,82,0.22);  color:#ff8a80; }
.ch-high  { background:rgba(255,152,0,0.22);  color:#ffcc80; }
.ch-mod   { background:rgba(255,235,59,0.18); color:#fff176; }
.ch-low   { background:rgba(76,175,80,0.22);  color:#a5d6a7; }
.ch-solar { background:rgba(0,188,212,0.22);  color:#80deea; }
.fc-legend { font-size:0.73rem; color:rgba(180,210,255,0.52); margin-top:8px; padding-left:2px; }

/* ── Optimization steps ── */
.opt-step  { background:rgba(0,200,120,0.07); border:1px solid rgba(0,200,120,0.22); border-radius:13px; padding:1rem 1.2rem; margin-bottom:9px; display:flex; gap:13px; align-items:flex-start; }
.opt-num   { width:28px; height:28px; border-radius:50%; background:rgba(0,200,120,0.24); display:flex; align-items:center; justify-content:center; font-size:0.74rem; font-weight:800; color:#69f0ae; flex-shrink:0; margin-top:1px; }
.opt-title { font-size:0.9rem; font-weight:800; color:#b2dfdb; margin-bottom:4px; }
.opt-body  { font-size:0.84rem; color:rgba(215,240,230,0.88); line-height:1.62; }
.opt-save  { margin-top:6px; font-size:0.76rem; font-family:'JetBrains Mono',monospace; color:#69f0ae; font-weight:600; }

/* ── ROI grid ── */
.roi-grid { display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-top:1rem; }
.roi-cell  { background:rgba(255,255,255,0.04); border:1px solid rgba(255,255,255,0.09); border-radius:11px; padding:0.9rem 1rem; }
.roi-label { font-size:0.70rem; text-transform:uppercase; letter-spacing:0.9px; color:rgba(190,215,255,0.62); font-weight:700; margin-bottom:4px; }
.roi-val   { font-size:1.12rem; font-weight:800; color:#e0f7fa; font-family:'JetBrains Mono',monospace; }
.roi-note  { font-size:0.74rem; color:rgba(180,215,235,0.58); margin-top:3px; line-height:1.4; }

/* ── SDG callout ── */
.sdg-callout { background:rgba(255,193,7,0.08); border:1px solid rgba(255,193,7,0.24); border-radius:13px; padding:1rem 1.3rem; margin-top:1rem; font-size:0.87rem; color:rgba(245,225,165,0.94); line-height:1.80; }

/* ── Privacy box ── */
.priv-box   { background:linear-gradient(135deg,#0c1c36,#0f2444); border:1px solid rgba(100,181,246,0.24); border-radius:16px; padding:1.6rem 1.9rem; }
.priv-title { font-size:0.93rem; font-weight:800; color:#90caf9; margin-bottom:1rem; }
.priv-item  { margin-bottom:0.95rem; font-size:0.86rem; color:rgba(218,232,255,0.90); line-height:1.80; }
.priv-key   { color:#b3e5fc; font-weight:700; }
.priv-foot  { margin-top:1rem; padding-top:0.8rem; border-top:1px solid rgba(255,255,255,0.09); font-size:0.73rem; color:rgba(165,195,235,0.52); }

/* ── Footer ── */
.eco-footer { margin-top:2.8rem; padding-top:1.2rem; border-top:1px solid rgba(255,255,255,0.09); text-align:center; font-size:0.74rem; color:rgba(180,205,245,0.48); line-height:1.7; }
</style>
""", unsafe_allow_html=True)


# ─── Simulation Pipeline ──────────────────────────────────────────────────────
def simulate_utility_and_weather_pipeline(meter_num: str) -> dict:
    seed = int(hashlib.sha256(meter_num.encode()).hexdigest(), 16) % (10 ** 9)
    rng = random.Random(seed)

    profiles = [
        ("Residential – Urban High-Rise",     "Hyderabad Urban",     "TSSPDCL", "LT-1A"),
        ("Residential – Independent House",   "Secunderabad",        "TSSPDCL", "LT-1B"),
        ("Agricultural Pumpset Consumer",      "Rangareddy District", "TSSPDCL", "LT-5A"),
        ("Residential – Apartment Complex",   "Cyberabad Zone",      "TSSPDCL", "LT-1A"),
        ("Small Commercial + Domestic Combo", "Warangal Urban",      "TSNPDCL", "LT-2"),
        ("Residential – Rural",               "Nalgonda",            "TSNPDCL", "LT-1C"),
        ("Domestic with Solar Net Metering",  "Madhapur, Hyderabad", "TSSPDCL", "LT-1A+NM"),
    ]
    consumer_type, locality, discom, tariff_code = rng.choice(profiles)

    temp       = round(rng.uniform(32.0, 42.0), 1)
    heat_idx   = round(temp + rng.uniform(2.5, 6.0), 1)
    humidity   = rng.randint(38, 78)
    irradiance = rng.randint(420, 890)
    wind       = round(rng.uniform(4.0, 18.0), 1)
    cloud      = rng.randint(5, 55)
    uv         = round(rng.uniform(7.5, 11.5), 1)

    daily_kwh   = round(rng.uniform(12.5, 38.0), 2)
    peak_kw     = round(rng.uniform(3.5, 12.8), 2)
    offpeak_kw  = round(rng.uniform(0.9, 3.2), 2)
    monthly_kwh = round(daily_kwh * 30 * rng.uniform(0.88, 1.12), 1)
    stress      = round(rng.uniform(0.52, 0.97), 3)
    voltage     = round(rng.uniform(218.0, 246.0), 1)
    pf          = round(rng.uniform(0.78, 0.96), 2)
    dr_ok       = rng.choice([True, True, True, False])

    pool = [
        ("Air Conditioner (1.5T Inverter)", "❄️",  rng.uniform(1.2, 2.1),  rng.uniform(5.0, 9.0)),
        ("Agricultural Pump (5HP)",         "🚿",  rng.uniform(2.8, 4.2),  rng.uniform(3.0, 7.5)),
        ("Refrigerator (350L)",             "🧊",  rng.uniform(0.15,0.25), 24.0),
        ("Washing Machine (7kg)",           "👕",  rng.uniform(0.85, 1.4), rng.uniform(1.0, 2.0)),
        ("Water Heater / Geyser (15L)",     "🔥",  rng.uniform(1.8, 2.2),  rng.uniform(0.5, 1.5)),
        ("Ceiling Fans x4",                 "🌀",  0.30,                   rng.uniform(10.0,18.0)),
        ("LED Lighting (12 points)",        "💡",  0.15,                   rng.uniform(6.0, 10.0)),
        ("Television (55-inch Smart TV)",   "📺",  rng.uniform(0.08,0.14), rng.uniform(4.0, 7.0)),
        ("Microwave Oven (1000W)",          "🍳",  1.0,                    rng.uniform(0.3, 0.8)),
        ("Computer / Laptop x2",            "💻",  0.15,                   rng.uniform(4.0, 8.0)),
        ("Water Motor (0.5HP)",             "⚙️",  0.37,                   rng.uniform(1.5, 3.0)),
        ("EV Charger (Level-1, 3.3kW)",     "🔌",  3.3,                    rng.uniform(2.0, 5.0)),
    ]
    rng.shuffle(pool)
    selected = pool[:rng.randint(5, len(pool))]
    appliances, total_kwh = [], 0.0
    for name, icon, kw, hrs in selected:
        dkwh = round(kw * hrs, 2)
        total_kwh += dkwh
        appliances.append({"name": name, "icon": icon, "kw": round(kw,3), "hrs": round(hrs,1), "dkwh": dkwh, "pct": 0.0})
    for a in appliances:
        a["pct"] = round(a["dkwh"] / max(total_kwh, 0.01) * 100, 1)
    appliances.sort(key=lambda x: x["dkwh"], reverse=True)

    forecast = []
    for h in range(24):
        is_peak_tariff = (6 <= h < 9) or (18 <= h < 22)
        base = rng.uniform(0.5, 1.2)
        if   6 <= h <= 9:  base *= rng.uniform(1.8, 2.8)
        elif 12 <= h <= 15: base *= rng.uniform(0.9, 1.4)
        elif 18 <= h <= 22: base *= rng.uniform(2.0, 3.1)
        elif 0 <= h <= 5:  base *= rng.uniform(0.15,0.45)
        kwh = round(base * rng.uniform(0.85, 1.15), 2)
        solar = 0.0
        if 9 <= h <= 16:
            solar = round(math.sin(math.pi*(h-9)/7) * rng.uniform(0.8,2.4) * (irradiance/1000), 2)
        if kwh >= 2.8:      status = "PEAK"
        elif kwh >= 2.0:    status = "HIGH"
        elif kwh >= 1.2:    status = "MODERATE"
        elif solar > kwh:   status = "SOLAR SURPLUS"
        else:               status = "LOW"
        forecast.append({"h":h,"label":f"{h:02d}:00","kwh":kwh,"solar":solar,
                          "net":round(max(kwh-solar,0),2),"peak_tariff":is_peak_tariff,"status":status})

    tariff    = rng.choice([6.35, 7.20, 8.10, 9.50])
    peak_mult = round(rng.uniform(1.35, 1.75), 2)
    shift_pct = round(rng.uniform(14.0, 31.0), 1)
    solar_pct = round(rng.uniform(8.0, 22.0), 1)
    total_pct = round(shift_pct * 0.6 + solar_pct * 0.4, 1)
    save_rs   = round(monthly_kwh * tariff * total_pct / 100, 0)
    co2_mo    = round(monthly_kwh * 0.71 * total_pct / 100, 1)
    co2_yr    = round(co2_mo * 12, 1)
    trees     = round(co2_yr / 21.8, 1)

    top = appliances[0]
    sec = appliances[1] if len(appliances) > 1 else appliances[0]
    shift_hr = rng.choice(["11:00 AM","12:30 PM","01:00 PM","02:00 PM"])
    night_hr = rng.choice(["10:00 PM","11:00 PM"])

    steps = [
        {"title": f"Shift {top['name']} to the Solar Generation Window",
         "body": (f"Your {top['name']} draws {top['dkwh']} kWh/day — your single largest load. "
                  f"The {discom} feeder in {locality} peaks sharply between 6–9 AM and 6–10 PM. "
                  f"Reschedule heavy cycles to {shift_hr}–3:00 PM to capture free solar energy "
                  f"and avoid the peak tariff multiplier of x{peak_mult}."),
         "save": f"Rs.{round(save_rs*0.42):,}/month saved  |  {round(co2_mo*0.38,1)} kg CO₂ prevented"},
        {"title": "Pre-cool the Building Before the Evening Peak Window",
         "body": (f"Run AC at 26°C between 4:00 PM–5:30 PM before peak tariff starts at 6 PM. "
                  f"At {temp}°C ambient ({heat_idx}°C heat index), building thermal mass retains coolness "
                  "for 90–120 minutes, letting you coast through the 6–10 PM window without discomfort."),
         "save": f"Rs.{round(save_rs*0.25):,}/month saved  |  {round(co2_mo*0.22,1)} kg CO₂ prevented"},
        {"title": f"Defer {sec['name']} to the Off-Peak Night Slot",
         "body": (f"Schedule {sec['name']} at {night_hr} when the {discom} feeder load drops below "
                  "30% utilization. Grid voltage stabilizes to near-nominal overnight, also reducing "
                  "wear on motor windings and compressor components."),
         "save": f"Rs.{round(save_rs*0.18):,}/month saved  |  {round(co2_mo*0.18,1)} kg CO₂ prevented"},
        {"title": "Enroll in the Demand Response (DR) Programme",
         "body": (f"Meter {meter_num} qualifies for {discom}'s Time-of-Use Demand Response scheme. "
                  "Allowing the utility to auto-signal load shifts during grid stress earns bill credits "
                  "of Rs.0.50–Rs.1.20/kWh shifted. Register via DISCOM portal or call Urja Mitra: 1912."),
         "save": f"Rs.{round(save_rs*0.15):,}/month credit  |  {round(co2_mo*0.14,1)} kg CO₂ prevented"},
        {"title": "Install a 3 kWp Rooftop Solar System with Net Metering",
         "body": (f"Today's solar irradiance: {irradiance} W/m². A 3 kWp array generates "
                  f"~{round(3*irradiance*5.5/1000,1)} kWh/day. Under {discom}'s net-metering policy, "
                  f"surplus units export at Rs.{tariff}/kWh. Estimated payback: 4.5–6 years."),
         "save": f"Rs.{round(save_rs*0.35):,}/month saved  |  {round(co2_mo*0.40,1)} kg CO₂ prevented"},
    ]

    if stress >= 0.85:
        slevel, scolor = "CRITICAL", "red"
        smsg = (f"Transformer overload risk on the {locality} feeder. Stress index: {stress:.2f}/1.00 — "
                f"above {discom}'s critical threshold of 0.85. Ambient {temp}°C is driving neighbourhood AC spikes. "
                "Voluntary reduction between 6–10 PM is strongly advised today.")
    elif stress >= 0.70:
        slevel, scolor = "HIGH", "amber"
        smsg = (f"Elevated stress on the {locality} feeder. Index: {stress:.2f}/1.00. "
                f"Heat index of {heat_idx}°C is concentrating demand into afternoon/evening windows. "
                f"Voluntary load reduction during 7–9 PM will help {discom} avoid feeder tripping.")
    else:
        slevel, scolor = "MODERATE", "blue"
        smsg = (f"Grid conditions in {locality} are currently manageable. Index: {stress:.2f}/1.00. "
                f"Temperature-driven demand will intensify between 4–8 PM as {temp}°C heat peaks. "
                "Proactive load-shifting now prevents escalation this evening.")

    return dict(
        meter=meter_num, consumer_type=consumer_type, locality=locality,
        discom=discom, tariff_code=tariff_code,
        temp=temp, heat_idx=heat_idx, humidity=humidity, irradiance=irradiance,
        wind=wind, cloud=cloud, uv=uv,
        daily_kwh=daily_kwh, peak_kw=peak_kw, offpeak_kw=offpeak_kw,
        monthly_kwh=monthly_kwh, stress=stress, slevel=slevel, scolor=scolor, smsg=smsg,
        voltage=voltage, pf=pf, dr_ok=dr_ok,
        appliances=appliances, forecast=forecast,
        tariff=tariff, peak_mult=peak_mult,
        shift_pct=shift_pct, solar_pct=solar_pct, total_pct=total_pct,
        save_rs=save_rs, co2_mo=co2_mo, co2_yr=co2_yr, trees=trees, steps=steps,
        ts=datetime.now().strftime("%d %b %Y, %I:%M %p"),
    )


# ─── HTML helpers ─────────────────────────────────────────────────────────────
def mchip(val, label, delta=""):
    d = f'<div class="mdelta">{delta}</div>' if delta else ""
    return f'<div class="mchip"><div class="mval">{val}</div><div class="mlabel">{label}</div>{d}</div>'

def app_row(a, max_kwh):
    pct = min(int(a["dkwh"] / max(max_kwh, 0.01) * 100), 100)
    return (f'<div class="app-row"><span class="app-icon">{a["icon"]}</span>'
            f'<span class="app-name">{a["name"]}</span>'
            f'<span class="app-spec">{a["kw"]} kW &middot; {a["hrs"]}h</span>'
            f'<div class="bar-wrap"><div class="bar-fill" style="width:{pct}%"></div></div>'
            f'<span class="app-kwh">{a["dkwh"]} kWh</span>'
            f'<span class="app-pct">{a["pct"]}%</span></div>')

def fc_row(f, head=False):
    if head:
        return ('<div class="fc-row fc-head">'
                '<span class="fc-time" style="color:#64b5f6;font-weight:800">Hour</span>'
                '<span class="fc-desc" style="color:#64b5f6;font-weight:800">Grid Demand</span>'
                '<span class="fc-net"  style="color:#64b5f6;font-weight:800">Net kWh</span>'
                '<span class="fc-stat" style="color:#64b5f6;font-weight:800;text-align:right">Status</span>'
                '</div>')
    cc = {"PEAK":"ch-peak","HIGH":"ch-high","MODERATE":"ch-mod","LOW":"ch-low","SOLAR SURPLUS":"ch-solar"}.get(f["status"],"ch-mod")
    tt = " 💸" if f["peak_tariff"] else ""
    st_tag = f' ☀️ &minus;{f["solar"]} kWh' if f["solar"] > 0 else ""
    return (f'<div class="fc-row">'
            f'<span class="fc-time">{f["label"]}</span>'
            f'<span class="fc-desc">Draw: <b style="color:#e0f7fa">{f["kwh"]} kWh</b>{st_tag}{tt}</span>'
            f'<span class="fc-net">{f["net"]} kWh</span>'
            f'<span class="fc-stat"><span class="chip {cc}">{f["status"]}</span></span></div>')

def sec(icon, title, badge=""):
    b = f'<span class="sec-badge">{badge}</span>' if badge else ""
    return (f'<div class="sec-hdr"><span class="sec-icon">{icon}</span>'
            f'<span class="sec-title">{title}</span>{b}</div>')


# ─── Layout ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-title">⚡ Eco-Watt AI</div>
  <div class="hero-sub">Smart Home Energy Forecasting &amp; Load Optimizer — Powered by Regional Grid Intelligence</div>
  <div class="pills">
    <span class="pill pill-gold">🌍 UN SDG 7 · Affordable &amp; Clean Energy</span>
    <span class="pill pill-green">🌿 UN SDG 13 · Climate Action</span>
    <span class="pill pill-blue">📡 TSSPDCL / TSNPDCL Grid Data Model</span>
  </div>
</div>
""", unsafe_allow_html=True)
# ── Input Card ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="card-eyebrow">🔍 Consumer Identity Lookup</div>', unsafe_allow_html=True)
st.markdown('<div class="card-label">Electricity Meter / Consumer Number</div>', unsafe_allow_html=True)

c1, c2 = st.columns([3, 1])
with c1:
    meter_input = st.text_input(
        label="meter", label_visibility="collapsed",
        placeholder="e.g. TSSPDCL-HYD-202411-00847",
        key="mid", max_chars=40,
    )
    st.markdown(
        '<div class="card-hint">Enter your Consumer ID as printed on your DISCOM electricity bill. '
        'Your identity is never stored — only anonymised usage patterns are analysed.</div>',
        unsafe_allow_html=True)
with c2:
    st.markdown("<br>", unsafe_allow_html=True)
    clicked = st.button("⚡ Analyze & Optimize Grid Load", key="go")

st.markdown('</div>', unsafe_allow_html=True)

# ── Report ────────────────────────────────────────────────────────────────────
if clicked:
    if not meter_input or len(meter_input.strip()) < 5:
        st.error("Please enter a valid Consumer / Meter Number (at least 5 characters) to proceed.")
    else:
        prog = st.progress(0)
        msgs = ["Querying DISCOM grid model...", "Merging weather telemetry...", "Running optimization engine..."]
        for i, p in enumerate([10,25,42,60,76,90,100]):
            time.sleep(0.11)
            prog.progress(p)
        d = simulate_utility_and_weather_pipeline(meter_input.strip())
        prog.empty()

        st.markdown(f"""
        <div class="success-banner">
          <span class="sb-icon">✅</span>
          <div>
            <div class="sb-title">Analysis Complete</div>
            <div class="sb-sub">Consumer ID: <span class="mono-tag">{d['meter']}</span>
              &nbsp;·&nbsp; {d['consumer_type']} &nbsp;·&nbsp; {d['locality']} &nbsp;·&nbsp; Generated: {d['ts']}
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        # 1. Snapshot
        st.markdown(sec("📊", "Live Grid &amp; Weather Snapshot", "REAL-TIME SIMULATION"), unsafe_allow_html=True)
        chips = (mchip(f"{d['temp']}°C","Ambient Temperature",f"Heat Index: {d['heat_idx']}°C") +
                 mchip(f"{d['irradiance']} W/m²","Solar Irradiance","Good generation window today") +
                 mchip(f"{d['peak_kw']} kW","Peak Load Demand",f"Off-peak: {d['offpeak_kw']} kW") +
                 mchip(f"{d['monthly_kwh']} kWh","Monthly Consumption",f"Tariff: Rs.{d['tariff']}/unit") +
                 mchip(f"{int(d['stress']*100)}%","Grid Stress Index",f"Level: {d['slevel']}") +
                 mchip(f"{d['voltage']} V","Voltage Stability",f"Power Factor: {d['pf']}") +
                 mchip(f"{d['humidity']}%","Relative Humidity",f"Wind: {d['wind']} km/h") +
                 mchip(f"UV {d['uv']}","UV Index Today",f"Cloud Cover: {d['cloud']}%"))
        st.markdown(f'<div class="mgrid">{chips}</div>', unsafe_allow_html=True)

        # 2. Alert
        st.markdown(sec("⚠️","Eco-Watt Grid Alert"), unsafe_allow_html=True)
        em = {"CRITICAL":"🔴","HIGH":"🟠","MODERATE":"🟡"}[d['slevel']]
        ac = {"red":"alert-red","amber":"alert-amber","blue":"alert-blue"}[d['scolor']]
        dr_col = "#69f0ae" if d['dr_ok'] else "#ff8a80"
        dr_txt = "Yes — Enroll Now" if d['dr_ok'] else "Not Enrolled"
        st.markdown(f"""
        <div class="alert {ac}">
          <div class="alert-title">{em} Neighbourhood Grid Stress: {d['slevel']}
            &nbsp;·&nbsp; {d['discom']} &nbsp;·&nbsp; {d['locality']}</div>
          <div class="alert-body">{d['smsg']}</div>
          <div class="alert-meta">
            <span>Tariff Code: <b>{d['tariff_code']}</b></span>
            <span>DR Eligible: <b style="color:{dr_col}">{dr_txt}</b></span>
            <span>Peak Tariff Multiplier: <b style="color:#ffd54f">x{d['peak_mult']}</b></span>
          </div>
        </div>""", unsafe_allow_html=True)

        # 3. Appliances
        st.markdown(sec("🏠","Appliance Load Breakdown","SIMULATED INVENTORY"), unsafe_allow_html=True)
        st.markdown('<p style="font-size:0.78rem;color:rgba(190,215,255,0.55);margin:0 0 10px">Sorted by daily consumption. Bar width = share of total household load.</p>', unsafe_allow_html=True)
        mx = max(a["dkwh"] for a in d["appliances"])
        st.markdown("".join(app_row(a, mx) for a in d["appliances"]), unsafe_allow_html=True)

        # 4. Forecast
        st.markdown(sec("🕐","24-Hour Demand Forecast","AI FORECAST MODEL"), unsafe_allow_html=True)
        rows = fc_row(None, head=True) + "".join(fc_row(f) for f in d["forecast"])
        st.markdown(f'<div class="fc-wrap">{rows}</div>', unsafe_allow_html=True)
        st.markdown('<div class="fc-legend">💸 Peak tariff window &nbsp;|&nbsp; ☀️ Solar generation offset &nbsp;|&nbsp; Net kWh = grid draw after solar</div>', unsafe_allow_html=True)

        # 5. Steps
        st.markdown(sec("💡","Actionable Optimization Steps","AI-GENERATED PLAN"), unsafe_allow_html=True)
        for i, s in enumerate(d["steps"], 1):
            st.markdown(f"""
            <div class="opt-step">
              <div class="opt-num">{i}</div>
              <div><div class="opt-title">{s['title']}</div>
              <div class="opt-body">{s['body']}</div>
              <div class="opt-save">💰 {s['save']}</div></div>
            </div>""", unsafe_allow_html=True)

        # 6. ROI
        st.markdown(sec("🌿","Environmental &amp; Economic ROI","IMPACT DASHBOARD"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="alert alert-green">
          <div class="alert-title">🎯 Your Full Optimization Potential at a Glance</div>
          <div class="alert-body">Based on <b>{d['monthly_kwh']} kWh/month</b> at Rs.{d['tariff']}/unit
          ({d['discom']} · {d['tariff_code']}), all five steps deliver:</div>
          <div class="roi-grid">
            <div class="roi-cell"><div class="roi-label">Monthly Bill Reduction</div>
              <div class="roi-val">Rs.{int(d['save_rs']):,}</div>
              <div class="roi-note">{d['total_pct']}% of current monthly spend</div></div>
            <div class="roi-cell"><div class="roi-label">Annual Savings Potential</div>
              <div class="roi-val">Rs.{int(d['save_rs']*12):,}</div>
              <div class="roi-note">At current Rs.{d['tariff']}/unit tariff</div></div>
            <div class="roi-cell"><div class="roi-label">CO₂ Prevented / Month</div>
              <div class="roi-val">{d['co2_mo']} kg</div>
              <div class="roi-note">0.71 kg CO₂/kWh · CEA 2023 India grid emission factor</div></div>
            <div class="roi-cell"><div class="roi-label">Annual CO₂ Mitigation</div>
              <div class="roi-val">{d['co2_yr']} kg</div>
              <div class="roi-note">≈ {d['trees']} mature trees planted</div></div>
            <div class="roi-cell"><div class="roi-label">Load-Shift Savings</div>
              <div class="roi-val">{d['shift_pct']}%</div>
              <div class="roi-note">From peak-to-off-peak rescheduling alone</div></div>
            <div class="roi-cell"><div class="roi-label">Solar Integration Gain</div>
              <div class="roi-val">{d['solar_pct']}%</div>
              <div class="roi-note">Rooftop solar + net metering scenario</div></div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sdg-callout">
          <b style="color:#ffe57f">SDG 7 Alignment:</b> Shifting {d['monthly_kwh']} kWh/month toward off-peak
          solar windows cuts fossil-fuel dependency by <b style="color:#ffe57f">{d['shift_pct']}%</b>,
          supporting India's 500 GW renewable target under the National Solar Mission and PM Surya Ghar scheme.<br><br>
          <b style="color:#b9f6ca">SDG 13 Alignment:</b> Preventing <b style="color:#b9f6ca">{d['co2_yr']} kg CO₂/year</b>
          per household — scaled across {d['discom']}'s ~6 million consumers — offsets
          <b style="color:#b9f6ca">{round(d['co2_yr']*6_000_000/1_000_000,1)} million tonnes CO₂/year</b>,
          equivalent to retiring a 500 MW coal plant. Climate action starts at the meter.
        </div>""", unsafe_allow_html=True)

        # 7. Privacy
        st.markdown(sec("🔒","Responsible AI &amp; Consumer Privacy Statement"), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="priv-box">
          <div class="priv-title">🛡️ How Eco-Watt AI Protects Your Identity</div>
          <div class="priv-item"><span class="priv-key">1. Zero Personal Data Ingestion:</span>
            Only the numerical meter identifier is read. No name, address, Aadhaar, bank detail, or contact
            information is requested, transmitted, or stored. The Consumer ID is used solely as a deterministic
            simulation seed and discarded when your session ends.</div>
          <div class="priv-item"><span class="priv-key">2. On-Device Processing:</span>
            All analytics — appliance profiling, load forecasting, optimization scoring — run entirely inside
            the Streamlit session container. No data reaches any external database, analytics API, or cloud
            data lake. Session data is ephemeral and cleared when the browser tab is closed.</div>
          <div class="priv-item"><span class="priv-key">3. Anonymised Trend Aggregation:</span>
            Any future neighbourhood-level aggregation uses only statistically anonymised, k-anonymity-protected
            aggregate trend vectors — never individual consumer records — fully compliant with DPDPA 2023 and
            CERT-In guidelines.</div>
          <div class="priv-item"><span class="priv-key">4. AI Transparency:</span>
            All outputs are AI-generated simulations from publicly available TSSPDCL/TSNPDCL tariff schedules,
            IMD weather distributions, and CEA emission factors. They are advisory only — not official
            billing statements or binding energy audits.</div>
          <div class="priv-item"><span class="priv-key">5. No Discriminatory Profiling:</span>
            Eco-Watt AI performs no credit scoring, income inference, or discriminatory consumer profiling.
            The system equitably empowers all consumers across all tariff categories, consistent with
            the universal-access mandate of UN SDG 7.</div>
          <div class="priv-foot">
            Consumer ID: <span class="mono-tag">{d['meter']}</span>
            &nbsp;·&nbsp; {d['ts']} IST &nbsp;·&nbsp; Eco-Watt AI v1.0 &nbsp;·&nbsp; DPDPA 2023 · CERT-In Compliant
          </div>
        </div>""", unsafe_allow_html=True)

st.markdown("""
<div class="eco-footer">
  ⚡ Eco-Watt AI &nbsp;·&nbsp; UN SDG 7 (Affordable &amp; Clean Energy) &amp; SDG 13 (Climate Action)
  &nbsp;·&nbsp; Grid model: TSSPDCL / TSNPDCL Telangana &nbsp;·&nbsp;
  Emission factor: CEA 2023 (0.71 kg CO₂/kWh) &nbsp;·&nbsp; All simulation data is synthetic · Educational use only
</div>
""", unsafe_allow_html=True)
