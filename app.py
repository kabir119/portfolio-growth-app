import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Portfolio Growth Tracker", layout="wide")
st.title("📈 Portfolio Growth Projection")

# --- Inputs --- #
with st.sidebar:
    st.header("Input Parameters")
    monthly_sip_start = st.number_input("Initial Monthly SIP (₹)", value=85000, step=1000)
    annual_increase = st.number_input("Annual SIP Increase (%)", value=15) / 100
    annual_return = st.number_input("Expected Annual Return (%)", value=15) / 100
    years = st.slider("Investment Duration (Years)", min_value=1, max_value=40, value=20)
    current_portfolio_value = st.number_input("Current Portfolio Value (₹)", value=5465000, step=50000)

# --- Calculations --- #
months = years * 12
monthly_rate = annual_return / 12

sip_value = []
lumpsum_value = []
portfolio_value = []
fv_current_progress = []
sip_monthly_values = []
current_value = current_portfolio_value

for month in range(months):
    year = month // 12
    monthly_sip = monthly_sip_start * ((1 + annual_increase) ** year)

    if month == 0:
        sip_monthly = monthly_sip
    else:
        sip_monthly = sip_monthly_values[-1] * (1 + monthly_rate) + monthly_sip
    sip_monthly_values.append(sip_monthly)

    current_value *= (1 + monthly_rate)
    fv_current_progress.append(current_value)

    total = sip_monthly + current_value
    sip_value.append(sip_monthly)
    lumpsum_value.append(current_value)
    portfolio_value.append(total)

# --- INR Formatter --- #
def format_inr(value):
    x = int(value)
    after_decimal = f"{value:.2f}".split(".")[1]
    s = ""
    if x >= 100000:
        s = f"{x//100000},{x%100000:05d}"
    else:
        s = str(x)
    if len(s) > 5:
        s = s[:-5] + "," + s[-5:-3] + "," + s[-3:]
    elif len(s) > 3:
        s = s[:-3] + "," + s[-3:]
    return f"₹ {s}.{after_decimal}"

final_sip = sip_value[-1]
final_lumpsum = lumpsum_value[-1]
final_total = portfolio_value[-1]

# --- Output in words --- #
st.subheader("📢 Summary")
st.markdown(f"**Future Value of SIPs (with {int(annual_increase*100)}% step-up):**")
st.success(f"👉 {format_inr(final_sip)}")

st.markdown(f"**💼 Future Value of Current Portfolio:**")
st.success(f"👉 {format_inr(final_lumpsum)}")

st.markdown(f"**📈 Total Portfolio Value after {years} Years:**")
st.success(f"👉 {format_inr(final_total)}")

# --- Charts --- #
time_years = np.arange(1, months + 1) / 12

fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(time_years, np.array(sip_value) / 1e7, label="SIP Value Over Time", color='blue')
ax.plot(time_years, np.array(lumpsum_value) / 1e7, label="Current Portfolio Growth", color='green')
ax.plot(time_years, np.array(portfolio_value) / 1e7, label="Total Portfolio Value", color='purple', linestyle='--')
ax.set_xlabel("Years")
ax.set_ylabel("Value (₹ Crores)")
ax.set_title("📊 Portfolio Growth Over Time")
ax.legend()
ax.grid(True)
st.pyplot(fig)

# --- Additional Pie Chart --- #
fig2, ax2 = plt.subplots()
ax2.pie([final_sip, final_lumpsum], labels=["SIP Contributions", "Current Portfolio"], autopct='%1.1f%%', startangle=140)
ax2.set_title("🔍 Contribution Breakdown After {} Years".format(years))
st.pyplot(fig2)
