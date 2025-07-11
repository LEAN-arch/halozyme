# pages/Data_Analytics_Platform_Info.py

import streamlit as st

st.set_page_config(
    page_title="Analytics Platform | Halozyme",
    layout="wide"
)

st.image("https://www.halozyme.com/wp-content/uploads/2023/07/logo-halozyme-1.svg", width=250)
st.title("📊 Data Analytics & Visualization Platform")
st.markdown("### Information regarding the validated platform used for MSAT data analysis and Continued Process Verification (CPV).")

st.info("""
**Audience Note:** This page provides a summary of our GxP data analysis environment. As the Principal MSAT Engineer, I use this validated platform for all formal process data analysis, ensuring data integrity and compliance with regulatory expectations. The interactive dashboards in this Command Center are built upon the principles and validated calculations from this core platform.
""")

st.divider()

st.header("Platform Overview")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Platform Name")
    st.markdown("##### GxP Analytics Suite (Powered by JMP® & Custom Scripts)")
    st.subheader("Version")
    st.markdown("##### JMP Pro 17.2, Python Environment v2.1")
    st.subheader("Validation Status")
    st.success("#### ✔️ Validated for Intended Use")
with col2:
    st.subheader("Intended Use Statement")
    st.markdown("""
    This platform is validated for the statistical analysis, visualization, and monitoring of GxP manufacturing process data in support of:
    - Process Characterization (PC) Studies
    - Continued Process Verification (CPV) Program
    - Annual Product Quality Reviews (APQRs)
    - Deviation and Non-conformance Investigations
    - Authoring of Regulatory Submission Sections (e.g., BLA 3.2.P.2)
    """)

st.divider()

st.header("Scope of Validated Analyses")
st.markdown("The following sections detail the types of analyses within the validated scope of this platform, which are used extensively by the MSAT team to oversee our external manufacturing partners.")

# --- Statistical Process Control (SPC) ---
with st.expander("Expand: Statistical Process Control (SPC)"):
    st.subheader("Statistical Process Control (SPC)")
    st.markdown("**Purpose:** To monitor the performance of our commercial processes at CDMOs over time, ensuring they remain in a state of statistical control and detecting any unforeseen process drift or special cause variation.")

    st.markdown("---")
    st.markdown("#### I-MR Control Chart")
    
    col_exp, col_viz = st.columns([1.5, 1])
    with col_exp:
        st.markdown("**Experiment:** Monitoring a Critical Process Parameter (CPP), such as the pool conductivity from an Ion Exchange (IEX) chromatography step for 30 consecutive commercial batches of rHuPH20.")
        st.markdown("""
        **Methodology:** An Individuals and Moving Range (I-MR) chart is used. This is the appropriate chart for individual batch data where subgrouping is not logical.
        - The **Individuals (I) chart** plots each batch's result and detects shifts in the process mean.
        - The **Moving Range (MR) chart** plots the range between consecutive points and detects shifts in process variability.
        - Control limits are calculated at ±3 standard deviations (σ) from the mean.
        - **Nelson or Western Electric (WECO) rules** are applied to detect non-random patterns (e.g., 7 points in a row on one side of the mean) that indicate a process shift even if no single point is outside the control limits.
        """)
    with col_viz:
        st.image("https://www.spcforexcel.com/files/images/named/i-mr-chart-example.png", caption="Example of an I-MR chart used for batch monitoring.")

    st.markdown("""
    **Results & MSAT Interpretation:** The I-chart shows that all batches fall within the control limits, but the Nelson rules have flagged a trend of 8 consecutive points below the mean. The MR chart shows variability is stable. As the MSAT Engineer, this signals a subtle but real downward shift in the process mean for conductivity. This is not a deviation, but it requires proactive investigation with the CDMO to understand the cause (e.g., a change in buffer preparation, a drifting probe) before it leads to an out-of-spec event.
    """)

# --- Process Capability Analysis ---
with st.expander("Expand: Process Capability Analysis"):
    st.subheader("Process Capability Analysis")
    st.markdown("**Purpose:** To quantitatively assess whether our process, in a state of control, is capable of consistently producing material that meets its pre-defined specification limits.")
    st.markdown("---")
    st.markdown("#### Cpk & Ppk Analysis")
    
    col_exp, col_viz = st.columns([1.5, 1])
    with col_exp:
        st.markdown("**Experiment:** Assessing the capability of our final UF/DF step to achieve the target protein concentration for rHuPH20. The specification is 9.5 to 10.5 mg/mL.")
        st.markdown("""
        **Methodology:** We calculate the Process Capability Indices, Cpk and Ppk.
        - **Cpk (Process Capability Index):** Measures short-term potential capability based on the variation *within* rational subgroups. Formula: $C_{pk} = \min\left(\frac{USL - \mu}{3\sigma_{within}}, \frac{\mu - LSL}{3\sigma_{within}}\right)$
        - **Ppk (Process Performance Index):** Measures long-term actual performance based on the *overall* variation of all data. This is typically the primary index for CPV. Formula: $P_{pk} = \min\left(\frac{USL - \mu}{3\sigma_{overall}}, \frac{\mu - LSL}{3\sigma_{overall}}\right)$
        - A common industry target is a Cpk/Ppk value **≥ 1.33**.
        """)
    with col_viz:
        st.image("https://sixsigmastudyguide.com/wp-content/uploads/2020/10/Cp_Cpk.png", caption="Example of a process capability histogram.")

    st.markdown("""
    **Results & MSAT Interpretation:** Analysis of the last 50 batches yields a Ppk of **1.15**. The histogram shows the process is well-centered but the overall variability (the spread of the distribution) is too wide relative to the specification limits. A Ppk of 1.15 is considered "marginally capable" and indicates a higher-than-desirable risk of future OOS events. As the MSAT lead, I would initiate a project with the CDMO to identify and reduce sources of variability in the UF/DF step to improve our process robustness and increase the Ppk.
    """)

# --- Statistical Modeling & Comparison ---
with st.expander("Expand: Statistical Modeling & Comparison"):
    st.subheader("Statistical Modeling & Comparison")
    st.markdown("**Purpose:** To make statistically-sound comparisons between different groups (e.g., lots of raw material) or to model the relationship between process parameters and product quality attributes.")
    st.markdown("---")
    st.markdown("#### Analysis of Variance (ANOVA)")
    
    col_exp, col_viz = st.columns([1.5, 1])
    with col_exp:
        st.markdown("**Experiment:** Qualifying a new lot of Protein A chromatography resin from a supplier. We compare the new lot against the current qualified lot and a historical reference standard by running 10 purification cycles with each and measuring a CQA, such as host cell protein (HCP) clearance.")
        st.markdown("""
        **Methodology:** A **One-Way ANOVA** is used to determine if there is a statistically significant difference between the means of the three resin lots. The test produces a **P-value**.
        - **Null Hypothesis (H₀):** The mean HCP clearance is the same for all three lots.
        - **Acceptance Criterion:** If the P-value is > 0.05, we fail to reject the null hypothesis and conclude the lots are equivalent. If P-value < 0.05, there is a statistically significant difference, and the new lot fails qualification.
        """)
    with col_viz:
        st.image("https://www.jmp.com/en_us/statistics-knowledge-portal/t-test/two-sample-t-test/_jcr_content/par/styledcontainer_3/par/image.img.png/1598535492842.png", caption="Example of a box plot for comparing group means.")

    st.markdown("""
    **Results & MSAT Interpretation:** The ANOVA test yields a P-value of **0.48**. Since this is well above 0.05, we conclude there is no statistical evidence of a difference in performance between the new resin lot and the existing lots. The box plot visually confirms that the distributions are highly similar. As the MSAT Engineer, I will sign the report approving the new lot of resin for use in commercial manufacturing at our CDMO.
    """)
    st.markdown("---")
    st.markdown("#### Design of Experiments (DOE) / Response Surface Methodology (RSM)")
    st.markdown("""
    **Description:** For complex process optimization and characterization, we use the validated DOE capabilities of our platform. This allows us to efficiently model the effects of multiple parameters (e.g., pH, salt concentration, load density) and their interactions on critical outcomes (e.g., yield, purity). The primary output is a "sweet spot" plot or response surface model.
    
    *For a detailed, interactive example of this analysis, please see the **Process Optimization (DOE)** dashboard in this application.*
    """)

# --- Data Visualization ---
with st.expander("Expand: Core Data Visualization Tools"):
    st.subheader("Core Data Visualization Tools")
    st.markdown("""
    In addition to the specific analyses above, the following validated plot types are used extensively for data exploration, reporting, and troubleshooting.
    - **Box Plots:** Used to visualize and compare the distribution (median, quartiles, spread, outliers) of a dataset across different categories (e.g., comparing batch yields across different CDMO sites).
    - **Scatter Plots:** Used to investigate the relationship between two continuous variables (e.g., plotting chromatography load density vs. product yield to identify a correlation).
    - **Time-Series Plots:** Used to visualize any parameter over time or batch number to identify trends, shifts, or cycles. The I-chart is a specialized form of a time-series plot.
    - **Pareto Charts:** A specialized bar chart used to identify the "vital few" causes contributing to the majority of problems (the 80/20 rule), such as identifying the most frequent root causes for manufacturing deviations.
    """)

st.divider()
st.info("""
For the full validation package, protocols, and reports for the GxP Analytics Suite, please refer to the Halozyme Quality Management System, Document #**VAL-SYS-101**.
""")
