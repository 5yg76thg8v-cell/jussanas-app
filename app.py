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
    """Fetch Lottie animation JSON safely from the web."""
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        return None
    return None

def show_custom_loading_screen(message="Veritas is analyzing legal statutes..."):
    """
    Renders custom ibis Paint drawing as an overlay while calculating.
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
        <img src="https://raw.githubusercontent.com/YOUR-GITHUB-USERNAME/veritas-app/main/mascot.png" 
             width="180" 
             style="margin-bottom: 20px; border-radius: 12px;" 
             alt="Veritas Mascot"
             onerror="this.style.display='none'" />
        
        <h2 style="color: #ff6b81; margin: 5px 0;">✨ Veritas in Progress ✨</h2>
        <p style="color: #4b6584; font-size: 16px; font-weight: bold; text-align: center; max-width: 80%;">
            {message}
        </p>
        
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
    time.sleep(1.5)
    placeholder.empty()

# Load Lottie animations
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

# Income cohort definitions
income_dict = {
    15000: "$15,000 / yr (Deep Poverty)",
    28000: "$28,000 / yr (Low Wage / Vulnerable)",
    45000: "$45,000 / yr (Lower-Middle Cohort)",
    60000: "$60,000 / yr (Median Household)",
    100000: "$100,000 / yr (Upper-Middle Income)",
    150000: "$150,000 / yr (High Earner / Buffered)",
    250000: "$250,000 / yr (Top Bracket / Fully Buffered)"
}

selected_income = st.sidebar.selectbox(
    "Annual Household Income ($)",
    options=list(income_dict.keys()),
    format_func=lambda key: income_dict[key],
    index=1,
    help="Socio-economic baseline income representing cohorts across the financial spectrum."
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
    cohort_label = income_dict[selected_income]
    st.caption(f"Modeled for Income Cohort: **{cohort_label}**")

    # Simulation Button
    if st.button("🚀 Run Bio-Legal Simulation", type="primary", use_container_width=True):
        show_custom_loading_screen("Veritas is calculating cortisol levels and autonomic strain...")
        st.success("Analysis Complete!")

    # Standardized Parameters
    W_val = max(0.0, (float(work_hours) - 35.0) / 15.0)
    S_val = float(np.log(float(selected_income) / 25000.0))
    R_val = max(0.0, (11.0 - float(rest_period)) / 11.0)
    E_val = (1.0 - float(env_compliance) / 100.0) * 1.2

    # Physiological Indexes
    csi_calc = 15.0 + 18.5 * (W_val ** 2) - 12.0 * S_val + 14.5 * E_val
    csi = min(100.0, max(0.0, csi_calc))

    asfi_calc = (10.0 + 38.0 * R_val + 22.0 * W_val) * (1.0 + 0.25 * E_val - 0.15 * S_val)
    asfi = min(100.0, max(0.0, asfi_calc))

    # Biomarker Displays
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

    # Cardiovascular Trajectory Chart
    st.subheader("5-Year Cardiovascular Strain Trajectory (CVSI)")
    st.write("Projected cumulative cardiovascular risk score over a 5-year statutory period:")

    years_list = [1, 2, 3, 4, 5]
    cvsi_list = []
    
    for yr in years_list:
        raw_cvsi = 10.0 + (35.0 * ((csi / 100.0) ** 1.5) + 20.0 * E_val - 8.5 * S_val) * (1.0 + 0.12 * float(yr))
        cvsi_list.append(min(100.0, max(0.0, raw_cvsi)))

    chart_data = pd.DataFrame({
        "Year": years_list,
        "Cardiovascular Strain (CVSI)": cvsi_list
    })
    
    st.line_chart(chart_data.set_index("Year"))

    # Educational Disclaimer
    st.caption("Disclaimer: Veritas is an educational modeling simulator for socio-legal research and does not constitute medical or legal advice.")


# ------------------------------------------
# SCREEN 3: ABOUT VERITAS
# ------------------------------------------
with tab3:
    st.title("About Veritas 🧠")
    
    if character_brain:
        st_lottie(character_brain, height=160, key="about_char")

    st.markdown("""
    ### The Core Intersections of Veritas
    * **Statutory Law:** Statutory limits establish structural conditions under which human labor operates.
    * **Sociology:** Socio-economic status acts as a biological buffer or amplifier against environmental strain.
    * **Physiology:** Chronic biological overload manifests measurable strain across neuroendocrine, autonomic, and cardiovascular systems.
    
    ---
    *Veritas — Uncovering biological truth in socio-legal systems.*
    """)
