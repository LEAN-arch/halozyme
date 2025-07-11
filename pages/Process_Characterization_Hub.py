# pages/Process_Characterization_Hub.py

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import generate_chromatography_data, generate_ufdf_data
import numpy as np
import pandas as pd

st.set_page_config(
    page_title="Process Characterization | Halozyme",
    layout="wide"
)

st.title("🔬 Process Characterization Hub")
st.markdown("### Analysis of key performance data from downstream unit operation characterization studies.")

with st.expander("🌐 Regulatory Context: The Role of Process Characterization", expanded=True):
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
        st.markdown("""
        #### The Experiment
        This study characterizes a critical purification step, such as an Ion Exchange (IEX) or Affinity chromatography column. The goal is to demonstrate effective separation of the target protein (e.g., rHuPH20) from process- and product-related impurities under defined conditions. We compare a standard, successful run against a "worst-case" or failed run (simulating a process deviation) to highlight the importance of process control.

        #### The Analysis
        - **Chromatogram Overlay:** Visual comparison of the UV absorbance profiles over time. Key features are the main product peak and adjacent impurity peaks.
        - **Peak Integration (Simulated):** In a real analysis (e.g., using Chromeleon or Unicorn software), we would integrate the area under each peak to quantify yield and impurity levels.
        - **Resolution (Rₛ):** A quantitative measure of how well two peaks are separated. A higher resolution is better. The formula is:
        """)
        st.latex(r''' R_s = \frac{2(t_{R2} - t_{R1})}{w_1 + w_2} ''')
        st.markdown(r"""
        Where $t_R$ is the retention time and $w$ is the peak width at the base. A resolution > 1.5 is generally considered baseline separation.
        """)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Standard (Successful) Run")
        fig_normal = px.line(chrom_normal_df, x="Time (min)", y="UV (mAU)", title="Chromatogram: Standard Run")
        st.plotly_chart(fig_normal, use_container_width=True)
        st.success("**Analysis:** Excellent separation. Product peak is sharp and well-resolved from impurity peaks.")
        st.metric("Product / Impurity 2 Resolution (Rₛ)", "1.65")

    with col2:
        st.subheader("Worst-Case (Failed) Run")
        fig_fail = px.line(chrom_fail_df, x="Time (min)", y="UV (mAU)", title="Chromatogram: Worst-Case Run")
        st.plotly_chart(fig_fail, use_container_width=True)
        st.error("**Analysis:** Poor separation. Impurity peaks are significantly larger and co-elute with the main product peak.")
        st.metric("Product / Impurity 2 Resolution (Rₛ)", "0.85")

    with st.expander("📊 **Conclusion & Actionable Insights for Tech Transfer**"):
        st.markdown("""
        The comparison clearly demonstrates the necessity of the established process parameters for achieving the required product quality. The "worst-case" run, which might simulate a deviation in buffer pH or conductivity, results in unacceptable product purity due to poor resolution.

        **Action for MSAT:**
        1.  **Define Control Limits:** This data is used to set the Normal Operating Range (NOR) and Proven Acceptable Range (PAR) for the Critical Process Parameters (CPPs) of this step (e.g., buffer pH, conductivity, load density).
        2.  **Tech Transfer Document:** These chromatograms and the resolution data will be included in the Process Description and Tech Transfer Protocol provided to the CDMO. This provides the scientific "why" behind the numbers in the batch record.
        3.  **CDMO Training:** This serves as a powerful training tool to show CDMO operators *why* strict adherence to the batch record parameters is critical for product quality.
        4.  **Regulatory Support:** This characterization data forms the basis for the justification of our control strategy in regulatory filings.
        """)

with tab2:
    st.header("Ultrafiltration/Diafiltration (UF/DF) Performance")
    st.caption("Analyzing transmembrane pressure (TMP) and flux to monitor membrane performance and detect fouling.")

    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""
        #### The Experiment
        This study characterizes the UF/DF step, which is used for concentrating the product and exchanging it into the final formulation buffer. We monitor the key parameters of **Flux** (the rate of fluid flow through the membrane, in Liters per square Meter per Hour, or LMH) and **Transmembrane Pressure (TMP)** (the pressure driving the fluid across the membrane) as the product is concentrated.

        #### The Analysis
        - **Flux vs. Volume:** In a well-behaved process, flux should decline gently and predictably as the product becomes more concentrated and viscous. A sharp, non-linear drop in flux is indicative of membrane fouling or gel-layer formation.
        - **TMP vs. Volume:** If operating at a constant flux, TMP will typically rise to compensate for the increasing concentration. A sharp, uncontrolled rise in TMP is a clear sign of fouling and can damage the membrane, potentially compromising product quality.
        """)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['Flux (LMH)'], name='Flux (LMH)', line=dict(color='#005EB8')))
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['TMP (psi)'], name='TMP (psi)', yaxis='y2', line=dict(color='#F36633')))
    fig.add_vline(x=ufdf_df['Volume (L)'][20], line_width=2, line_dash="dash", line_color="red", annotation_text="Fouling Event", annotation_position="top left")
    fig.update_layout(title="UF/DF Performance: Flux and TMP vs. Process Volume", xaxis_title="In-Process Volume (L) - (Concentrating)", yaxis=dict(title="<b>Flux (LMH)</b>", color='#005EB8'), yaxis2=dict(title="<b>TMP (psi)</b>", color='#F36633', overlaying='y', side='right'), legend=dict(x=0.8, y=0.95), xaxis_autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 **Results & Analysis**"):
        st.markdown("""
        #### Analysis of the Run
        - **Normal Operation (20L to ~6L):** The process exhibits predictable behavior. Flux gently declines as TMP gradually increases to compensate for the rising protein concentration. This is the expected performance envelope for our rHuPH20 product.
        - **Fouling Event (<6L):** At approximately the 6L mark, there is a sharp, non-linear drop in flux, accompanied by a rapid spike in TMP. This is a classic signature of membrane fouling, where precipitated protein or other components block the membrane pores, impeding flow.

        #### Conclusion & Actionable Insights for MSAT
        This characterization study is critical for defining the operational limits of the UF/DF step.
        1.  **Define Process Limits:** The data helps set alert limits and action limits for the maximum allowable TMP and the minimum allowable flux rate. Any deviation beyond these limits during a manufacturing run at the CDMO would trigger a formal deviation investigation.
        2.  **Determine Process Capacity:** This study determines the maximum achievable concentration factor before significant fouling occurs, defining the limits of the process and ensuring we do not push the system beyond its capabilities.
        3.  **Troubleshooting Guide:** As the MSAT engineer, if a CDMO reports a similar deviation, this characterization data provides me with a strong hypothesis that they are experiencing a fouling event, allowing me to guide their investigation more effectively toward potential causes like incorrect buffer pH or temperature.
        """)

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
        - **Capacity Determination:** The filter's capacity is often defined as the throughput achieved just before a significant (e.g., 15-20%) drop in flow rate occurs, or before the pressure exceeds a defined limit (e.g., 30 psid). This ensures the process is run efficiently without risking filter integrity.
        """)
        
    fig_viral = go.Figure()
    fig_viral.add_trace(go.Scatter(x=viral_df['Throughput (L/m²)'], y=viral_df['Flow Rate (L/hr)'], name='Flow Rate (L/hr)', line=dict(color='#005EB8')))
    fig_viral.add_trace(go.Scatter(x=viral_df['Throughput (L/m²)'], y=viral_df['Pressure (psi)'], name='Pressure (psi)', yaxis='y2', line=dict(color='#F36633')))
                             
    flow_initial = viral_df['Flow Rate (L/hr)'][0]
    flow_threshold = flow_initial * 0.8
    capacity_point = viral_df[viral_df['Flow Rate (L/hr)'] < flow_threshold].iloc[0]
    
    fig_viral.add_vline(x=capacity_point['Throughput (L/m²)'], line_width=2, line_dash="dash", line_color="red",
                  annotation_text=f"Capacity Limit ({capacity_point['Throughput (L/m²)']:.0f} L/m²)", annotation_position="top left")

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
        - **Linear Phase (0 - ~500 L/m²):** The flow rate remains high and stable, and the pressure increases linearly and predictably. This indicates normal, unrestricted flow through the filter, where filter resistance is constant.
        - **Plugging Phase (> 500 L/m²):** The flow rate begins to decay at an accelerated rate, while the pressure begins to rise more sharply. This signifies that the filter pores are becoming constricted by deposited proteins, a phenomenon known as filter plugging or fouling.
        - **Capacity Limit:** The analysis identifies the capacity limit at **{capacity_point['Throughput (L/m²)']:.0f} L/m²**, the point at which the flow rate has dropped by 20% from its initial value. Processing beyond this point is inefficient and risks breaching the filter's maximum pressure rating, which could compromise its viral retention capability.

        #### Conclusion & Actionable Insights for MSAT
        This characterization study is fundamental to defining the viral filtration step for our CDMOs.
        1.  **Set Sizing for Manufacturing:** This data directly informs how we size the viral filter for a commercial-scale batch. For example, if a batch is 2000L, and we target a conservative operational capacity of 600 L/m² (providing a safety margin), we would specify a filter size of at least $2000L / 600 L/m² = 3.33 m²$. We would select the next largest available filter size from the supplier.
        2.  **Define Batch Record Parameters:** The target throughput (e.g., 600 L/m²) and the maximum pressure limit (e.g., 30 psi) are specified directly in the master batch record that is transferred to the CDMO. These are non-negotiable operational parameters.
        3.  **Regulatory Support:** This study is a key component of the viral clearance section of our BLA, providing the data to justify our scaled-down model and prove that our commercial process is robust and effective at viral removal.
        """)
