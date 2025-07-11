# pages/Data_Analytics_Platform_Info.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

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

# --- Original Content: Preserved and Integrated ---
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

st.header("Key Compliance & Data Integrity Features")
st.subheader("Compliance with 21 CFR Part 11")
st.markdown("The platform and its supporting procedures are designed to comply with the requirements for electronic records and electronic signatures.")
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""
    **✔️ Secure, Auditable Data Source**
    - Data is pulled directly from the validated corporate data historian (e.g., PI) or LIMS, preventing manual data entry errors.
    - All raw data is read-only.
    """)
with c2:
    st.markdown("""
    **✔️ Validated Calculations & Scripts**
    - All statistical scripts (e.g., for control charting, Cpk) are formally validated.
    - The use of commercial, widely-accepted software (JMP®) for core statistical functions provides additional assurance.
    """)
with c3:
    st.markdown("""
    **✔️ Access Control & Audit Trails**
    - Access to the platform is controlled by unique user credentials.
    - While this Streamlit dashboard is for visualization, the source platform (JMP) generates auditable logs for all analyses and reports.
    """)

st.divider()

# --- NEW: Expanded and Visualized Scope of Analyses ---
st.header("Scope of Validated Analyses")
st.markdown("The following sections detail the types of analyses within the validated scope of this platform, with examples relevant to MSAT oversight of external manufacturing.")

# --- Statistical Process Control (SPC) ---
with st.expander("**1. Statistical Process Control (SPC)**", expanded=True):
    st.markdown("**Purpose:** To monitor the performance of our commercial processes at CDMOs over time, ensuring they remain in a state of statistical control and detecting any unforeseen process drift or special cause variation.")
    st.markdown("---")
    
    st.markdown("#### I-MR Control Chart Example")
    col_exp, col_viz = st.columns([1, 1.2])
    with col_exp:
        st.markdown("**Experiment:** Monitoring a Critical Process Parameter (CPP), such as the pool conductivity from an Ion Exchange (IEX) chromatography step for 30 consecutive commercial batches of rHuPH20.")
        st.markdown("""
        **Methodology:** An Individuals and Moving Range (I-MR) chart is used for individual batch data.
        - The **Individuals (I) chart** plots each batch's result to detect shifts in the process mean.
        - The **Moving Range (MR) chart** plots the range between consecutive points to detect shifts in process variability.
        - Control limits are calculated at **±3 standard deviations (σ)** from the mean. Nelson rules are applied to detect non-random patterns.
        """)
    with col_viz:
        # Generate data for the plot
        np.random.seed(42)
        i_data = np.random.normal(15.2, 0.2, 30)
        i_data[20:] -= 0.3 # Introduce a shift
        i_df = pd.DataFrame({'value': i_data, 'batch': range(1, 31)})
        i_df['mr'] = i_df['value'].diff().abs()

        i_mean, mr_mean = i_df['value'].mean(), i_df['mr'].mean()
        i_ucl, i_lcl = i_mean + 3 * i_df['value'].std(), i_mean - 3 * i_df['value'].std()
        mr_ucl = mr_mean + 3 * i_df['mr'].std()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=i_df['batch'], y=i_df['value'], mode='lines+markers', name='Conductivity (mS/cm)'))
        fig.add_hline(y=i_mean, line_dash="dash", line_color="green")
        fig.add_hline(y=i_ucl, line_dash="dash", line_color="red")
        fig.add_hline(y=i_lcl, line_dash="dash", line_color="red")
        fig.add_annotation(x=25, y=i_mean - 0.4, text="Rule Violation: 8 points below mean", showarrow=True, arrowhead=1)
        fig.update_layout(title="Individuals (I) Chart for IEX Conductivity", height=300, margin=dict(t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Results & MSAT Interpretation:** The I-chart shows that all batches fall within the control limits, but a Nelson rule has flagged a run of 8 consecutive points below the mean. This signals a subtle but real downward shift in the process. As the MSAT Engineer, this is a proactive signal to investigate the cause with the CDMO (e.g., a drifting probe, a change in buffer preparation) before it results in a deviation.
    """)

# --- Process Capability Analysis ---
with st.expander("**2. Process Capability Analysis**"):
    st.markdown("**Purpose:** To quantitatively assess whether our process, in a state of control, is capable of consistently producing material that meets its pre-defined specification limits.")
    st.markdown("---")
    
    st.markdown("#### Cpk & Ppk Analysis Example")
    col_exp, col_viz = st.columns([1, 1.2])
    with col_exp:
        st.markdown("**Experiment:** Assessing the capability of our final UF/DF step to achieve the target protein concentration for rHuPH20. The specification is 9.5 to 10.5 mg/mL.")
        st.markdown("""
        **Methodology:** We calculate the Process Performance Index (Ppk), which measures long-term actual performance based on the *overall* variation of all data.
        - **Formula:** $P_{pk} = \min\left(\frac{USL - \mu}{3\sigma_{overall}}, \frac{\mu - LSL}{3\sigma_{overall}}\right)$
        - A common industry target is a **Ppk value ≥ 1.33**.
        """)
    with col_viz:
        np.random.seed(10)
        cap_data = np.random.normal(10.1, 0.25, 100)
        lsl, usl = 9.5, 10.5
        fig = px.histogram(x=cap_data, nbins=20, histnorm='probability density')
        fig.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
        fig.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
        fig.update_layout(title="Process Capability Histogram for Protein Conc.", height=300, margin=dict(t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Results & MSAT Interpretation:** Analysis of the last 100 batches yields a Ppk of **0.89**. The histogram shows the process is centered far too close to the upper specification limit (USL), and the process spread is wide. A Ppk of 0.89 is **not capable**. As the MSAT lead, this data provides the justification to launch a process improvement project with the CDMO to re-center the process mean and reduce overall variability.
    """)

# --- Statistical Modeling & Comparison ---
with st.expander("**3. Statistical Modeling & Comparison**"):
    st.markdown("**Purpose:** To make statistically-sound comparisons between different groups or to model the relationship between process parameters and product quality attributes.")
    st.markdown("---")
    
    st.markdown("#### ANOVA Example")
    col_exp, col_viz = st.columns([1, 1.2])
    with col_exp:
        st.markdown("**Experiment:** Qualifying a new lot of Protein A chromatography resin. We compare the new lot against the current qualified lot by measuring a CQA, such as host cell protein (HCP) clearance (LRV).")
        st.markdown("""
        **Methodology:** A **One-Way ANOVA** is used to determine if there is a statistically significant difference between the means of the resin lots. The test produces a **P-value**.
        - **Null Hypothesis (H₀):** The mean HCP clearance is the same for both lots.
        - **Acceptance Criterion:** If the P-value is **> 0.05**, we conclude the lots are equivalent.
        """)
    with col_viz:
        np.random.seed(1)
        anova_df = pd.DataFrame({
            'LRV': np.concatenate([np.random.normal(3.1, 0.1, 10), np.random.normal(3.12, 0.1, 10)]),
            'Lot': ['Current Lot'] * 10 + ['New Lot'] * 10
        })
        fig = px.box(anova_df, x='Lot', y='LRV', color='Lot')
        fig.update_layout(title="ANOVA Comparison of Resin Lot Performance", height=300, margin=dict(t=30, b=0))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Results & MSAT Interpretation:** The ANOVA test yields a P-value of **0.75**. Since this is well above 0.05, we conclude there is no statistical evidence of a difference in performance. As the MSAT Engineer, I will sign the report approving the new lot of resin for use in manufacturing.
    """)
    
# --- Data Visualization ---
with st.expander("**4. Core Data Visualization Tools**"):
    st.markdown("**Purpose:** To use a validated suite of plots for data exploration, reporting, and troubleshooting during investigations.")
    st.markdown("---")
    st.markdown("#### Pareto Chart Example")
    col_exp, col_viz = st.columns([1, 1.2])
    with col_exp:
        st.markdown("**Experiment:** Analyzing the root causes of all deviations that occurred across the CDMO network in the past year to identify systemic issues.")
        st.markdown("""
        **Methodology:** A **Pareto Chart** is a specialized bar chart that adheres to the **80/20 rule**, identifying the "vital few" causes that contribute to the majority of problems. It plots the counts of each category and the cumulative percentage line.
        """)
    with col_viz:
        pareto_df = pd.DataFrame({
            'Category': ['Buffer Error', 'Operator Error', 'Column Issue', 'Equipment', 'Material'],
            'Count': [15, 8, 4, 2, 1]
        })
        pareto_df['Cumulative %'] = (pareto_df['Count'].cumsum() / pareto_df['Count'].sum()) * 100
        fig = go.Figure()
        fig.add_trace(go.Bar(x=pareto_df['Category'], y=pareto_df['Count'], name='Count'))
        fig.add_trace(go.Scatter(x=pareto_df['Category'], y=pareto_df['Cumulative %'], yaxis='y2', name='Cumulative %', line=dict(color='red')))
        fig.update_layout(title="Pareto Analysis of Deviation Root Causes", height=300, margin=dict(t=30, b=0),
                          yaxis2=dict(title='Cumulative %', overlaying='y', side='right', range=[0, 101]))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Results & MSAT Interpretation:** The Pareto chart clearly shows that "Buffer Error" and "Operator Error" account for nearly 80% of all deviations. This is a powerful, data-driven insight. This justifies launching a high-priority, network-wide CAPA focused on improving buffer preparation procedures and operator training at our CDMO partners.
    """)

st.divider()
st.info("""
For the full validation package, protocols, and reports for the GxP Analytics Suite, please refer to the Halozyme Quality Management System, Document #**VAL-SYS-101**.
""")
