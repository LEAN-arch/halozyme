# pages/Continued_Process_Verification_CPV.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(
    page_title="CPV Dashboard | Halozyme",
    layout="wide"
)

st.title("📈 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of the commercial downstream manufacturing process for rHuPH20 at **CDMO Alpha**.")

with st.expander("🌐 The Role of CPV & Regulatory Context", expanded=True):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that the process remains in a state of control during routine commercial manufacturing. As the MSAT lead, this is a cornerstone of my lifecycle management responsibilities.

    - **FDA Process Validation Guidance (Stage 3):** This guidance explicitly calls for an ongoing program to collect and analyze product and process data that relate to product quality. This dashboard is our primary tool for fulfilling this requirement.
    - **ICH Q8 (Pharmaceutical Development):** CPV is a key component of lifecycle management, ensuring that the process remains within the established **Design Space**.
    - **Purpose:** This dashboard is used to:
        1.  Monitor all defined Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) using statistical control charts.
        2.  Detect and investigate any unexpected process variability or trends across the control strategy.
        3.  Periodically assess Process Capability (Ppk) for all CQAs to ensure we consistently meet quality specifications.
        4.  Provide the data package for Annual Product Quality Reviews (APQRs) and regulatory inspections.
    """)

# --- Data Generation ---
def generate_full_cpv_data():
    """Generates a comprehensive, realistic CPV dataset."""
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    
    # --- CMAs: Critical Material Attributes ---
    resin_age = np.linspace(1, 200, n_batches)
    buffer_lot_id = [f"BUF-0{i//10}" for i in range(n_batches)]
    
    # --- CPPs: Critical Process Parameters ---
    conductivity = np.random.normal(15.2, 0.2, n_batches)
    conductivity[40] = 17.5 # Special cause variation
    load_density = np.random.normal(25.5, 0.5, n_batches)
    elution_ph = np.random.normal(6.5, 0.05, n_batches)
    
    # --- CQAs: Critical Quality Attributes ---
    purity_base = 99.0
    purity_resin_effect = - (resin_age / 250)**2
    purity_cond_effect = - abs(conductivity - 15.2) * 0.5
    purity_noise = np.random.normal(0, 0.1, n_batches)
    purity = purity_base + purity_resin_effect + purity_cond_effect + purity_noise
    
    yield_val = 90 - (resin_age / 100) + np.random.normal(0, 0.5, n_batches)
    
    return pd.DataFrame({
        'Batch ID': batches,
        'CQA - Purity (%)': purity,
        'CQA - Step Yield (%)': yield_val,
        'CPP - IEX Pool Conductivity (mS/cm)': conductivity,
        'CPP - IEX Load Density (g/L)': load_density,
        'CPP - Elution Buffer pH': elution_ph,
        'CMA - Resin Age (cycles)': resin_age,
        'CMA - Buffer Lot ID': buffer_lot_id
    })

cpv_df = generate_full_cpv_data()

# --- Control Strategy Definition ---
st.header("IEX Chromatography Control Strategy")
st.markdown("This dashboard tracks all defined parameters for the Ion Exchange unit operation. The goal is to correlate the performance of our inputs (CMAs, CPPs) with our outputs (CQAs).")
st.divider()

# --- 1. Critical Quality Attributes (CQAs) ---
st.subheader("I. Critical Quality Attribute (CQA) Monitoring")
st.markdown("CQAs are the direct measures of product quality that must meet specification.")

cqa_col1, cqa_col2 = st.columns(2)
with cqa_col1:
    parameter = 'CQA - Purity (%)'
    lsl, usl = 97.5, 100.0
    
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")
    
    fig = create_control_chart(cpv_df, parameter, '#005EB8')
    st.plotly_chart(fig, use_container_width=True)

with cqa_col2:
    parameter = 'CQA - Step Yield (%)'
    lsl, usl = 85.0, 100.0
    
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")

    fig = create_control_chart(cpv_df, parameter, '#00A9E0')
    st.plotly_chart(fig, use_container_width=True)
    
st.divider()

# --- 2. Critical Process Parameters (CPPs) ---
st.subheader("II. Critical Process Parameter (CPP) Monitoring")
st.markdown("CPPs are the operational parameters we control to ensure the CQA outcomes.")

cpp_col1, cpp_col2, cpp_col3 = st.columns(3)
cpps_to_plot = {
    cpp_col1: {'param': 'CPP - IEX Pool Conductivity (mS/cm)', 'color': '#F36633'},
    cpp_col2: {'param': 'CPP - IEX Load Density (g/L)', 'color': '#8DC63F'},
    cpp_col3: {'param': 'CPP - Elution Buffer pH', 'color': '#6F1D77'},
}
for col, info in cpps_to_plot.items():
    with col:
        st.markdown(f"**{info['param']}**")
        fig = create_control_chart(cpv_df, info['param'], info['color'])
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 3. Critical Material Attributes (CMAs) ---
st.subheader("III. Critical Material Attribute (CMA) Monitoring")
st.markdown("CMAs are properties of our input materials that can impact the process.")

cma_col1, cma_col2 = st.columns(2)
with cma_col1:
    parameter = 'CMA - Resin Age (cycles)'
    st.markdown(f"**{parameter}**")
    fig = px.line(cpv_df, x='Batch ID', y=parameter, title="Resin Usage Trend", markers=True, line_shape="linear")
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with cma_col2:
    parameter = 'CMA - Buffer Lot ID'
    st.markdown(f"**{parameter}**")
    fig = px.scatter(cpv_df, x='Batch ID', y=parameter, title="Buffer Lot Changes", color=parameter)
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10), yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
    
st.divider()

# --- 4. Multivariate Analysis ---
st.header("IV. Multivariate Analysis: Linking Inputs to Outcomes")
with st.expander("**Correlation Matrix & Overall MSAT Interpretation**", expanded=True):
    st.markdown("""
    **Purpose:** This correlation matrix is the key to understanding the entire system. It visualizes the strength and direction of the relationships between all our tracked parameters, allowing us to form scientifically sound hypotheses during investigations.
    """)
    
    numeric_df = cpv_df.select_dtypes(include=np.number)
    corr_df = numeric_df.corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title="Correlation Heatmap of CQAs, CPPs, and CMAs"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    ### Overall MSAT Conclusion & Action Plan
    
    This holistic CPV analysis tells a clear, data-driven story that would be impossible to see by looking at charts in isolation:
    
    1.  **The Problem:** Our most important CQA, **Purity**, is exhibiting a clear downward trend, and its process capability is unacceptable (Ppk < 1.0). Our secondary CQA, **Step Yield**, is also showing a similar, though less severe, decline.
    2.  **The Clues:** The control charts for all three CPPs—**Conductivity, Load Density, and pH**—are stable and in a state of control (excluding one historical special cause for conductivity). This indicates the CDMO is operating the process consistently according to the batch record. The problem is not in their execution.
    3.  **The Smoking Gun:** The control chart for the CMA, **Resin Age**, shows a steady increase as expected. The **Correlation Matrix** provides the critical link, revealing a very strong **negative correlation (r = -0.96)** between **CMA - Resin Age** and **CQA - Purity**.
    
    **Action Plan as MSAT Lead:**
    - **Definitive Conclusion:** The process is not failing; the *resin* is failing. The declining purity is a direct result of the chromatography resin nearing the end of its validated lifetime. Its ability to clear impurities is degrading with each successive cycle.
    - **Corrective Action:** I will issue a formal recommendation to the CDMO to discard the current resin pack and prepare the column with a new lot of resin before the next campaign begins.
    - **Preventive Action (Lifecycle Management):** This data provides the justification to tighten our control strategy. I will initiate a change control to reduce the validated lifetime of the IEX resin from its current limit (e.g., 250 cycles) to a more conservative 200 cycles. This ensures that we prevent this degradation from impacting product quality in the future, demonstrating effective lifecycle management to regulatory authorities.
    """)

# --- Helper Functions for this page ---
def calculate_ppk(data_series, usl, lsl):
    mean = data_series.mean()
    std_dev = data_series.std()
    if std_dev == 0: return np.inf
    ppu = (usl - mean) / (3 * std_dev)
    ppl = (mean - lsl) / (3 * std_dev)
    return min(ppu, ppl)

def create_control_chart(df, parameter, color):
    mean = df[parameter].mean()
    ucl = mean + 3 * df[parameter].std()
    lcl = mean - 3 * df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green", opacity=0.8)
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", opacity=0.8)
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", opacity=0.8)
    fig.add_trace(go.Scatter(x=df['Batch ID'], y=df[parameter], mode='lines+markers', name=parameter, line_color=color))
    
    out_of_control = df[(df[parameter] > ucl) | (df[parameter] < lcl)]
    if not out_of_control.empty:
        fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='OOC'))
        
    fig.update_layout(height=300, margin=dict(t=10, b=20, l=10, r=10), showlegend=False)
    return fig
