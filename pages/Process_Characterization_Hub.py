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

# --- Data Generation ---
# These functions now simulate downstream process data
chrom_normal_df = generate_chromatography_data(high_impurity=False)
chrom_fail_df = generate_chromatography_data(high_impurity=True)
ufdf_df = generate_ufdf_data()

# --- Page Tabs for Downstream Unit Operations ---
tab1, tab2, tab3 = st.tabs([
    "**Chromatography Performance**",
    "**Ultrafiltration/Diafiltration (UF/DF)**",
    "**Viral Filtration (Placeholder)**"
])

with tab1:
    st.header("Chromatography Step Characterization")
    st.caption("Analysis of elution profiles to assess yield, purity, and impurity clearance.")

    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""
        #### The Experiment
        This study characterizes a critical purification step, such as an Ion Exchange (IEX) or Affinity chromatography column. The goal is to demonstrate effective separation of the target protein (e.g., rHuPH20) from process- and product-related impurities under defined conditions. We compare a standard, successful run against a "worst-case" or failed run to highlight the importance of process control.

        #### The Analysis
        - **Chromatogram Overlay:** Visual comparison of the UV absorbance profiles over time. Key features are the main product peak and adjacent impurity peaks.
        - **Peak Integration (Simulated):** In a real analysis (e.g., using Chromeleon or Unicorn software), we would integrate the area under each peak to quantify yield and impurity levels. Here, we simulate this analysis to provide key metrics.
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
        The comparison clearly demonstrates the necessity of the established process parameters. The "worst-case" run, which might simulate a deviation in buffer pH or conductivity, results in unacceptable product purity due to poor resolution.

        **Action for MSAT:**
        1.  **Define Control Limits:** This data is used to set the Normal Operating Range (NOR) and Proven Acceptable Range (PAR) for the CPPs of this step (e.g., buffer pH, conductivity, load density).
        2.  **Tech Transfer Document:** These chromatograms and the resolution data will be included in the Process Description and Tech Transfer Protocol provided to the CDMO.
        3.  **CDMO Training:** This serves as a powerful training tool to show CDMO operators *why* adherence to the batch record parameters is critical for product quality.
        """)

with tab2:
    st.header("Ultrafiltration/Diafiltration (UF/DF) Performance")
    st.caption("Analyzing transmembrane pressure (TMP) and flux to monitor membrane performance and detect fouling.")

    with st.expander("🔬 **Experiment & Method**"):
        st.markdown("""
        #### The Experiment
        This study characterizes the UF/DF step, which is used for concentrating the product and buffer exchange. We monitor the key parameters of **Flux** (the rate of fluid flow through the membrane, in Liters per square Meter per Hour, or LMH) and **Transmembrane Pressure (TMP)** (the pressure driving the fluid across the membrane) as the product is concentrated.

        #### The Analysis
        - **Flux vs. Volume:** In a well-behaved process, flux should decline gently and predictably as the product becomes more concentrated (viscous). A sharp drop in flux is indicative of membrane fouling.
        - **TMP vs. Volume:** TMP will typically rise to compensate for the increasing concentration and maintain the target flux rate. A sharp, uncontrolled rise in TMP is a clear sign of fouling and can damage the membrane.
        """)

    fig = go.Figure()
    # Add Flux trace
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['Flux (LMH)'], name='Flux (LMH)',
                             line=dict(color='#005EB8')))
    # Add TMP trace on a secondary y-axis
    fig.add_trace(go.Scatter(x=ufdf_df['Volume (L)'], y=ufdf_df['TMP (psi)'], name='TMP (psi)',
                             yaxis='y2', line=dict(color='#F36633')))
    # Add a marker for the fouling event
    fig.add_vline(x=ufdf_df['Volume (L)'][20], line_width=2, line_dash="dash", line_color="red",
                  annotation_text="Fouling Event", annotation_position="top left")

    fig.update_layout(
        title="UF/DF Performance: Flux and TMP vs. Process Volume",
        xaxis_title="In-Process Volume (L) - (Concentrating)",
        yaxis=dict(title="<b>Flux (LMH)</b>", color='#005EB8'),
        yaxis2=dict(title="<b>TMP (psi)</b>", color='#F36633', overlaying='y', side='right'),
        legend=dict(x=0.8, y=0.95),
        xaxis_autorange="reversed" # Show volume decreasing
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("📊 **Results & Analysis**"):
        st.markdown("""
        #### Analysis of the Run
        - **Normal Operation (20L to ~6L):** The process exhibits predictable behavior. Flux gently declines as TMP gradually increases to compensate for the rising protein concentration. This is the expected performance envelope.
        - **Fouling Event (<6L):** At approximately the 6L mark, there is a sharp, non-linear drop in flux, accompanied by a rapid spike in TMP. This is a classic signature of membrane fouling, where precipitated protein or other components block the membrane pores.

        #### Conclusion & Actionable Insights for MSAT
        This characterization study is critical for defining the operational limits of the UF/DF step.

        1.  **Define Process Limits:** The data helps set alert limits and action limits for the maximum allowable TMP and the minimum allowable flux rate. Any deviation beyond these limits during a manufacturing run at the CDMO would trigger a formal deviation.
        2.  **Determine Process Capacity:** This study determines the maximum achievable concentration factor before significant fouling occurs, defining the limits of the process.
        3.  **Troubleshooting Guide:** As the MSAT engineer, if a CDMO reports a similar deviation, this characterization data provides me with a strong hypothesis that they are experiencing a fouling event, allowing me to guide their investigation more effectively.
        """)

with tab3:
    st.header("Viral Filtration Characterization")
    st.info("🚧 This section is under construction. It will contain analysis of viral filtration studies, including Vmax™ curves, decay modeling, and determination of filter capacity (L/m²).")
    st.image("https://www.sartorius.com/media/global/products/virus-clearance-viresolve-pro-solution-with-shield-2-slider-1600x900-5.jpg")
