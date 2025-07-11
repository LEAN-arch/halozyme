# pages/Process_Characterization_Hub.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_chromatography_data, generate_ufdf_data
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

st.set_page_config(
    page_title="Process Characterization | Halozyme",
    layout="wide"
)

st.title("🔬 Process Characterization Hub")
st.markdown("### Analysis of key performance data from downstream unit operation characterization studies.")

with st.expander("🌐 Regulatory Context: The Role of Process Characterization"):
    st.markdown("""
    Process Characterization (PC) is a cornerstone of our CMC (Chemistry, Manufacturing, and Controls) strategy. It involves a series of laboratory-scale studies designed to identify and understand the relationships between process parameters and product quality attributes. As a Principal MSAT Engineer, I use this data to:

    - **Establish a Control Strategy:** Define Critical Process Parameters (CPPs), Key Process Parameters (KPPs), and their Proven Acceptable Ranges (PARs).
    - **Support Process Validation:** The data generated here provides the scientific rationale for the operating ranges used during full-scale Process Validation (PV) campaigns at our CDMOs.
    - **Author Regulatory Submissions:** PC study reports are a critical component of our Biologics License Application (BLA) and other global regulatory filings. They demonstrate a fundamental understanding of our manufacturing process, which is a key expectation of agencies like the FDA and EMA.
    - **Lifecycle Management (ICH Q8, Q11):** These studies define the **Design Space**, allowing for more flexible post-approval manufacturing changes and providing a basis for our Continued Process Verification (CPV) program.
    """)

# --- Mock Data Generation ---
chrom_normal_df = generate_chromatography_data(high_impurity=False)
chrom_fail_df = generate_chromatography_data(high_impurity=True)
ufdf_df = generate_ufdf_data()

def generate_viral_filtration_data():
    """Generates data for a viral filtration capacity study."""
    throughput = np.linspace(0, 1000, 50) # L/m^2
    initial_flow = 200 # L/hr
    decay_rate = 0.00015
    flow_rate = initial_flow - (decay_rate * throughput**2) + np.random.normal(0, 2, 50)
    flow_rate = np.clip(flow_rate, 0, initial_flow)
    pressure = 10 + 0.02 * throughput + np.random.normal(0, 0.5, 50)
    pressure[flow_rate < 100] += np.linspace(0, 5, len(pressure[flow_rate < 100]))
    return pd.DataFrame({'Throughput (L/m²)': throughput, 'Flow Rate (L/hr)': flow_rate, 'Pressure (psi)': pressure})

viral_df = generate_viral_filtration_data()


# --- Page Tabs for Downstream Unit Operations ---
tab1, tab2, tab3 = st.tabs([
    "**Chromatography Performance**",
    "**Ultrafiltration/Diafiltration (UF/DF)**",
    "**Viral Filtration Characterization**"
])

with tab1:
    st.header("Chromatography Step Characterization")
    st.caption("Analysis of elution profiles to assess yield, purity, and impurity clearance.")
    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""...""") # Hidden for brevity
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Standard (Successful) Run")
        fig_normal = px.line(chrom_normal_df, x="Time (min)", y="UV (mAU)", title="Chromatogram: Standard Run")
        st.plotly_chart(fig_normal, use_container_width=True)
        st.success("**Analysis:** Excellent separation.")
        st.metric("Product / Impurity 2 Resolution (Rₛ)", "1.65")
    with col2:
        st.subheader("Worst-Case (Failed) Run")
        fig_fail = px.line(chrom_fail_df, x="Time (min)", y="UV (mAU)", title="Chromatogram: Worst-Case Run")
        st.plotly_chart(fig_fail, use_container_width=True)
        st.error("**Analysis:** Poor separation.")
        st.metric("Product / Impurity 2 Resolution (Rₛ)", "0.85")
    with st.expander("📊 **Conclusion & Actionable Insights for Tech Transfer**"):
        st.markdown("""...""") # Hidden for brevity

with tab2:
    st.header("Ultrafiltration/Diafiltration (UF/DF) Performance")
    st.caption("Analyzing transmembrane pressure (TMP) and flux to monitor membrane performance and detect fouling.")
    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""...""") # Hidden for brevity
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['Flux (LMH)'], name='Flux (LMH)', line=dict(color='#005EB8')))
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['TMP (psi)'], name='TMP (psi)', yaxis='y2', line=dict(color='#F36633')))
    fig.add_vline(x=ufdf_df['Volume (L)'][20], line_width=2, line_dash="dash", line_color="red", annotation_text="Fouling Event", annotation_position="top left")
    fig.update_layout(title="UF/DF Performance: Flux and TMP vs. Process Volume", xaxis_title="In-Process Volume (L) - (Concentrating)", yaxis=dict(title="<b>Flux (LMH)</b>", color='#005EB8'), yaxis2=dict(title="<b>TMP (psi)</b>", color='#F36633', overlaying='y', side='right'), legend=dict(x=0.8, y=0.95), xaxis_autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
    with st.expander("📊 **Results & Analysis**"):
        st.markdown("""...""") # Hidden for brevity

with tab3:
    st.header("Viral Filtration Characterization")
    st.caption("Determining viral filter capacity and defining operational parameters for robust viral clearance.")
    
    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""
        #### The Experiment
        Viral filtration is a critical unit operation dedicated to removing potential viral contaminants. This characterization study, often performed using a scaled-down model, is designed to determine the **maximum processing capacity** of a specific viral filter with our product (e.g., rHuPH20) under defined conditions (e.g., protein concentration, pressure). This is often called a Vmax™ or filter capacity study.

        #### The Analysis
        We monitor the **flow rate** and **inlet pressure** as a function of the total **volumetric throughput** (total volume processed per unit of filter area, L/m²).
        - **Flow Rate vs. Throughput:** In a typical filtration, the flow rate remains stable initially and then begins to decay as the filter pores become blocked or "plugged" by the protein solution.
        - **Pressure vs. Throughput:** If the process is run at constant flow, the pressure will remain stable and then increase sharply as the filter plugs.
        - **Capacity Determination:** The filter's capacity is often defined as the throughput achieved just before a significant (e.g., 15% or 20%) drop in flow rate occurs, or before the pressure exceeds a defined limit. This ensures the process is run efficiently without risking filter integrity.
        """)
        
    fig_viral = go.Figure()
    # Add Flow Rate trace
    fig_viral.add_trace(go.Scatter(x=viral_df['Throughput (L/m²)'], y=viral_df['Flow Rate (L/hr)'], name='Flow Rate (L/hr)',
                             line=dict(color='#005EB8')))
    # Add Pressure trace on a secondary y-axis
    fig_viral.add_trace(go.Scatter(x=viral_df['Throughput (L/m²)'], y=viral_df['Pressure (psi)'], name='Pressure (psi)',
                             yaxis='y2', line=dict(color='#F36633')))
                             
    # Find the point where flow rate drops by 20%
    flow_initial = viral_df['Flow Rate (L/hr)'][0]
    flow_threshold = flow_initial * 0.8
    capacity_point = viral_df[viral_df['Flow Rate (L/hr)'] < flow_threshold].iloc[0]
    
    # --- FIX: Use double quotes for the f-string to allow single quotes inside ---
    fig_viral.add_vline(x=capacity_point['Throughput (L/m²)'], line_width=2, line_dash="dash", line_color="red",
                  annotation_text=f"Capacity Limit ({capacity_point['Throughput (L/m²)']:.0f} L/m²)", annotation_position="top left")
    # --- END OF FIX ---

    fig_viral.update_layout(
        title="Viral Filter Capacity Study: Flow & Pressure vs. Throughput",
        xaxis_title="Volumetric Throughput (L/m²)",
        yaxis=dict(title="<b>Flow Rate (L/hr)</b>", color='#005EB8'),
        yaxis2=dict(title="<b>Pressure (psi)</b>", color='#F36633', overlaying='y', side='right'),
        legend=dict(x=0.05, y=0.95),
    )
    st.plotly_chart(fig_viral, use_container_width=True)
    
    with st.expander("📊 **Results & MSAT Interpretation**"):
        st.markdown(f"""
        #### Analysis of the Filtration Profile
        - **Linear Phase (0 - ~500 L/m²):** The flow rate remains high and stable, and the pressure increases linearly and predictably. This indicates normal, unrestricted flow through the filter.
        - **Plugging Phase (> 500 L/m²):** The flow rate begins to decay at an accelerated rate, while the pressure begins to rise more sharply. This signifies that the filter pores are becoming constricted, a phenomenon known as filter plugging or fouling.
        - **Capacity Limit:** The analysis identifies the capacity limit at **{capacity_point['Throughput (L/m²)']:.0f} L/m²**, the point at which the flow rate has dropped by 20% from its initial value. Processing beyond this point is inefficient and risks breaching the filter's maximum pressure rating.

        #### Conclusion & Actionable Insights for MSAT
        This characterization study is fundamental to defining the viral filtration step for our CDMOs.
        1.  **Set Sizing for Manufacturing:** This data directly informs how we size the viral filter for a commercial-scale batch. For example, if a batch is 2000L, and we target a conservative capacity of 600 L/m², we would specify a filter size of at least $2000L / 600 L/m² = 3.33 m²$. We would select the next largest available filter size.
        2.  **Define Batch Record Parameters:** The target throughput (e.g., 600 L/m²) and the maximum pressure limit (e.g., 30 psi) are specified directly in the master batch record that is transferred to the CDMO.
        3.  **Regulatory Support:** This study is a key component of the viral clearance section of our BLA, providing the data to justify our scaled-down model and prove that our commercial process is robust and effective at viral removal.
        """)
