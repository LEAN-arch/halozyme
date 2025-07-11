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
st.markdown("### Ongoing monitoring of our commercial downstream manufacturing process for rHuPH20.")

with st.expander("🌐 The Role of CPV & Regulatory Context"):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that the process remains in a state of control during routine commercial manufacturing. As the MSAT lead, this is a cornerstone of my lifecycle management responsibilities.

    - **FDA Process Validation Guidance (Stage 3):** This guidance explicitly calls for an ongoing program to collect and analyze product and process data that relate to product quality. This dashboard is our primary tool for fulfilling this requirement.
    - **ICH Q8 (Pharmaceutical Development):** CPV is a key component of lifecycle management, ensuring that the process remains within the established **Design Space**.
    - **Purpose:** This dashboard is used to:
        1.  Monitor Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) using statistical control charts.
        2.  Detect and investigate any unexpected process variability or trends.
        3.  Periodically assess the Process Capability (Cpk) to ensure we can consistently meet our quality specifications.
        4.  Provide data for Annual Product Quality Reviews (APQRs).
    """)

# --- Data Generation ---
cpv_df = generate_cpv_data()

# --- Select Parameter to Analyze ---
st.header("Select a Parameter for CPV Analysis")
parameter_to_plot = st.selectbox(
    "Select a Critical Process Parameter (CPP) or Critical Quality Attribute (CQA):",
    cpv_df.columns.drop('Batch ID').tolist()
)
st.divider()

# --- 1. Statistical Process Control (SPC) Chart ---
st.header(f"1. Control Chart for: **{parameter_to_plot}**")
st.caption("Monitoring batch-to-batch performance to detect process shifts or special cause variation.")

# SPC Chart Logic
mean = cpv_df[parameter_to_plot].mean()
std = cpv_df[parameter_to_plot].std()
ucl = mean + 3 * std  # Upper Control Limit
lcl = mean - 3 * std  # Lower Control Limit

fig_spc = go.Figure()

# Add Control Limits
fig_spc.add_hline(y=mean, line_dash="solid", line_color="green", annotation_text="Mean")
fig_spc.add_hline(y=ucl, line_dash="dash", line_color="red", annotation_text="UCL (+3σ)")
fig_spc.add_hline(y=lcl, line_dash="dash", line_color="red", annotation_text="LCL (-3σ)")

# Add Data Trace
fig_spc.add_trace(go.Scatter(
    x=cpv_df['Batch ID'], y=cpv_df[parameter_to_plot],
    mode='lines+markers', name=parameter_to_plot
))

# Highlight Out-of-Control Points
out_of_control = cpv_df[(cpv_df[parameter_to_plot] > ucl) | (cpv_df[parameter_to_plot] < lcl)]
if not out_of_control.empty:
    fig_spc.add_trace(go.Scatter(
        x=out_of_control['Batch ID'], y=out_of_control[parameter_to_plot],
        mode='markers', marker=dict(color='red', size=12, symbol='x'),
        name='Out of Control'
    ))

fig_spc.update_layout(
    title=f"I-Chart for {parameter_to_plot}",
    xaxis_title="Batch ID",
    yaxis_title=parameter_to_plot,
    xaxis={'type': 'category'}
)
st.plotly_chart(fig_spc, use_container_width=True)

with st.expander("🔬 **MSAT Analysis of Control Chart**"):
    st.markdown("""
    The control chart is our first line of defense in detecting process changes. We are looking for two things:
    1.  **Special Cause Variation:** Individual points that fall outside the ±3σ control limits. These represent unexpected, significant events that require immediate investigation.
    2.  **Process Drift / Trends:** Non-random patterns in the data, such as 7 or more consecutive points on one side of the mean, which can indicate a subtle but real shift in the process.

    **Current Analysis:**
    - For **Purity (%)**, the chart shows a clear downward shift starting around batch B0130. While no points breach the control limits, this trend is a signal of a process change that warrants investigation.
    - For **Conductivity (mS/cm)**, batch B0140 is a clear out-of-control point (special cause variation), indicating a significant one-time event, likely a buffer preparation error at the CDMO. This would have triggered a formal deviation.
    """)

st.divider()

# --- 2. Process Capability Analysis (Cpk) ---
st.header(f"2. Process Capability Analysis for: **{parameter_to_plot}**")
st.caption("Assessing how well our process is able to meet its defined specification limits.")

# Cpk Logic
spec_limits = {
    'Purity (%)': (97.5, 100.0),
    'Conductivity (mS/cm)': (14.0, 16.5),
    'Concentration Factor': (9.5, 10.5)
}
lsl, usl = spec_limits[parameter_to_plot]

def calculate_cpk(data_series, usl, lsl):
    mean = data_series.mean()
    std_dev = data_series.std()
    if std_dev == 0: return np.inf
    cpu = (usl - mean) / (3 * std_dev)
    cpl = (mean - lsl) / (3 * std_dev)
    return min(cpu, cpl)

cpk_value = calculate_cpk(cpv_df[parameter_to_plot], usl, lsl)

col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("Capability Metrics")
    st.metric("Lower Spec Limit (LSL)", f"{lsl}")
    st.metric("Upper Spec Limit (USL)", f"{usl}")
    st.metric("Process Capability Index (Cpk)", f"{cpk_value:.2f}")

    if cpk_value < 1.0:
        st.error("**NOT CAPABLE:** Process is producing out-of-spec material.")
    elif cpk_value < 1.33:
        st.warning("**MARGINALLY CAPABLE:** Process is at high risk of failure. Improvement is recommended.")
    else:
        st.success("**CAPABLE:** Process consistently meets specifications.")

    with st.expander("Cpk Explained"):
        st.markdown("""
        **Cpk** measures how centered and "narrow" our process is relative to the specification limits. It answers the question: "How much room for error do we have?"
        - A value of **1.0** means the process distribution just touches the nearest spec limit.
        - A value of **1.33** is a common industry target for a capable process.
        - A value of **1.67** or higher is considered excellent (Six Sigma capability).
        """)

with col2:
    st.subheader("Process Distribution vs. Specification Limits")
    fig_hist = px.histogram(
        cpv_df, x=parameter_to_plot, nbins=20,
        histnorm='probability density', title="Process Capability Histogram"
    )
    # Add Normal distribution curve
    x_range = np.linspace(cpv_df[parameter_to_plot].min(), cpv_df[parameter_to_plot].max(), 200)
    fig_hist.add_trace(go.Scatter(
        x=x_range, y=norm.pdf(x_range, mean, std),
        mode='lines', name='Normal Fit', line=dict(color='firebrick')
    ))
    # Add Spec Limits
    fig_hist.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
    fig_hist.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
    st.plotly_chart(fig_hist, use_container_width=True)

with st.expander("🔬 **MSAT Analysis of Process Capability**"):
    st.markdown(f"""
    #### Analysis for {parameter_to_plot}:
    The histogram shows the "Voice of the Process" (how it actually performs) against the "Voice of the Customer" (the specification limits we must meet).

    - **The Cpk value of {cpk_value:.2f}** provides a quantitative assessment.
    - If Cpk is low, the plot helps diagnose why. Is the process off-center (a mean shift issue)? Or is the distribution too wide (a variability issue)?
    
    **Example Analysis (Purity %):** The Cpk is likely marginal (<1.33). The histogram would show the process mean is centered, but the recent downward shift has widened the overall distribution, pushing the left tail dangerously close to the Lower Specification Limit of 97.5%.

    **Action as MSAT Lead:** A low Cpk, combined with an adverse trend on the control chart, is a strong signal that intervention is needed. I would initiate a formal investigation with the CDMO to identify the root cause of the process drift. The goal is to implement corrective actions that re-center the process and reduce variability, thereby improving our Cpk and ensuring long-term product quality and supply reliability.
    """)
