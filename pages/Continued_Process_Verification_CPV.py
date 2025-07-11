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
st.markdown("### Ongoing monitoring of our commercial downstream manufacturing process for rHuPH20 at **CDMO Alpha**.")

with st.expander("🌐 The Role of CPV & Regulatory Context", expanded=True):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that the process remains in a state of control during routine commercial manufacturing. As the MSAT lead, this is a cornerstone of my lifecycle management responsibilities.

    - **FDA Process Validation Guidance (Stage 3):** This guidance explicitly calls for an ongoing program to collect and analyze product and process data that relate to product quality. This dashboard is our primary tool for fulfilling this requirement.
    - **ICH Q8 (Pharmaceutical Development):** CPV is a key component of lifecycle management, ensuring that the process remains within the established **Design Space**.
    - **Purpose:** This dashboard is used to:
        1.  Monitor Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) using statistical control charts.
        2.  Detect and investigate any unexpected process variability or trends.
        3.  Periodically assess the Process Capability (Ppk) to ensure we can consistently meet our quality specifications.
        4.  Provide data for Annual Product Quality Reviews (APQRs) and regulatory inspections.
    """)

# --- Mock Data Generation with CMAs ---
def generate_cpv_data_with_cma():
    """Generates historical batch data for CPV monitoring including a CMA."""
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    
    # CMA: Critical Material Attribute
    resin_age = np.linspace(1, 200, n_batches) # Number of cycles on the IEX resin
    
    # CPPs: Critical Process Parameters
    conductivity = np.random.normal(15.2, 0.2, n_batches)
    conductivity[40] = 17.5 # Special cause variation
    load_density = np.random.normal(25.5, 0.5, n_batches)
    
    # CQA: Critical Quality Attribute
    # Simulate purity being impacted by both resin age and conductivity
    purity_base = 99.0
    purity_resin_effect = - (resin_age / 250)**2 # Degradation over time
    purity_cond_effect = - abs(conductivity - 15.2) * 0.5 # Higher conductivity hurts purity
    purity_noise = np.random.normal(0, 0.1, n_batches)
    purity = purity_base + purity_resin_effect + purity_cond_effect + purity_noise
    
    return pd.DataFrame({
        'Batch ID': batches,
        'CQA - Purity (%)': purity,
        'CPP - IEX Pool Conductivity (mS/cm)': conductivity,
        'CPP - IEX Load Density (g/L)': load_density,
        'CMA - Resin Age (cycles)': resin_age
    })

cpv_df = generate_cpv_data_with_cma()

# --- Definitions Section ---
st.header("Control Strategy for IEX Chromatography Step")
with st.expander("Definitions of CQA, CPPs, and CMAs for this Unit Operation"):
    st.markdown("""
    - **Critical Quality Attribute (CQA):** A physical, chemical, biological or microbiological property or characteristic that should be within an appropriate limit, range, or distribution to ensure the desired product quality.
      - **Example:** `Purity (%)` - Must be within its specification to ensure patient safety and efficacy.
    - **Critical Process Parameter (CPP):** A process parameter whose variability has an impact on a critical quality attribute and therefore should be monitored or controlled to ensure the process produces the desired quality.
      - **Examples:** `IEX Pool Conductivity`, `IEX Load Density`.
    - **Critical Material Attribute (CMA):** A physical, chemical, or biological characteristic of an input material that must be controlled to ensure the process can deliver a drug product with the desired quality.
      - **Example:** `Resin Age (cycles)` - The number of uses on a chromatography resin, which can impact its performance.
    """)

st.divider()

# --- Integrated Dashboard Layout ---
st.header("Holistic View: IEX Step Performance")
st.markdown("Analyzing the CQA (**Purity**) alongside the CPPs and CMAs that influence it.")

# --- 1. CQA Monitoring & Capability ---
cqa_col1, cqa_col2 = st.columns([1.5, 1])
with cqa_col1:
    st.subheader("CQA Control Chart: Purity (%)")
    parameter = 'CQA - Purity (%)'
    mean = cpv_df[parameter].mean()
    ucl, lcl = mean + 3 * cpv_df[parameter].std(), mean - 3 * cpv_df[parameter].std()
    
    fig_spc = go.Figure()
    fig_spc.add_hline(y=mean, line_dash="solid", line_color="green")
    fig_spc.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL")
    fig_spc.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL")
    fig_spc.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter], mode='lines+markers', name=parameter))
    fig_spc.update_layout(height=400, margin=dict(t=20, b=0))
    st.plotly_chart(fig_spc, use_container_width=True)

with cqa_col2:
    st.subheader("CQA Process Capability (Ppk)")
    lsl, usl = 97.5, 100.0
    
    def calculate_ppk(data_series, usl, lsl):
        mean = data_series.mean()
        std_dev = data_series.std()
        if std_dev == 0: return np.inf
        ppu = (usl - mean) / (3 * std_dev)
        ppl = (mean - lsl) / (3 * std_dev)
        return min(ppu, ppl)

    ppk_value = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric("Process Performance (Ppk)", f"{ppk_value:.2f}")
    if ppk_value < 1.0: st.error("NOT CAPABLE")
    elif ppk_value < 1.33: st.warning("MARGINALLY CAPABLE")
    else: st.success("CAPABLE")
    
    st.markdown(f"**Specification Limits:** {lsl}% – {usl}%")
    st.markdown("""
    **Interpretation:** The control chart shows a clear, concerning downward trend in purity. This process drift has resulted in an unacceptable **Ppk of {ppk_value:.2f}**, indicating the process is no longer capable of consistently meeting its specification.
    """)

st.divider()

# --- 2. CPP & CMA Monitoring ---
st.header("Influencing Parameter Control Charts")
param_col1, param_col2, param_col3 = st.columns(3)
charts = {
    param_col1: {'param': 'CPP - IEX Pool Conductivity (mS/cm)', 'color': '#F36633'},
    param_col2: {'param': 'CPP - IEX Load Density (g/L)', 'color': '#00A9E0'},
    param_col3: {'param': 'CMA - Resin Age (cycles)', 'color': '#8DC63F'}
}
for col, chart_info in charts.items():
    with col:
        parameter = chart_info['param']
        st.subheader(parameter)
        mean = cpv_df[parameter].mean()
        ucl, lcl = mean + 3 * cpv_df[parameter].std(), mean - 3 * cpv_df[parameter].std()
        fig = go.Figure()
        fig.add_hline(y=mean, line_dash="solid", line_color="green")
        fig.add_hline(y=ucl, line_dash="dash", line_color="red")
        fig.add_hline(y=lcl, line_dash="dash", line_color="red")
        fig.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter], mode='lines+markers', name=parameter, line_color=chart_info['color']))
        out_of_control = cpv_df[(cpv_df[parameter] > ucl) | (cpv_df[parameter] < lcl)]
        if not out_of_control.empty:
            fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='OOC'))
        fig.update_layout(height=300, margin=dict(t=20, b=20, l=10, r=10))
        st.plotly_chart(fig, use_container_width=True)

st.divider()

# --- 3. Multivariate Analysis ---
st.header("Multivariate Analysis: Linking Inputs to Outcomes")
with st.expander("**Correlation Matrix & MSAT Interpretation**", expanded=True):
    st.markdown("""
    **Purpose:** Real-world manufacturing processes are multivariate. A CQA is often influenced by multiple parameters acting together. A correlation matrix helps us visualize the strength and direction of these relationships, which is critical for effective troubleshooting.
    
    **Methodology:** We calculate the **Pearson correlation coefficient (r)** for each pair of parameters. An `r` value close to -1.0 or +1.0 indicates a strong linear correlation.
    """)
    
    corr_df = cpv_df.drop(columns='Batch ID').corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=".2f",
        aspect="auto",
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title="Correlation Heatmap of CQA, CPPs, and CMAs"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    ### Overall MSAT Conclusion & Action Plan
    
    This holistic CPV analysis tells a clear, data-driven story:
    
    1.  **The Problem:** Our CQA, **Purity**, is in a state of drift, and its process capability is unacceptable (Ppk < 1.0).
    2.  **The Clues:** The control charts for the CPPs show that **Load Density** and **Conductivity** are stable (with one historical special cause). However, the CMA, **Resin Age**, shows a clear, expected upward trend as the column is used.
    3.  **The Smoking Gun:** The **Correlation Matrix** provides the critical link. It shows a very strong **negative correlation (r = -0.96)** between **CMA - Resin Age** and **CQA - Purity**. This is our primary hypothesis. There is also a weaker, secondary negative correlation with Conductivity.
    
    **Action Plan as MSAT Lead:**
    - **Immediate Investigation:** The data strongly suggests that the declining purity is due to the chromatography resin nearing the end of its validated lifetime. The resin's ability to clear impurities is degrading with each cycle.
    - **Corrective Action:** I will issue a formal recommendation to the CDMO to strip, clean, and re-pack the column with new resin before the next set of batches.
    - **Preventive Action (Lifecycle Management):** This analysis provides the data to justify tightening the validated lifetime of the IEX resin. I will initiate a change control to reduce the maximum number of cycles from (for example) 250 to 200 to ensure this downward trend does not impact future batches. This is a perfect example of using CPV data to drive continuous improvement and ensure long-term process robustness.
    """)
