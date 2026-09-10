import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie

# Page Setup
st.set_page_config(page_title="JusSanus App", page_icon="🧸", layout="centered")

# Helper function to load cute Lottie animations from the web
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Cute animated characters from LottieFiles
character_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json") # Friendly waving robot/character
character_brain = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json") # Cute science animation

# Create Multi-Screen Navigation using Tabs
tab1, tab2, tab3 = st.tabs(["🏠 Welcome", "📊 Policy Simulator", "📖 Learn More"])

# ==========================================
# SCREEN 1: WELCOME SCREEN
# ==========================================
with tab1:
    st.title("Welcome to JusSanus! 🧸")
    st.write("Meet **Sanus**, your cute guide to understanding how laws affect human biological health!")
    
    if character_hello:
        st_lottie(character_hello, height=220, key="welcome_char")
    else:
        st.write("👋 *(Sanus waving)*")
        
    st.info("👈 Tap the **Policy Simulator** tab above to start testing legal rules!")

# ==========================================
# SCREEN 2: POLICY SIMULATOR (WITH LOADING)
# ==========================================
with tab2:
    st.title("Policy & Biomarker Simulator 🧪")
    
    # Sidebar Controls
    st.sidebar.header("Legal Policy Parameters")
    work_hours = st.sidebar.slider("Weekly Work Hours Cap", 30, 70, 50)
    rest_period = st.sidebar.slider("Min. Rest Between Shifts (hrs)", 6, 14, 8)
    env_compliance = st.sidebar.slider("Environmental Compliance (%)", 0, 100, 60)

    st.sidebar.header("Sociological Filter")
    income = st.sidebar.selectbox("Annual Household Income ($)", [28000, 60000, 150000])

    # Simulation Button with Cute Loading Screen
    if st.button("🚀 Run Bio-Legal Simulation", type="primary"):
        with st.spinner("🤖 Sanus is analyzing legal statutes and calculating cortisol levels..."):
            time.sleep(1.2) # Simulates a fake 1.2-second loading delay
        st.success("Simulation Complete!")

    # Mathematical Calculations
    W = max(0, (work_hours - 35) / 15)
    S = np.log(income / 25000)
    R = max(0, (11 - rest_period) / 11)
    E = (1 - env_compliance / 100) * 1.2

    # Biomarker Outputs
    csi = min(100.0, 15 + 18.5 * (W**2) - 12.0 * S + 14.5 * E)
    asfi = min(100.0, (10 + 38 * R + 22 * W) * (1 + 0.25 * E - 0.15 * S))

    # Output Cards
    st.subheader("Physiological Strain Indicators")
    col1, col2 = st.columns(2)
    col1.metric("Cortisol Stress Index (CSI)", f"{csi:.1f} / 100")
    col2.metric("Autonomic Fatigue Index (ASFI)", f"{asfi:.1f} / 100")

    # Chart
    st.subheader("5-Year Cardiovascular Risk Trajectory (CVSI)")
    years = list(range(1, 6))
    cvsi_scores = [min(100.0, 10 + (35 * (csi / 100)**1.5 + 20 * E - 8.5 * S) * (1 + 0.12 * t)) for t in years]
    df = pd.DataFrame({"Year": years, "Cardiovascular Strain": cvsi_scores})
    st.line_chart(df.set_index("Year"))

# ==========================================
# SCREEN 3: ABOUT / LEARN MORE
# ==========================================
with tab3:
    st.title("About JusSanus 🧠")
    
    if character_brain:
        st_lottie(character_brain, height=180, key="brain_char")
        
    st.markdown("""
    ### Why bridge Sociology, Physiology, and Law?
    * **Law:** Sets legal caps on work hours, minimum rest breaks, and pollution limits.
    * **Sociology:** Determines how poverty or wealth buffers against environmental stress.
    * **Physiology:** Measures the biological price paid by the human body over time.
    """)
