import streamlit as st
import pandas as pd
import plotly.express as px

footer_html = """<div style='text-align: center;'>
  <p>ReVibe Energy AB 2025</p>
</div>"""

logo = "Materials/ReVibe.png"

# --- Configuration ---
EXCHANGE_RATE_EUR_TO_USD = 1.14  # You can update this

# System price in EUR
system_name = "PM Industrial Ethernet Kit (90014)"
system_price_eur = 8125

# --- Streamlit App ---
st.set_page_config(page_title="Anura Downtime Cost Calculator", layout="centered")
st.columns(3)[1].image(logo)
st.title("Anura Downtime Cost Calculator")

st.markdown("""
This calculator estimates the **Return on Investment (ROI)** of installing PM monitoring systems 
based on **downtime cost, frequency**, and **number of installations**.
""")

# --- Currency Selection ---
st.subheader("1. Select Currency")
currency = st.radio("Choose your currency:", ["EUR", "USD"])
exchange_rate = 1.0 if currency == "EUR" else EXCHANGE_RATE_EUR_TO_USD
currency_symbol = "€" if currency == "EUR" else "$"

# --- Downtime Input ---
st.subheader("2. Downtime Event Details")

downtime_cost_options = list(range(0, 110000, 10000))
downtime_cost_per_hour = st.selectbox(
    f"Downtime cost per hour ({currency}):", downtime_cost_options
)

downtime_duration_days_options = [i * 0.5 for i in range(0, 29)]  # 0 to 5 days in 0.5-day steps
downtime_duration_days = st.selectbox(
    "Downtime duration per event (in days):", downtime_duration_days_options
)
downtime_duration_hours = downtime_duration_days * 24  # Convert to hours for calculation


downtime_events_options = list(range(0, 101))
downtime_events_per_year = st.selectbox(
    "Number of downtime events per year:", downtime_events_options
)

# Total downtime per year in hours
total_downtime_hours = downtime_duration_hours * downtime_events_per_year
annual_savings_per_install = total_downtime_hours * downtime_cost_per_hour

st.markdown("---")

# --- Installation Quantity ---
st.subheader("3. Number of Installations")

installation_options = list(range(1, 51))  # 1 to 50 installations
installations = st.selectbox(
    f"Number of '{system_name}' installations:", installation_options
)

# --- ROI Calculations ---
total_price = system_price_eur * installations * exchange_rate
total_savings = annual_savings_per_install * installations
roi = ((total_savings - total_price) / total_price) * 100 if total_price > 0 else 0

# --- Payback Time Analysis ---
savings_per_stop = downtime_duration_hours * downtime_cost_per_hour * installations

if savings_per_stop > 0:
    cumulative_savings = 0
    stop_number = 0
    while cumulative_savings < total_price:
        stop_number += 1
        cumulative_savings += savings_per_stop

    payback_info = f"**Payback achieved after stop #{stop_number}** (total savings: {currency_symbol}{cumulative_savings:,.2f})"
else:
    payback_info = "⚠️ No downtime savings defined. Cannot calculate payback."


df = pd.DataFrame([{
    "System": system_name,
    "Installations": installations,
    f"Total Cost ({currency_symbol})": total_price,
    f"Total Savings ({currency_symbol})": total_savings,
    "ROI (%)": roi
}])


st.markdown(f"""
### ROI Summary

- **Total Cost:** <span style='font-size:22px; font-weight:bold;'>{currency_symbol}{total_price:,.2f}</span>  
- **Total Savings/year:** <span style='font-size:22px; font-weight:bold;'>{currency_symbol}{total_savings:,.2f}</span>  
- **ROI:** <span style='font-size:22px; font-weight:bold;'>{roi:.2f}%</span>
""", unsafe_allow_html=True)



st.markdown("### 4. Payback Time")
st.markdown(payback_info)

payback_data = []
cumulative = 0
payback_point = None

for i in range(1, 10):  # Show up to 30 stops
    cumulative += savings_per_stop
    payback_data.append({
        "Stop": i,
        "Cumulative Savings": cumulative
    })
    if payback_point is None and cumulative >= total_price:
        payback_point = i

payback_df = pd.DataFrame(payback_data)

fig = px.line(
    payback_df,
    x="Stop",
    y="Cumulative Savings",
    title=f"Cumulative Savings vs. Number of Downtime Events ({currency})",
    markers=True,
    labels={"Cumulative Savings": f"Cumulative Savings ({currency_symbol})"},
)

fig.add_hline(
    y=total_price,
    line_dash="dash",
    line_color="red",
    annotation_text="Total Cost",
    annotation_position="top left"
)

fig.update_layout(
    yaxis_tickprefix=currency_symbol,
    height=500,
    xaxis_title="Number of Downtime Events (Stops)",
    yaxis_title=f"Cumulative Savings ({currency_symbol})"
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

st.markdown(footer_html, unsafe_allow_html=True)
