import streamlit as st
import numpy as np
import pandas as pd

# 1. Header & Title
st.title("JusSanus: Socio-Legal Health Simulator")
st.write("Visualizing how legal statutes and labor rules directly impact population physiology.")

# 2. Controls (Sidebar)
st.sidebar.header("Legal Policy Parameters")
work_hours = st.sidebar.slider("Weekly Work Hours Cap", 30, 70, 50)
rest_period = st.sidebar.slider("Min. Rest Between Shifts (hrs)", 6, 14, 8)
env_compliance = st.sidebar.slider("Environmental Compliance (%)", 0, 100, 60)

st.sidebar.header("Sociological Filter")
income = st.sidebar.selectbox("Annual Household Income ($)", [28000, 60000, 150000])

# 3. Mathematical Calculations
W = max(0, (work_hours - 35) / 15)
S = np.log(income / 25000)
R = max(0, (11 - rest_period) / 11)
E = (1 - env_compliance / 100) * 1.2

# Biomarker Outputs
csi = min(100.0, 15 + 18.5 * (W**2) - 12.0 * S + 14.5 * E)
asfi = min(100.0, (10 + 38 * R + 22 * W) * (1 + 0.25 * E - 0.15 * S))

# 4. Display Results on Screen
st.subheader("Physiological Strain Indicators")
col1, col2 = st.columns(2)
col1.metric("Cortisol Stress Index (CSI)", f"{csi:.1f} / 100")
col2.metric("Autonomic Fatigue Index (ASFI)", f"{asfi:.1f} / 100")

# 5. Cardiovascular Risk Trajectory Chart
st.subheader("5-Year Cardiovascular Risk Trajectory (CVSI)")
years = list(range(1, 6))
cvsi_scores = [min(100.0, 10 + (35 * (csi / 100)**1.5 + 20 * E - 8.5 * S) * (1 + 0.12 * t)) for t in years]

df = pd.DataFrame({"Year": years, "Cardiovascular Strain": cvsi_scores})
st.line_chart(df.set_index("Year"))
