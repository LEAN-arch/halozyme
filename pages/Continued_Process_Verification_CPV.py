# pages/Continued_Process_Verification_CPV.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_cpv_data
from scipy.stats import norm

st.set_page_config(
    page_title="CPV Dashboard | Halozyme",
    layout="wide"
)

st.title("📈 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of our commercial downstream manufacturing process for rHuPH20 at **CDMO Alpha**.")

with st.expander("🌐 The Role of CPV & Regulatory Context"):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that the process remains in a state of control during routine commercial manufacturing. As the MSAT lead, this is a cornerstone of my lifecycle management responsibilities.

    - **FDA Process Validation Guidance (Stage 3):** This guidance explicitly calls for an ongoing program to collect and analyze product and process data that relate to product quality. This dashboard is our primary tool for fulfilling this requirement.
    - **ICH Q8 (Pharmaceutical Development):** CPV is a key component of lifecycle management, ensuring that the process remains within the established **Design Space**.
    - **Purpose:** This dashboard is used to:
        1.  Monitor Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) using statistical control charts.
        2.  Detect and investigate any unexpected process variability or trends.
        3.  Periodically assess the Process Capability (Cpk/Ppk) to ensure we can consistently meet our quality specifications.
        4.  Provide data for Annual Product Quality Reviews (APQRs) and regulatory inspections.
    """)

# --- Data Generation ---
cpv_df = generate_cpv_data()

# --- Integrated Dashboard Layout ---
st.header("Holistic View: IEX Chromatography Step Performance")
st.markdown("Analyzing a Critical Quality Attribute (**Purity**) alongside the Critical Process Parameters (CPPs) that influence it.")
st.divider()

# --- 1. CQA Monitoring & Capability ---
cqa_col1, cqa_col2 = st.columns([1.5, 1])
with cqa_col1:
    st.subheader("CQA Control Chart: Purity by RP-HPLC (%)")
    parameter_to_plot = 'Purity (%)'
    mean = cpv_df[parameter_to_plot].mean()
    std = cpv_df[parameter_to_plot].std()
    ucl, lcl = mean + 3 * std, mean - 3 * std
    
    fig_spc = go.Figure()
    fig_spc.add_hline(y=mean, line_dash="solid", line_color="green", annotation_text="Mean")
    fig_spc.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL (+3σ)")
    fig_spc.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL (-3σ)")
    fig_spc.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter_to_plot], mode='lines+markers', name=parameter_to_plot))
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

    ppk_value = calculate_ppk(cpv_df[parameter_to_plot], usl, lsl)
    
    st.metric("Process Performance (Ppk)", f"{ppk_value:.2f}")
    if ppk_value < 1.0: st.error("NOT CAPABLE")
    elif ppk_value < 1.33: st.warning("MARGINALLY CAPABLE")
    else: st.success("CAPABLE")
    
    st.markdown("**Specification Limits:**")
    st.write(f"LSL: {lsl}%, USL: {usl}%")
    st.markdown("""
    **MSAT Interpretation:** The control chart reveals a clear downward trend in purity over the last 20 batches. While no single batch has failed, this process drift has severely impacted our process capability. The **Ppk of 0.95** is unacceptable and indicates a high likelihood of future OOS results. This requires immediate investigation.
    """)

st.divider()

# --- 2. CPP Monitoring ---
st.header("Influencing CPP Control Charts")
cpp_col1, cpp_col2 = st.columns(2)
with cpp_col1:
    st.subheader("CPP: IEX Pool Conductivity (mS/cm)")
    parameter = 'Conductivity (mS/cm)'
    mean = cpv_df[parameter].mean()
    ucl, lcl = mean + 3 * cpv_df[parameter].std(), mean - 3 * cpv_df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green")
    fig.add_hline(y=ucl, line_dash="dash", line_color="red")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red")
    fig.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter], mode='lines+markers', name=parameter, line_color='#F36633'))
    
    # Highlight Out-of-Control Points
    out_of_control = cpv_df[(cpv_df[parameter] > ucl) | (cpv_df[parameter] < lcl)]
    if not out_of_control.empty:
        fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='Out of Control'))
    
    fig.update_layout(height=350, margin=dict(t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)

with cpp_col2:
    st.subheader("CPP: Concentration Factor")
    parameter = 'Concentration Factor'
    mean = cpv_df[parameter].mean()
    ucl, lcl = mean + 3 * cpv_df[parameter].std(), mean - 3 * cpv_df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green")
    fig.add_hline(y=ucl, line_dash="dash", line_color="red")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red")
    fig.add_trace(go.Scatter(x=cpv_df['Batch ID'], y=cpv_df[parameter], mode='lines+markers', name=parameter, line_color='#00A9E0'))
    fig.update_layout(height=350, margin=dict(t=20, b=0))
    st.plotly_chart(fig, use_container_width=True)
    
st.divider()

# --- 3. Multivariate Analysis ---
st.header("Multivariate Analysis: Understanding Relationships")
with st.expander("**Correlation Matrix & MSAT Interpretation**"):
    st.markdown("""
    **Purpose:** Real-world manufacturing processes are multivariate. A CQA is often influenced by multiple CPPs acting together. A correlation matrix helps us visualize the strength and direction of these relationships, which is critical for effective troubleshooting. A strong correlation (positive or negative) between a CPP and a CQA provides a clear hypothesis for investigation when a process drifts.
    
    **Methodology:** We calculate the **Pearson correlation coefficient (r)** for each pair of parameters.
    - **r = +1.0:** Perfect positive linear correlation.
    - **r = -1.0:** Perfect negative linear correlation.
    - **r = 0.0:** No linear correlation.
    
    The results are displayed as a heatmap, where warmer colors (red) indicate a positive correlation and cooler colors (blue) indicate a negative correlation.
    """)
    
    corr_df = cpv_df.drop(columns='Batch ID').corr()
    fig_corr = px.imshow(
        corr_df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale='RdBu_r',
        zmin=-1, zmax=1,
        title="Correlation Heatmap of CPPs and CQAs"
    )
    st.plotly_chart(fig_corr, use_container_width=True)

    st.markdown("""
    ### Overall MSAT Conclusion & Action Plan
    
    This holistic CPV analysis tells a clear story that would be missed by looking at charts in isolation:
    
    1.  **The Problem:** Our primary CQA, **Purity**, is in a state of drift and its process capability is unacceptable (Ppk=0.95).
    2.  **The Clues:** The control charts for the CPPs show that **Concentration Factor** is stable, but **Conductivity** had a significant special cause event and may be exhibiting some instability.
    3.  **The Hypothesis:** The **Correlation Matrix** provides the critical link. It shows a moderately strong **negative correlation (-0.62)** between **Conductivity** and **Purity**. This is scientifically sound, as higher conductivity in an IEX pool can lead to premature elution of weakly-bound impurities, thereby lowering the final purity.
    
    **Action Plan as MSAT Lead:**
    - **Immediate Investigation:** I will lead a technical deep-dive with the CDMO, focusing specifically on their buffer preparation and in-line conductivity monitoring for the IEX step. The special cause event in batch B0140 is the starting point for this investigation.
    - **Proactive Monitoring:** I will increase the monitoring frequency of this step and request additional data from the CDMO until the root cause of the drift is identified and corrected.
    - **Report & Escalate:** This complete data package will be used to formally document the process trend and justify the need for corrective actions to both internal management and the CDMO.
    """)
