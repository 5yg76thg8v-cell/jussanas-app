import streamlit as st
import numpy as np
import pandas as pd
import time
import requests
from streamlit_lottie import st_lottie

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Veritas: Bio-Legal Simulator",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. HELPER FUNCTIONS & CUSTOM LOADING SCREEN
# ==========================================
def load_lottieurl(url: str):
    """Fetch Lottie animation JSON from the web."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None

def show_custom_loading_screen(message="Veritas is analyzing legal statutes and calculating biological impact..."):
    """
    Renders your custom ibis Paint drawing as an overlay while calculating formulas.
    Replace the img src URL with your actual GitHub raw link once uploaded!
    """
    loading_html = f"""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-color: rgba(255, 245, 248, 0.96);
        z-index: 999999;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-family: sans-serif;
    ">
        <!-- REPLACE LINK BELOW WITH YOUR GITHUB RAW IMAGE LINK -->
        <img src="https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/veritas-app/main/mascot.png" 
             width="180" 
             style="margin-bottom: 20px; border-radius: 12px;" 
             alt="Veritas Mascot"
             onerror="this.style.display='none'" />
        
        <h2 style="color: #ff6b81; margin: 5px 0;">✨ Veritas in Progress ✨</h2>
        <p style="color: #4b6584; font-size: 16px; font-weight: bold; text-align: center; max-width: 80%;">
            {message}
        </p>
        
        <!-- Animated Progress Bar -->
        <div style="
            width: 220px;
            height: 10px;
            background-color: #ffe0e6;
            border-radius: 10px;
            overflow: hidden;
            margin-top: 15px;
        ">
            <div style="
                width: 100%;
                height: 100%;
                background-color: #ff6b81;
                animation: loading 2s infinite ease-in-out;
            "></div>
        </div>
    </div>
    """
    
    placeholder = st.empty()
    placeholder.markdown(loading_html, unsafe_allow_html=True)
    time.sleep(2.0)  # Controls how long the loading screen stays visible
    placeholder.empty()

# Load cute Lottie animations for the app
character_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_V9t630.json")
character_brain = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_mDnmhAgZkb.json")


# ==========================================
# 3. SIDEBAR (POLICY & SOCIO-ECONOMIC INPUTS)
# ==========================================
st.sidebar.title("Veritas ⚖️")
st.sidebar.subheader("Legal Policy Controls")

work_hours = st.sidebar.slider(
    "Weekly Work Hours Cap", 
    min_value=30, max_value=70, value=50, step=1,
    help="Maximum legal limit of work hours permitted per week."
)

rest_period = st.sidebar.slider(
    "Min. Rest Between Shifts (hrs)", 
    min_value=6, max_value=14, value=8, step=1,
    help="Statutory minimum rest window required between consecutive shifts."
)

env_compliance = st.sidebar.slider(
    "Environmental Compliance (%)", 
    min_value=0, max_value=100, value=60, step=5,
    help="Regulatory compliance level for air, noise, and environmental standards."
)

st.sidebar.divider()
st.sidebar.subheader("Sociological Filter")

income = st.sidebar.selectbox(
    "Annual Household Income ($)",
    options=[28000, 60000, 150000],
    format_func=lambda x: f"${x:,} / year",
    help="Socio-economic baseline income representing vulnerable, middle, and high-earning cohorts."
)


# ==========================================
# 4. MULTI-SCREEN TAB NAVIGATION
# ==========================================
tab1, tab2, tab3 = st.tabs(["🏠 Welcome", "📊 Bio-Legal Simulator", "📖 About Veritas"])


# ------------------------------------------
# SCREEN 1: WELCOME SCREEN
# ------------------------------------------
with tab1:
    st.title("Welcome to Veritas ⚖️")
    st.write("Uncovering the physiological price paid by human populations under legal statutes.")
    
    if character_hello:
        st_lottie(character_hello, height=200, key="welcome_char")
    
    st.info("👈 Adjust the policy controls in the **Sidebar**, then open the **Bio-Legal Simulator** tab above to run the math!")
    
    st.markdown("""
    ### How Veritas Works:
    1. **Set Legal Parameters:** Modify statutory caps on working hours, rest breaks, and pollution limits.
    2. **Filter by Income:** Select a socio-economic population to see how financial buffering alters physical strain.
    3. **Analyze Biomarkers:** Observe real-time changes in **Cortisol (CSI)**, **Autonomic Fatigue (ASFI)**, and **5-Year Cardiovascular Risk (CVSI)**.
    """)


# ------------------------------------------
# SCREEN 2: BIO-LEGAL SIMULATOR
# ------------------------------------------
with tab2:
    st.title("Physiological Impact Simulator 🧪")
    st.caption("Modeled for Annual Household Income: **$" + f"{income:,}**")

    # Simulation Button with Custom ibis Paint Loading Screen
    if st.button("🚀 Run Bio-Legal Simulation", type="primary", use_container_width=True):
        show_custom_loading_screen("Veritas is calculating cortisol levels and autonomic strain...")
        st.success("Analysis Complete!")

    # --- MATHEMATICAL MODEL CALCULATIONS ---
    # Standardized parameters
    W = max(0, (work_hours - 35) / 15)
    S = np.log(income / 25000)
    R = max(0, (11 - rest_period) / 11)
    E = (1 - env_compliance / 100) * 1.2

    # Physiological Indexes
    csi = min(100.0, 15 + 18.5 * (W**2) - 12.0 * S + 14.5 * E)
    asfi = min(100.0, (10 + 38 * R + 22 * W) * (1 + 0.25 * E - 0.15 * S))

    # --- BIOMARKER METRICS DISPLAY ---
    st.subheader("Current Biomarker Strain Indicators")
    col1, col2 = st.columns(2)
    
    col1.metric(
        label="Cortisol Stress Index (CSI)", 
        value=f"{csi:.1f} / 100",
        help="Higher values indicate chronic elevation of serum cortisol."
    )
    col2.metric(
        label="Autonomic Fatigue Index (ASFI)", 
        value=f"{asfi:.1f} / 100",
        help="Measures parasympathetic suppression and sleep fragmentation."
    )

    st.divider()

    # --- CARDIOVASCULAR RISK TRAJECTORY CHART ---
    st.subheader("5-Year Cardiovascular Strain Trajectory (CVSI)")
    st.write("Projected cumulative cardiovascular risk score over a 5-year statutory period:")

    years = list(range(1, 6))
    cvsi_scores = [
        min(100.0, 10 + (35 * (csi / 100)**1.5 + 20 * E - 8.5 * S) * (1 + 0.12 * t)) 
        for t in years
    ]

    df_chart = pd.DataFrame({
        "Year": years,
        "Cardiovascular Strain (CVSI)": cvsi_scores
    })
    
    st.line_chart(df_chart.set_index("Year"))

    # Educational Disclaimer
    st.caption("Disclaimer: Veritas is an educational modeling
