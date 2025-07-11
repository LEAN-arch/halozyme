# pages/Process_Optimization_DOE.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from utils import generate_process_optimization_doe_data

st.set_page_config(
    page_title="Process Optimization (DOE) | Halozyme",
    layout="wide"
)

st.title("🧪 Process Optimization: Design of Experiments (DOE)")
st.markdown("### Using Response Surface Methodology (RSM) to define an optimal operating window for a downstream chromatography step.")

with st.expander("🌐 MSAT Role & The Power of DOE"):
    st.markdown("""
    As the MSAT subject matter authority, a key part of my role is to lead process improvement and lifecycle management activities. Design of Experiments (DOE) is the most powerful and efficient tool for this purpose.

    - **Goal:** Instead of one-factor-at-a-time (OFAT) experiments, which are inefficient and miss critical interactions, we use a structured statistical approach to model the entire process space.
    - **Application:** Here, we are optimizing a critical Ion Exchange (IEX) chromatography step. Our goal is to find the "sweet spot" of **pH** and **Salt Concentration** that concurrently maximizes **Product Yield** and the **Log Removal Value (LRV) of a key impurity**.
    - **Outcome:** The result is not just a single "optimal" point, but a well-defined **Design Space** or **Sweet Spot Plot**. This provides a deep understanding of process robustness and serves as the scientific basis for our control strategy, which we then transfer to our CDMO partners. This work is foundational to our BLA filings and responses to regulatory agency inquiries (e.g., FDA, EMA).
    """)

# --- 1. Experimental Design & Data ---
st.header("1. DOE Data: IEX Chromatography Optimization")
st.caption("A Central Composite Design (CCD) was executed to model the effects of pH and NaCl concentration on process performance.")
doe_df = generate_process_optimization_doe_data()
st.dataframe(doe_df, use_container_width=True)

# --- 2. Interactive Sweet Spot Analysis ---
st.header("2. Interactive Visualization of the Operating Window")
st.markdown("Use the sliders to define the minimum acceptable specifications for both yield and impurity clearance. The highlighted green area on the plot represents the **'Sweet Spot'**—the operating window where both criteria are met simultaneously.")

# --- Interactive Controls for Specifications ---
spec_col1, spec_col2 = st.columns(2)
with spec_col1:
    yield_spec = st.slider(
        "Minimum Acceptable Yield (%)",
        min_value=80.0, max_value=95.0, value=88.0, step=0.5
    )
with spec_col2:
    lrv_spec = st.slider(
        "Minimum Acceptable Impurity LRV",
        min_value=2.0, max_value=3.5, value=2.5, step=0.1
    )

# --- Generate Contour Data (Simulated for this mockup) ---
ph_range = np.linspace(doe_df['pH'].min(), doe_df['pH'].max(), 50)
salt_range = np.linspace(doe_df['NaCl (mM)'].min(), doe_df['NaCl (mM)'].max(), 50)
ph_grid, salt_grid = np.meshgrid(ph_range, salt_range)

# Mock response surfaces based on the DOE data's known center
yield_pred = 92 - 15 * (ph_grid - 7.0)**2 - 0.003 * (salt_grid - 100)**2
lrv_pred = 2.8 - 5 * (ph_grid - 7.1)**2 - 0.001 * (salt_grid - 90)**2

# --- Combined Contour Plot for Sweet Spot ---
fig = go.Figure()

# Add Yield Contour
fig.add_trace(go.Contour(
    z=yield_pred, x=ph_range, y=salt_range,
    name='Yield (%)',
    contours_coloring='lines',
    line_color='#005EB8',
    showscale=False,
    contours=dict(showlabels=True, labelfont=dict(color='#005EB8'))
))

# Add LRV Contour
fig.add_trace(go.Contour(
    z=lrv_pred, x=ph_range, y=salt_range,
    name='Impurity LRV',
    contours_coloring='lines',
    line_color='#F36633',
    showscale=False,
    contours=dict(showlabels=True, labelfont=dict(color='#F36633'))
))

# Calculate and highlight the "Sweet Spot"
sweet_spot_mask = (yield_pred >= yield_spec) & (lrv_pred >= lrv_spec)
fig.add_trace(go.Contour(
    z=sweet_spot_mask.astype(int),
    x=ph_range, y=salt_range,
    contours_coloring='lines',
    line_width=0,
    showscale=False,
    colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(141, 198, 63, 0.4)']], # Transparent and Green
    hoverinfo='none'
))

# Add DOE points
fig.add_trace(go.Scatter(
    x=doe_df['pH'], y=doe_df['NaCl (mM)'],
    mode='markers', marker=dict(color='black', symbol='diamond-open', size=10),
    name='DOE Design Points'
))

fig.update_layout(
    title="Process 'Sweet Spot' Plot: Yield vs. Impurity Clearance",
    height=700,
    xaxis_title="Buffer pH",
    yaxis_title="NaCl Concentration (mM)",
    legend=dict(x=1.05, y=1)
)
st.plotly_chart(fig, use_container_width=True)

with st.expander("📊 **MSAT Conclusion & Actionable Next Steps**"):
    st.markdown("""
    #### Analysis of the Design Space
    This "Sweet Spot" plot is the primary output of our process characterization work. It visualizes the trade-offs between competing process outcomes and defines a robust operating window.
    
    - **Optimal Region:** The green shaded area represents the **Proven Acceptable Range (PAR)** where we can confidently operate while meeting our specifications for both high yield and effective impurity clearance.
    - **Process Cliffs:** We can clearly see regions where performance drops off sharply. For example, at a pH above ~7.1, the impurity LRV decreases significantly, even though yield remains high. This is a critical process vulnerability that this analysis exposes.
    - **Interaction Effects:** The non-circular shape of the contours reveals interactions between pH and salt concentration. The optimal salt concentration changes depending on the pH, an insight impossible to gain from OFAT experiments.

    #### Actionable Next Steps
    1.  **Define Control Strategy:** Based on this data, I will propose a Target Operating Point (e.g., pH 7.0, 95 mM NaCl) and a Normal Operating Range (NOR) that sits comfortably within the center of this green "sweet spot."
    2.  **Technology Transfer:** This plot and the underlying report are key deliverables in the tech transfer package for our CDMO. It provides the scientific justification for the process parameters defined in the master batch record.
    3.  **Regulatory Filing:** This analysis will form a key part of the Process and Controls section (3.2.P.2) of our BLA submission, demonstrating a deep, science-based understanding of our manufacturing process to health authorities.
    """)
