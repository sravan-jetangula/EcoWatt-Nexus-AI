import hashlib
import random
import streamlit as st

st.set_page_config(page_title="Eco-Watt AI", page_icon="🌱", layout="wide")

def simulate_utility_and_weather_pipeline(meter_num: str):
    seed = int(hashlib.sha256(meter_num.encode()).hexdigest(), 16) % (10**8)
    rng = random.Random(seed)

    temperature = round(rng.uniform(32, 42), 1)
    daily_kwh = round(rng.uniform(12, 48), 2)
    peak_load = round(rng.uniform(2.5, 8.5), 2)

    appliances = [
        "Air Conditioner",
        "Agricultural Pump",
        "Water Heater",
        "Refrigerator",
        "Washing Machine"
    ]
    heavy_appliance = rng.choice(appliances)

    bill_reduction = round(rng.uniform(8, 25), 1)
    carbon_saved = round(daily_kwh * rng.uniform(0.15, 0.35), 2)

    return {
        "temperature": temperature,
        "daily_kwh": daily_kwh,
        "peak_load": peak_load,
        "heavy_appliance": heavy_appliance,
        "bill_reduction": bill_reduction,
        "carbon_saved": carbon_saved
    }

st.title("🌱 Eco-Watt AI: Smart Home Energy Forecasting & Load Optimizer")
st.subheader("Supporting UN SDG 7 (Affordable & Clean Energy) and SDG 13 (Climate Action)")

meter = st.text_input("Electricity Meter / Consumer Number")

if st.button("Analyze & Optimize Grid Load"):
    if not meter:
        st.error("Please enter a valid Electricity Meter / Consumer Number.")
    else:
        data = simulate_utility_and_weather_pipeline(meter)

        st.success("Analysis Complete")

        st.markdown("## ⚠️ Eco-Watt Grid Alert")
        st.warning(
            f"High ambient temperature of {data['temperature']}°C indicates elevated neighborhood demand. "
            f"Peak load estimated at {data['peak_load']} kW."
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Daily Consumption (kWh)", data["daily_kwh"])
        c2.metric("Peak Load (kW)", data["peak_load"])
        c3.metric("Temperature (°C)", data["temperature"])

        st.markdown("## 💡 Actionable Optimization Steps")
        st.write(
            f"- Shift heavy usage from **{data['heavy_appliance']}** to midday solar-rich hours.\n"
            "- Run washing machines between 1 PM and 3 PM.\n"
            "- Maintain AC at 24–26°C.\n"
            "- Avoid simultaneous operation of high-load appliances."
        )

        st.markdown("## 🌱 Environmental & Economic ROI")
        st.write(
            f"- Estimated bill reduction: **{data['bill_reduction']}%**\n"
            f"- Estimated CO₂ mitigation: **{data['carbon_saved']} kg**\n"
            "- Supports grid stability and renewable energy utilization."
        )

        st.markdown("## 🔒 Responsible AI Disclaimer")
        st.info(
            "This demonstration uses simulated utility and weather data. "
            "Personal identities are not processed. Only anonymized numerical usage patterns are analyzed."
        )
