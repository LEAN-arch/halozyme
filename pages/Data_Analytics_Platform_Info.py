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

st.header("Key Compliance & Data Integrity Features")

st.subheader("Compliance with 21 CFR Part 11")
st.markdown("""
The platform and its supporting procedures are designed to comply with the requirements for electronic records and electronic signatures.
""")

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
st.header("Scope of Validated Analyses")

st.markdown("""
The following types of analyses are within the validated scope of this platform and are used extensively by the MSAT team to oversee our external manufacturing partners.
""")

st.markdown("""
- **Statistical Process Control (SPC):**
  - I-MR, Xbar-R, and Xbar-S control charts for monitoring CPPs and CQAs.
  - Implementation of Western Electric (WECO) or Nelson rules for trend analysis.

- **Process Capability Analysis:**
  - Calculation of Cp, Cpk, Pp, and Ppk for normal and non-normal data.
  - Generation of process capability histograms.

- **Statistical Modeling & Comparison:**
  - Analysis of Variance (ANOVA) and t-tests for lot-to-lot comparisons and process change assessments.
  - Design of Experiments (DOE) analysis, including Response Surface Methodology (RSM) for process optimization and characterization.

- **Data Visualization:**
  - Box plots, scatter plots, time-series plots, and Pareto charts.
""")

st.info("""
For questions regarding the validation package or specific procedures for using this platform, please refer to the Halozyme Quality Management System, Document #`VAL-SYS-101`.
""")
