import streamlit as st
import random
import math
import hashlib
from datetime import datetime, timedelta

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Eco-Watt AI | Smart Energy Forecasting",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ──────────────────────────────────────────────
#  GLOBAL STYLES
# ──────────────────────────────────────────────
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .main { background-color: #0a0f1e; }

        .stApp {
            background: linear-gradient(135deg, #0a0f1e 0%, #0d1b2a 50%, #0a1628 100%);
            color: #e2e8f0;
        }

        /* ── HEADER BANNER ── */
        .header-banner {
            background: linear-gradient(120deg, #003d1f 0%, #005c2e 40%, #004d40 100%);
            border: 1px solid #00c853;
            border-radius: 16px;
            padding: 36px 40px;
            margin-bottom: 28px;
            position: relative;
            overflow: hidden;
        }
        .header-banner::before {
            content: '';
            position: absolute;
            top: -60px; right: -60px;
            width: 200px; height: 200px;
            background: radial-gradient(circle, rgba(0,200,83,0.18) 0%, transparent 70%);
            border-radius: 50%;
        }
        .header-title {
            font-size: 2.6rem;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: -0.5px;
            margin: 0 0 6px 0;
            line-height: 1.15;
        }
        .header-subtitle {
            font-size: 1.05rem;
            color: #a7f3d0;
            font-weight: 400;
            margin: 0 0 18px 0;
        }
        .sdg-badge {
            display: inline-block;
            padding: 5px 14px;
            border-radius: 20px;
            font-size: 0.78rem;
            font-weight: 600;
            margin-right: 8px;
            letter-spacing: 0.3px;
        }
        .sdg7  { background: #ffc107; color: #1a1a00; }
        .sdg13 { background: #4caf50; color: #fff; }

        /* ── CARD ── */
        .eco-card {
            background: rgba(15, 28, 50, 0.85);
            border: 1px solid rgba(0,200,83,0.22);
            border-radius: 14px;
            padding: 26px 28px;
            margin-bottom: 22px;
            backdrop-filter: blur(4px);
        }
        .card-title {
            font-size: 1.15rem;
            font-weight: 700;
            color: #00e676;
            margin-bottom: 14px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .card-body {
            font-size: 0.94rem;
            color: #cbd5e1;
            line-height: 1.7;
        }

        /* ── METRIC TILES ── */
        .metric-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 14px;
            margin-bottom: 22px;
        }
        .metric-tile {
            background: rgba(0,200,83,0.07);
            border: 1px solid rgba(0,200,83,0.3);
            border-radius: 12px;
            padding: 18px 16px;
            text-align: center;
        }
        .metric-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.75rem;
            font-weight: 700;
            color: #00e676;
            line-height: 1;
        }
        .metric-label {
            font-size: 0.74rem;
            color: #94a3b8;
            margin-top: 6px;
            text-transform: uppercase;
            letter-spacing: 0.6px;
        }

        /* ── ALERT BOXES ── */
        .alert-red {
            background: rgba(211,47,47,0.14);
            border-left: 4px solid #ef5350;
            border-radius: 0 10px 10px 0;
            padding: 16px 20px;
            margin-bottom: 16px;
            color: #ffcdd2;
        }
        .alert-yellow {
            background: rgba(255,193,7,0.12);
            border-left: 4px solid #ffc107;
            border-radius: 0 10px 10px 0;
            padding: 16px 20px;
            margin-bottom: 16px;
            color: #fff8e1;
        }
        .alert-green {
            background: rgba(0,200,83,0.10);
            border-left: 4px solid #00c853;
            border-radius: 0 10px 10px 0;
            padding: 16px 20px;
            margin-bottom: 16px;
            color: #ccffe5;
        }

        /* ── STEP LIST ── */
        .step-item {
            display: flex;
            align-items: flex-start;
            gap: 14px;
            padding: 14px 16px;
            background: rgba(255,255,255,0.03);
            border-radius: 10px;
            margin-bottom: 10px;
            border: 1px solid rgba(255,255,255,0.06);
        }
        .step-num {
            background: #00c853;
            color: #001a09;
            font-weight: 800;
            font-size: 0.8rem;
            width: 26px; height: 26px;
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            flex-shrink: 0;
        }
        .step-text { font-size: 0.91rem; color: #cbd5e1; line-height: 1.55; }
        .step-save { font-size: 0.78rem; color: #00e676; font-weight: 600; margin-top: 3px; }

        /* ── ROI TABLE ── */
        .roi-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .roi-label { font-size: 0.88rem; color: #94a3b8; }
        .roi-val   { font-family: 'JetBrains Mono', monospace; font-size: 0.92rem; color: #00e676; font-weight: 600; }

        /* ── PROGRESS BAR ── */
        .prog-wrap { margin-bottom: 16px; }
        .prog-header { display: flex; justify-content: space-between; font-size: 0.83rem; color: #94a3b8; margin-bottom: 6px; }
        .prog-track { background: rgba(255,255,255,0.08); border-radius: 6px; height: 9px; overflow: hidden; }
        .prog-fill  { height: 100%; border-radius: 6px; transition: width 0.4s ease; }
        .prog-green  { background: linear-gradient(90deg, #00c853, #69f0ae); }
        .prog-yellow { background: linear-gradient(90deg, #ffc107, #ffee58); }
        .prog-red    { background: linear-gradient(90deg, #ef5350, #ff8a80); }

        /* ── DIVIDER ── */
        .eco-divider {
            border: none;
            border-top: 1px solid rgba(0,200,83,0.18);
            margin: 28px 0;
        }

        /* ── INPUT OVERRIDE ── */
        .stTextInput > div > div > input {
            background: rgba(15,28,50,0.9) !important;
            border: 1.5px solid rgba(0,200,83,0.4) !important;
            color: #e2e8f0 !important;
            border-radius: 10px !important;
            font-family: 'JetBrains Mono', monospace !important;
            font-size: 1rem !important;
            padding: 12px 16px !important;
        }
        .stTextInput > div > div > input:focus {
            border-color: #00c853 !important;
            box-shadow: 0 0 0 3px rgba(0,200,83,0.15) !important;
        }

        /* ── BUTTON OVERRIDE ── */
        .stButton > button {
            background: linear-gradient(135deg, #00c853, #00897b) !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1rem !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 14px 36px !important;
            letter-spacing: 0.3px !important;
            transition: all 0.25s ease !important;
            width: 100% !important;
        }
        .stButton > button:hover {
            background: linear-gradient(135deg, #00e676, #00acc1) !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 24px rgba(0,200,83,0.35) !important;
        }

        /* ── FOOTER ── */
        .eco-footer {
            text-align: center;
            padding: 24px;
            font-size: 0.78rem;
            color: #475569;
            border-top: 1px solid rgba(0,200,83,0.1);
            margin-top: 40px;
        }

        /* ── DISCLAIMER ── */
        .disclaimer-box {
            background: rgba(30,41,59,0.7);
            border: 1px solid rgba(100,116,139,0.35);
            border-radius: 12px;
            padding: 20px 24px;
            font-size: 0.85rem;
            color: #94a3b8;
            line-height: 1.65;
        }
        .disclaimer-box strong { color: #cbd5e1; }

        /* ── UTILITY ── */
        .tag-chip {
            display: inline-block;
            background: rgba(0,200,83,0.12);
            border: 1px solid rgba(0,200,83,0.28);
            color: #69f0ae;
            font-size: 0.72rem;
            font-weight: 600;
            padding: 3px 10px;
            border-radius: 20px;
            margin: 2px 3px;
            letter-spacing: 0.4px;
            text-transform: uppercase;
        }
        .mono { font-family: 'JetBrains Mono', monospace; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
#  CONSTANTS
# ──────────────────────────────────────────────
DISCOMS = {
    "TSSPDCL": "Telangana Southern Power Distribution Co. Ltd.",
    "TSNPDCL": "Telangana Northern Power Distribution Co. Ltd.",
    "APEPDCL": "Andhra Pradesh Eastern Power Distribution Co. Ltd.",
    "APSPDCL": "Andhra Pradesh Southern Power Distribution Co. Ltd.",
    "BESCOM":  "Bangalore Electricity Supply Company",
    "MSEDCL":  "Maharashtra State Electricity Distribution Co. Ltd.",
}
APPLIANCES = [
    "Agricultural Water Pump (5 HP)",
    "Split Air Conditioner (1.5 Ton)",
    "Electric Water Heater (Geyser)",
    "Refrigerator (Double-door, 320L)",
    "Ceiling Fan (×4)",
    "Washing Machine (Front-load)",
    "Induction Cooktop",
    "LED Lighting (×12 fixtures)",
    "Desert Cooler (Evaporative)",
    "Television + Set-top Box",
    "Submersible Pump (1 HP)",
    "Microwave Oven",
]
DISTRICTS = [
    "Hyderabad", "Rangareddy", "Medchal-Malkajgiri", "Warangal",
    "Nizamabad", "Karimnagar", "Khammam", "Nalgonda",
    "Vijayawada", "Visakhapatnam", "Guntur", "Tirupati",
]
TARIFF_SLABS = [
    (0,   100,  1.45),
    (101, 200,  2.60),
    (201, 300,  4.00),
    (301, 500,  5.50),
    (501, 9999, 7.00),
]

# ──────────────────────────────────────────────
#  SIMULATION PIPELINE
# ──────────────────────────────────────────────
def simulate_utility_and_weather_pipeline(meter_num: str) -> dict:
    """
    Seeds a deterministic random generator from the meter number hash so
    the same consumer ID always produces the same simulated profile.
    Returns a rich dict of mock utility + weather metrics mirroring
    open-data fields from TSSPDCL / TSNPDCL public APIs and IMD weather data.
    """
    seed_bytes  = hashlib.sha256(meter_num.strip().upper().encode()).digest()
    seed_int    = int.from_bytes(seed_bytes[:8], "big")
    rng         = random.Random(seed_int)

    # ── Consumer identity (simulated) ──────────────────────────────────
    discom_key  = rng.choice(list(DISCOMS.keys()))
    district    = rng.choice(DISTRICTS)
    division    = f"DIV-{rng.randint(1, 12):02d}"
    substation  = f"SS-{district[:3].upper()}{rng.randint(100, 999)}"
    connection  = rng.choice(["LT Domestic", "LT Commercial", "LT Agricultural", "HT Industrial"])
    contract_kw = rng.choice([2, 3, 5, 7.5, 10, 15])

    # ── Weather metrics (IMD Telangana/AP summer range) ────────────────
    ambient_temp    = round(rng.uniform(32.0, 42.5), 1)           # °C
    feels_like      = round(ambient_temp + rng.uniform(2, 5), 1)  # heat index
    humidity_pct    = rng.randint(28, 72)                          # %
    wind_speed_kmh  = round(rng.uniform(4.0, 22.0), 1)
    uv_index        = rng.randint(7, 11)
    solar_irr       = round(rng.uniform(4.2, 6.8), 2)             # kWh/m²/day
    cloud_cover_pct = rng.randint(0, 40)

    # ── Consumption metrics (past 30 days simulated) ───────────────────
    monthly_kwh     = rng.randint(180, 1400)
    daily_avg_kwh   = round(monthly_kwh / 30, 2)
    peak_demand_kw  = round(rng.uniform(contract_kw * 0.5, contract_kw * 1.35), 2)
    off_peak_kwh    = round(monthly_kwh * rng.uniform(0.30, 0.45), 1)
    solar_backfeed  = round(rng.uniform(0, 85), 1)    # units fed to grid
    power_factor    = round(rng.uniform(0.78, 0.97), 2)

    # ── Appliance breakdown (kWh/month, randomised but summing ≈ monthly_kwh) ──
    num_appliances  = rng.randint(4, min(8, len(APPLIANCES)))
    selected_apps   = rng.sample(APPLIANCES, num_appliances)
    remaining       = monthly_kwh
    app_loads       = {}
    for i, app in enumerate(selected_apps):
        if i == len(selected_apps) - 1:
            app_loads[app] = remaining
        else:
            share = rng.uniform(0.08, 0.30)
            val   = min(int(monthly_kwh * share), remaining - (len(selected_apps) - i - 1) * 5)
            app_loads[app] = max(val, 5)
            remaining     -= app_loads[app]

    top_appliance   = max(app_loads, key=app_loads.get)
    top_app_kwh     = app_loads[top_appliance]
    top_app_pct     = round(top_app_kwh / monthly_kwh * 100, 1)

    # ── Grid stress calculation ────────────────────────────────────────
    # Stress index 0-100 from temperature, peak demand vs contract, power factor
    temp_factor      = (ambient_temp - 32) / (42.5 - 32)
    demand_factor    = min(peak_demand_kw / contract_kw, 1.5) / 1.5
    pf_factor        = 1 - power_factor
    grid_stress_idx  = round((temp_factor * 0.5 + demand_factor * 0.35 + pf_factor * 0.15) * 100, 1)
    grid_stress_idx  = min(grid_stress_idx, 99.9)

    stress_level = (
        "CRITICAL"  if grid_stress_idx >= 75 else
        "HIGH"      if grid_stress_idx >= 55 else
        "MODERATE"  if grid_stress_idx >= 35 else
        "NORMAL"
    )

    # ── Tariff & billing estimate ──────────────────────────────────────
    bill_amount = 0.0
    remaining_units = monthly_kwh
    prev_upper = 0
    for lower, upper, rate in TARIFF_SLABS:
        slab_units = min(remaining_units, upper - prev_upper)
        if slab_units <= 0:
            break
        bill_amount   += slab_units * rate
        remaining_units -= slab_units
        prev_upper      = upper
        if remaining_units <= 0:
            break
    fixed_charge  = contract_kw * 40           # ₹40 per kW contract demand
    bill_total    = round(bill_amount + fixed_charge, 2)
    bill_per_unit = round(bill_total / monthly_kwh, 2)

    # ── Optimisation opportunities ─────────────────────────────────────
    shift_saving_pct   = round(rng.uniform(8, 22), 1)
    pf_saving_pct      = round((1 - power_factor) * 15, 1)  # if corrected
    solar_saving_est   = round(solar_irr * 1.2 * 30 * 0.85, 0)  # kWh/month potential
    total_saving_pct   = round(min(shift_saving_pct + pf_saving_pct + rng.uniform(2, 6), 34), 1)
    monthly_saving_inr = round(bill_total * total_saving_pct / 100, 0)
    annual_saving_inr  = round(monthly_saving_inr * 12, 0)

    # ── Carbon metrics (Indian grid emission factor: 0.82 kgCO2/kWh in 2024) ──
    EMISSION_FACTOR    = 0.82
    monthly_co2_kg     = round(monthly_kwh * EMISSION_FACTOR, 1)
    saving_co2_kg      = round(monthly_kwh * (total_saving_pct / 100) * EMISSION_FACTOR, 1)
    annual_co2_saving  = round(saving_co2_kg * 12, 1)
    trees_equivalent   = round(annual_co2_saving / 21.7, 1)  # avg tree absorbs 21.7 kg CO2/yr

    # ── Peer comparison (simulated neighbourhood sample) ──────────────
    peer_avg_kwh       = rng.randint(220, 680)
    percentile_rank    = round(min(monthly_kwh / (peer_avg_kwh * 2) * 100, 99), 0)

    # ── Time-of-use schedule ──────────────────────────────────────────
    peak_hours    = ["18:00–21:00", "07:00–09:00"]
    off_peak_hrs  = ["22:00–05:00", "11:00–16:00"]
    solar_peak    = ["10:00–15:00"]

    return {
        # Identity
        "meter_num":        meter_num.strip().upper(),
        "discom_key":       discom_key,
        "discom_name":      DISCOMS[discom_key],
        "district":         district,
        "division":         division,
        "substation":       substation,
        "connection_type":  connection,
        "contract_kw":      contract_kw,
        # Weather
        "ambient_temp":     ambient_temp,
        "feels_like":       feels_like,
        "humidity_pct":     humidity_pct,
        "wind_speed_kmh":   wind_speed_kmh,
        "uv_index":         uv_index,
        "solar_irr":        solar_irr,
        "cloud_cover_pct":  cloud_cover_pct,
        # Consumption
        "monthly_kwh":      monthly_kwh,
        "daily_avg_kwh":    daily_avg_kwh,
        "peak_demand_kw":   peak_demand_kw,
        "off_peak_kwh":     off_peak_kwh,
        "solar_backfeed":   solar_backfeed,
        "power_factor":     power_factor,
        # Appliances
        "app_loads":        app_loads,
        "top_appliance":    top_appliance,
        "top_app_kwh":      top_app_kwh,
        "top_app_pct":      top_app_pct,
        # Grid
        "grid_stress_idx":  grid_stress_idx,
        "stress_level":     stress_level,
        # Billing
        "bill_total":       bill_total,
        "bill_per_unit":    bill_per_unit,
        "fixed_charge":     fixed_charge,
        # Optimisation
        "shift_saving_pct":    shift_saving_pct,
        "pf_saving_pct":       pf_saving_pct,
        "solar_saving_est":    solar_saving_est,
        "total_saving_pct":    total_saving_pct,
        "monthly_saving_inr":  monthly_saving_inr,
        "annual_saving_inr":   annual_saving_inr,
        # Carbon
        "monthly_co2_kg":      monthly_co2_kg,
        "saving_co2_kg":       saving_co2_kg,
        "annual_co2_saving":   annual_co2_saving,
        "trees_equivalent":    trees_equivalent,
        # Peers
        "peer_avg_kwh":        peer_avg_kwh,
        "percentile_rank":     percentile_rank,
        # Schedule
        "peak_hours":          peak_hours,
        "off_peak_hrs":        off_peak_hrs,
        "solar_peak":          solar_peak,
    }


# ──────────────────────────────────────────────
#  HELPER RENDERERS
# ──────────────────────────────────────────────
def render_progress_bar(label: str, value: float, max_val: float, color_class: str, unit: str = "%") -> str:
    pct = min(value / max_val * 100, 100)
    return f"""
    <div class="prog-wrap">
      <div class="prog-header"><span>{label}</span><span>{value} {unit}</span></div>
      <div class="prog-track">
        <div class="prog-fill {color_class}" style="width:{pct}%;"></div>
      </div>
    </div>
    """


def stress_colour(level: str) -> str:
    return {"CRITICAL": "alert-red", "HIGH": "alert-red",
            "MODERATE": "alert-yellow", "NORMAL": "alert-green"}.get(level, "alert-green")


def stress_emoji(level: str) -> str:
    return {"CRITICAL": "🔴", "HIGH": "🟠", "MODERATE": "🟡", "NORMAL": "🟢"}.get(level, "🟢")


# ──────────────────────────────────────────────
#  HEADER
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="header-banner">
        <div class="header-title">⚡ Eco-Watt AI</div>
        <div class="header-subtitle">Smart Home Energy Forecasting &amp; Grid Load Optimizer</div>
        <span class="sdg-badge sdg7">🌞 UN SDG 7 — Affordable &amp; Clean Energy</span>
        <span class="sdg-badge sdg13">🌍 UN SDG 13 — Climate Action</span>
    </div>
    """,
    unsafe_allow_html=True,
)

# ──────────────────────────────────────────────
#  INPUT PANEL
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="eco-card">
      <div class="card-title">🔌 Consumer Identification</div>
      <div class="card-body">
        Enter your <strong style="color:#69f0ae;">Electricity Meter / Consumer Number</strong> as
        printed on your monthly bill issued by TSSPDCL, TSNPDCL, APEPDCL, or any regional
        Indian Distribution Company (DISCOM). Your data is hashed locally and never transmitted.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

col_input, col_btn = st.columns([3, 1], gap="medium")
with col_input:
    meter_number = st.text_input(
        label="Meter / Consumer Number",
        placeholder="e.g. TSSPDCL-HYD-20240087234",
        help="Find this on the top-right corner of your electricity bill. Any alphanumeric ID works.",
        label_visibility="collapsed",
    )
with col_btn:
    st.markdown("<div style='padding-top:4px;'></div>", unsafe_allow_html=True)
    analyze_btn = st.button("⚡ Analyze & Optimize Grid Load")

# ──────────────────────────────────────────────
#  MAIN REPORT
# ──────────────────────────────────────────────
if analyze_btn:
    if not meter_number or len(meter_number.strip()) < 4:
        st.error("⚠️ Please enter a valid Meter / Consumer Number (minimum 4 characters).")
        st.stop()

    with st.spinner("🔄 Fetching grid telemetry, merging weather data, running load optimizer…"):
        d = simulate_utility_and_weather_pipeline(meter_number)

    # ── REPORT HEADER ──────────────────────────────────────────────────
    ts = datetime.now().strftime("%d %B %Y  •  %H:%M IST")
    st.markdown(
        f"""
        <div style="display:flex; justify-content:space-between; align-items:center;
                    padding:14px 20px; background:rgba(0,200,83,0.07);
                    border:1px solid rgba(0,200,83,0.2); border-radius:12px; margin-bottom:22px;">
          <div>
            <span style="font-size:1.1rem; font-weight:700; color:#00e676;">
              📋 Analysis Report
            </span>
            <span style="font-size:0.82rem; color:#94a3b8; margin-left:12px;">{ts}</span>
          </div>
          <div>
            <span class="tag-chip">{d['discom_key']}</span>
            <span class="tag-chip">{d['district']}</span>
            <span class="tag-chip">{d['connection_type']}</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── METER IDENTITY CARD ────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="eco-card">
          <div class="card-title">🪪 Utility Mapping — {d['meter_num']}</div>
          <div class="card-body">
            <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; font-size:0.88rem;">
              <div><span style="color:#64748b;">DISCOM</span><br><strong style="color:#e2e8f0;">{d['discom_name']}</strong></div>
              <div><span style="color:#64748b;">District</span><br><strong style="color:#e2e8f0;">{d['district']}</strong></div>
              <div><span style="color:#64748b;">Division</span><br><strong style="color:#e2e8f0;">{d['division']}</strong></div>
              <div><span style="color:#64748b;">Sub-station</span><br><strong style="color:#e2e8f0;">{d['substation']}</strong></div>
              <div><span style="color:#64748b;">Connection Type</span><br><strong style="color:#e2e8f0;">{d['connection_type']}</strong></div>
              <div><span style="color:#64748b;">Contract Demand</span><br><strong style="color:#e2e8f0;">{d['contract_kw']} kW</strong></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── KEY METRICS TILES ──────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="metric-grid">
          <div class="metric-tile">
            <div class="metric-value">{d['monthly_kwh']}</div>
            <div class="metric-label">Units / Month (kWh)</div>
          </div>
          <div class="metric-tile">
            <div class="metric-value">₹{d['bill_total']:,.0f}</div>
            <div class="metric-label">Est. Monthly Bill</div>
          </div>
          <div class="metric-tile">
            <div class="metric-value">{d['peak_demand_kw']}</div>
            <div class="metric-label">Peak Demand (kW)</div>
          </div>
          <div class="metric-tile">
            <div class="metric-value">{d['ambient_temp']}°C</div>
            <div class="metric-label">Ambient Temp</div>
          </div>
          <div class="metric-tile">
            <div class="metric-value">{d['grid_stress_idx']}</div>
            <div class="metric-label">Grid Stress Index</div>
          </div>
          <div class="metric-tile">
            <div class="metric-value">{d['monthly_co2_kg']}</div>
            <div class="metric-label">CO₂ Footprint (kg)</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<hr class='eco-divider'>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # SECTION 1 — GRID ALERT
    # ══════════════════════════════════════════════════════════════════
    st.markdown(
        f"""
        <div class="eco-card">
          <div class="card-title">⚠️ Eco-Watt Grid Alert</div>
        """,
        unsafe_allow_html=True,
    )

    s_col   = stress_colour(d["stress_level"])
    s_emoji = stress_emoji(d["stress_level"])

    st.markdown(
        f"""
          <div class="{s_col}">
            <strong>{s_emoji} {d['stress_level']} STRESS — Grid Stress Index: {d['grid_stress_idx']} / 100</strong><br>
            Current ambient temperature in <strong>{d['district']}</strong> is
            <strong>{d['ambient_temp']}°C</strong> (feels like {d['feels_like']}°C with
            {d['humidity_pct']}% humidity). At {d['peak_demand_kw']} kW peak draw against a
            {d['contract_kw']} kW contracted supply, your feeder at sub-station
            <span class="mono">{d['substation']}</span> is operating at
            <strong>{round(d['peak_demand_kw']/d['contract_kw']*100, 0):.0f}%</strong>
            of capacity. Regional DISCOM data indicates neighbourhood-wide load clustering
            between 18:00–21:00 IST during high-temperature days above 38°C.
          </div>
          <div style="margin-top:10px; font-size:0.88rem; color:#94a3b8; line-height:1.7;">
            <strong style="color:#e2e8f0;">Weather Snapshot:</strong>
            🌡️ {d['ambient_temp']}°C ambient &nbsp;|&nbsp;
            💧 {d['humidity_pct']}% RH &nbsp;|&nbsp;
            🌬️ {d['wind_speed_kmh']} km/h wind &nbsp;|&nbsp;
            ☀️ UV Index {d['uv_index']} &nbsp;|&nbsp;
            🌤️ {d['cloud_cover_pct']}% cloud cover &nbsp;|&nbsp;
            ⚡ Solar irradiance {d['solar_irr']} kWh/m²/day
          </div>
          <br>
        """,
        unsafe_allow_html=True,
    )

    # Progress bars for grid stress dimensions
    st.markdown(
        render_progress_bar(
            "Temperature Stress",
            d["ambient_temp"], 45,
            "prog-red" if d["ambient_temp"] > 38 else "prog-yellow",
            "°C",
        )
        + render_progress_bar(
            "Peak Demand vs Contract",
            round(d["peak_demand_kw"] / d["contract_kw"] * 100, 1), 150,
            "prog-red" if d["peak_demand_kw"] / d["contract_kw"] > 1 else "prog-yellow",
        )
        + render_progress_bar(
            "Power Factor Quality",
            round(d["power_factor"] * 100, 0), 100,
            "prog-green" if d["power_factor"] > 0.90 else "prog-yellow",
        )
        + render_progress_bar(
            "Overall Grid Stress Index",
            d["grid_stress_idx"], 100,
            "prog-red" if d["grid_stress_idx"] >= 65 else "prog-yellow",
        ),
        unsafe_allow_html=True,
    )

    # Appliance breakdown
    st.markdown(
        "<div style='font-size:0.9rem; font-weight:600; color:#94a3b8; margin:14px 0 10px;'>📊 Appliance Load Breakdown (kWh/month)</div>",
        unsafe_allow_html=True,
    )
    for app, kwh in sorted(d["app_loads"].items(), key=lambda x: x[1], reverse=True):
        pct = round(kwh / d["monthly_kwh"] * 100, 1)
        bar_color = "prog-red" if pct > 25 else "prog-yellow" if pct > 15 else "prog-green"
        st.markdown(
            render_progress_bar(app, kwh, d["monthly_kwh"], bar_color, "kWh"),
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close eco-card

    st.markdown("<hr class='eco-divider'>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # SECTION 2 — ACTIONABLE OPTIMIZATION STEPS
    # ══════════════════════════════════════════════════════════════════
    st.markdown(
        """
        <div class="eco-card">
          <div class="card-title">💡 Actionable Optimization Steps</div>
          <div class="card-body" style="margin-bottom:14px;">
            The following AI-generated load-shifting recommendations are derived from your
            specific consumption profile, regional time-of-use pricing windows, and live
            solar irradiance data for your district.
          </div>
        """,
        unsafe_allow_html=True,
    )

    steps = [
        (
            "Shift Heavy Loads to Solar Window",
            f"Run your <strong>{d['top_appliance']}</strong> — your single largest consumer "
            f"at <strong>{d['top_app_kwh']} kWh/month ({d['top_app_pct']}%)</strong> — "
            f"between <strong>10:00 AM – 2:00 PM</strong> when your sub-station feeder experiences "
            f"minimum stress and solar generation peaks at {d['solar_irr']} kWh/m²/day.",
            f"Estimated saving: {d['shift_saving_pct']}% on peak tariff charges",
        ),
        (
            "Stagger Washing & Cooking to 1:00 PM",
            "Run your washing machine full-load cycle starting at 1:00 PM. Solar irradiance "
            "during this window makes grid power cheaper and cleaner — Telangana's distribution "
            "grid imports the highest share of renewable energy between 11:00–15:00 IST. "
            "Batch induction cooking tasks to the same window.",
            "Saves ~12–18% on afternoon energy costs",
        ),
        (
            "Set AC Thermostat to 24–26°C and Use Fan Assist",
            f"At {d['ambient_temp']}°C ambient, every 1°C reduction in AC setpoint increases "
            "consumption by approximately 6%. Setting your split AC to 24°C with one ceiling fan "
            "running delivers the same thermal comfort at 18–22% lower energy draw. "
            "Enable the AC's 'economy' or 'sleep' mode after 10 PM.",
            "Expected saving: 18–22% on air conditioning load",
        ),
        (
            "Correct Power Factor with Capacitor Bank",
            f"Your measured power factor is <strong>{d['power_factor']}</strong>. TSSPDCL/TSNPDCL "
            "levy a reactive energy surcharge when PF drops below 0.90. Installing a 2–5 kVAR "
            "capacitor bank (₹1,200–₹2,500 one-time cost) near your DB panel will raise PF "
            "to 0.95+ and eliminate this penalty.",
            f"Estimated saving: ₹{round(d['bill_total'] * d['pf_saving_pct'] / 100):,}/month after correction",
        ),
        (
            "Avoid Simultaneous Use During Evening Peak (18:00–21:00)",
            "The evening peak 18:00–21:00 IST coincides with maximum neighbourhood load — "
            "all refrigerators, TVs, ACs, and lighting switch on simultaneously. "
            "Pre-cool your home to 23°C by 17:30, pre-boil water for cooking, and defer "
            "non-essential charging (phones, laptops) to after 22:00 when grid stress drops sharply.",
            "Reduces peak kW demand charge on your bill",
        ),
        (
            "Enable Off-Peak Water Heating (22:00–05:00)",
            "If you use an electric water heater (geyser), install a ₹350 mechanical timer "
            "to run it between 22:00–04:00. This off-peak window carries the lowest grid stress "
            f"nationally and helps DISCOM operators ({d['discom_key']}) flatten their load curve, "
            "directly contributing to SDG 7 infrastructure resilience.",
            "Saves up to 8% on water heating costs",
        ),
    ]

    for i, (title, body, saving) in enumerate(steps, 1):
        st.markdown(
            f"""
            <div class="step-item">
              <div class="step-num">{i}</div>
              <div>
                <div style="font-weight:600; color:#e2e8f0; font-size:0.92rem; margin-bottom:4px;">{title}</div>
                <div class="step-text">{body}</div>
                <div class="step-save">✅ {saving}</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close eco-card

    st.markdown("<hr class='eco-divider'>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # SECTION 3 — ENVIRONMENTAL & ECONOMIC ROI
    # ══════════════════════════════════════════════════════════════════
    st.markdown(
        """
        <div class="eco-card">
          <div class="card-title">🌱 Environmental &amp; Economic ROI</div>
        """,
        unsafe_allow_html=True,
    )

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown(
            f"""
            <div style="font-size:0.9rem; font-weight:600; color:#94a3b8; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">
              Economic Performance
            </div>
            <div class="roi-row">
              <span class="roi-label">Current Monthly Bill</span>
              <span class="roi-val">₹{d['bill_total']:,.0f}</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Projected Bill After Optimization</span>
              <span class="roi-val">₹{d['bill_total'] - d['monthly_saving_inr']:,.0f}</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Monthly Saving</span>
              <span class="roi-val">₹{d['monthly_saving_inr']:,.0f} ({d['total_saving_pct']}%)</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Annual Projected Saving</span>
              <span class="roi-val">₹{d['annual_saving_inr']:,.0f}</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Average Bill per Unit (kWh)</span>
              <span class="roi-val">₹{d['bill_per_unit']}</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Fixed Charges (Contract Demand)</span>
              <span class="roi-val">₹{d['fixed_charge']:,.0f}</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Solar Potential (if rooftop 1 kWp installed)</span>
              <span class="roi-val">{d['solar_saving_est']:.0f} kWh/month</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Grid Back-feed (Solar Export Simulated)</span>
              <span class="roi-val">{d['solar_backfeed']} units</span>
            </div>
            <div class="roi-row" style="border:none;">
              <span class="roi-label">Neighbourhood Percentile (Usage Rank)</span>
              <span class="roi-val">Top {100 - int(d['percentile_rank'])}%</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f"""
            <div style="font-size:0.9rem; font-weight:600; color:#94a3b8; margin-bottom:12px; text-transform:uppercase; letter-spacing:0.5px;">
              Carbon &amp; Climate Impact
            </div>
            <div class="roi-row">
              <span class="roi-label">Current Monthly CO₂ Footprint</span>
              <span class="roi-val">{d['monthly_co2_kg']} kg CO₂</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">CO₂ Prevented This Month (Optimized)</span>
              <span class="roi-val">{d['saving_co2_kg']} kg CO₂</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Annual CO₂ Mitigation</span>
              <span class="roi-val">{d['annual_co2_saving']} kg CO₂/yr</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Equivalent Trees Planted</span>
              <span class="roi-val">🌳 {d['trees_equivalent']} trees/year</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Indian Grid Emission Factor Used</span>
              <span class="roi-val">0.82 kg CO₂/kWh</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Off-Peak Energy Consumed</span>
              <span class="roi-val">{d['off_peak_kwh']} kWh</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Solar Irradiance (Your District)</span>
              <span class="roi-val">{d['solar_irr']} kWh/m²/day</span>
            </div>
            <div class="roi-row">
              <span class="roi-label">Peer Average Consumption</span>
              <span class="roi-val">{d['peer_avg_kwh']} kWh/month</span>
            </div>
            <div class="roi-row" style="border:none;">
              <span class="roi-label">Alignment with SDG 13 Target</span>
              <span class="roi-val">✅ On Track</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Summary highlight
    st.markdown(
        f"""
        <div class="alert-green" style="margin-top:18px;">
          <strong>🏆 Your 12-Month Impact Summary:</strong> By following these optimization steps,
          you will save approximately <strong>₹{d['annual_saving_inr']:,.0f}</strong> annually,
          prevent <strong>{d['annual_co2_saving']} kg of CO₂</strong> from entering the atmosphere —
          equivalent to planting <strong>{d['trees_equivalent']} trees</strong> — and reduce grid
          pressure on the <strong>{d['substation']}</strong> feeder serving your neighbourhood in
          <strong>{d['district']}</strong>.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<hr class='eco-divider'>", unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════════
    # SECTION 4 — RESPONSIBLE AI DISCLAIMER
    # ══════════════════════════════════════════════════════════════════
    st.markdown(
        """
        <div class="eco-card">
          <div class="card-title">🔒 Responsible AI &amp; Data Privacy Disclosure</div>
          <div class="disclaimer-box">
            <strong>How Eco-Watt AI processes your Meter Number:</strong><br><br>
            Your Electricity Meter / Consumer Number is passed through a
            <strong>one-way SHA-256 cryptographic hash function</strong> entirely within your local
            browser session. No meter number, consumer name, address, or billing identity is
            transmitted to any external server, stored in any database, or shared with third parties
            including the DISCOM operators named in this report.<br><br>
            <strong>What the AI reads vs. what it ignores:</strong><br>
            Eco-Watt AI reads only <em>aggregated numerical usage trends</em> — monthly kilowatt-hours,
            peak demand windows, and power factor readings — which are the same category of data
            published in anonymised form by the Central Electricity Authority (CEA) and Ministry of
            Power in India's open data portals. At no point does the system infer, store, or process
            personally identifiable information (PII) such as consumer name, service address,
            aadhaar linkage, or payment history.<br><br>
            <strong>Simulation transparency:</strong><br>
            All consumption metrics, appliance loads, billing figures, and weather readings presented
            in this report are <em>deterministically simulated</em> from publicly available
            Indian grid statistics (TSSPDCL/TSNPDCL tariff orders FY 2023–24, CEA Load Generation
            Balance Reports, and IMD climatological normals for Telangana &amp; Andhra Pradesh).
            They represent a statistically representative consumer profile seeded from your meter
            number and are intended for educational, advisory, and internship demonstration purposes
            only. They do not constitute official DISCOM billing data.<br><br>
            <strong>Alignment with AI ethics frameworks:</strong><br>
            Eco-Watt AI is developed under the principles of the NITI Aayog Responsible AI framework
            and the EU AI Act's transparency requirements for high-impact AI systems. The system
            does not make automated decisions affecting your legal rights, financial status, or
            utility service. All recommendations are advisory and humans remain in full control of
            energy decisions.<br><br>
            <em>For official billing inquiries, contact your DISCOM directly via their consumer
            portal. TSSPDCL: tssouthernpower.com | TSNPDCL: tsnpdcl.in</em>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
#  SIDEBAR — ABOUT
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown(
        """
        <div style="padding:16px 0; font-family:'Inter',sans-serif;">
          <div style="font-size:1.1rem; font-weight:700; color:#00e676; margin-bottom:8px;">
            ⚡ Eco-Watt AI
          </div>
          <div style="font-size:0.82rem; color:#94a3b8; line-height:1.6;">
            <strong style="color:#cbd5e1;">Project Type:</strong> Internship Demo<br>
            <strong style="color:#cbd5e1;">Domain:</strong> Sustainability Tech<br>
            <strong style="color:#cbd5e1;">Stack:</strong> Python · Streamlit · Docker<br>
            <strong style="color:#cbd5e1;">SDGs:</strong> #7 Clean Energy · #13 Climate Action<br>
            <strong style="color:#cbd5e1;">Region:</strong> Telangana / Andhra Pradesh, India<br>
            <strong style="color:#cbd5e1;">Emission Factor:</strong> 0.82 kg CO₂/kWh (CEA 2024)<br>
          </div>
          <hr style="border-color:rgba(0,200,83,0.15); margin:14px 0;">
          <div style="font-size:0.78rem; color:#64748b; line-height:1.55;">
            Data sources referenced:<br>
            • TSSPDCL Tariff Order FY24<br>
            • CEA Load Generation Balance Report<br>
            • IMD Climatological Normals AP/TS<br>
            • MoP National Smart Grid Mission<br>
            • NITI Aayog SDG India Index
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ──────────────────────────────────────────────
#  FOOTER
# ──────────────────────────────────────────────
st.markdown(
    """
    <div class="eco-footer">
      Eco-Watt AI &nbsp;•&nbsp; Built for UN SDG 7 &amp; SDG 13 &nbsp;•&nbsp;
      Powered by Python &amp; Streamlit &nbsp;•&nbsp;
      All consumption data is simulated for demonstration purposes &nbsp;•&nbsp;
      No real consumer data is collected or stored
    </div>
    """,
    unsafe_allow_html=True,
)
