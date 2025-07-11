# pages/Deviation_Change_Control_Hub.py

import streamlit as st
import pandas as pd
from datetime import date, timedelta
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from utils import generate_deviation_data, generate_change_control_data, generate_pareto_data

st.set_page_config(
    page_title="Deviations & CC | Halozyme",
    layout="wide"
)

st.title("📋 Deviation & Change Control Hub")
st.markdown("### MSAT oversight of non-conformances and change controls originating from our external manufacturing partners.")

with st.expander("🌐 MSAT Role in the Quality System"):
    st.markdown("""
    As the MSAT subject matter authority for our external manufacturing, I play a critical role in Halozyme's Quality Management System (QMS). My responsibility is not to run the CDMO's QMS, but to provide timely and robust technical oversight.

    - **Deviation & Non-conformance Management (Per 21 CFR 211.192):** When a deviation from the batch record occurs at a CDMO, I lead the technical assessment to determine the potential impact on product quality. I review and approve the CDMO's investigation, root cause analysis, and proposed corrective actions.
    - **Change Control Management (Per ICH Q10, 3.2.4):** I am the technical lead for evaluating any proposed changes to our validated manufacturing processes at a CDMO. This includes assessing the change's impact on the process, product quality, and its regulatory reportability (e.g., as a CBE-30 or PAS).
    - **CAPA Feeder:** Significant or recurring deviations managed here are the primary input into our formal Corrective and Preventive Action (CAPA) system, driving systemic improvements across our network.
    """)

# --- Data Generation ---
deviation_df = generate_deviation_data()
change_control_df = generate_change_control_data()
pareto_df = generate_pareto_data()

# --- 1. KPIs ---
st.header("1. Quality System Event KPIs (CDMO Network)")
total_open_devs = len(deviation_df)
overdue_devs = deviation_df[deviation_df['Age (Days)'] > 30].shape[0] # Deviations should be closed within 30 days
open_changes = len(change_control_df)

col1, col2, col3 = st.columns(3)
col1.metric("Open Deviations", f"{total_open_devs}")
col2.metric("Deviations Overdue (>30d)", f"{overdue_devs}", delta=f"{overdue_devs} Overdue", delta_color="inverse")
col3.metric("Active Change Controls", f"{open_changes}")

st.divider()

# --- 2. Deviation Management ---
st.header("2. Active Deviation Tracker")
st.caption("Real-time status of open non-conformance investigations at our CDMO partners.")
st.dataframe(deviation_df, use_container_width=True, hide_index=True)

st.divider()

# --- 3. Root Cause Analysis & Change Control ---
col1, col2 = st.columns(2)

with col1:
    st.header("3. Deviation Root Cause Pareto")
    st.caption("Analyzing historical root causes to identify systemic issues and guide preventive actions.")

    pareto_df['Cumulative %'] = (pareto_df['Count'].cumsum() / pareto_df['Count'].sum()) * 100
    fig_pareto = make_subplots(specs=[[{"secondary_y": True}]])
    fig_pareto.add_trace(go.Bar(x=pareto_df['Root Cause Category'], y=pareto_df['Count'], name='Deviation Count'), secondary_y=False)
    fig_pareto.add_trace(go.Scatter(x=pareto_df['Root Cause Category'], y=pareto_df['Cumulative %'], name='Cumulative %', line=dict(color='red')), secondary_y=True)
    fig_pareto.update_layout(title_text="Pareto Chart of Deviation Root Causes", height=500)
    fig_pareto.update_yaxes(title_text="<b>Count</b>", secondary_y=False)
    fig_pareto.update_yaxes(title_text="<b>Cumulative Percentage (%)</b>", secondary_y=True, range=[0, 101])
    st.plotly_chart(fig_pareto, use_container_width=True)

with col2:
    st.header("4. Active Change Control Log")
    st.caption("Tracking proposed changes to validated processes, materials, or equipment.")
    st.dataframe(change_control_df, use_container_width=True, hide_index=True, height=530)


with st.expander("🔬 **My Role as MSAT Engineer: From Data to Action**"):
    st.markdown("""
    This dashboard provides the data I need to fulfill my oversight responsibilities effectively.

    #### Analysis of Current Events:
    - **Active Deviations:** The tracker shows `DEV-24-051` is an out-of-spec conductivity result. This is a critical parameter that can impact protein binding and impurity clearance. I need to ensure the CDMO's investigation is scientifically sound and that their root cause analysis is thorough.
    - **Pareto Chart:** The historical data is clear: **Buffer Preparation Error** is our number one cause of deviations across the network. This isn't an isolated issue; it's a systemic vulnerability.
    - **Change Controls:** The proposed change to a new UF/DF skid (`CC-24-012`) is a major undertaking. As the MSAT lead, I must draft the technical assessment for this change, outlining the validation and comparability studies required to prove the new equipment yields an equivalent product. I will also work with Regulatory Affairs to confirm its reportability as a CBE-30.

    #### Strategic Actions:
    1.  **Systemic Improvement:** Based on the Pareto chart, I will propose and lead a cross-functional "One Team" initiative with our CDMO partners to standardize and improve buffer preparation processes. This could involve enhanced training, automation, or in-line concentration checks. This is a classic **Preventive Action** designed to reduce the recurrence of our most common failure mode.
    2.  **Technical Leadership:** For the active deviation, I will review the CDMO's data, challenge their assumptions, and ensure their proposed corrective actions are robust. For the change control, I will define the scope of work and technical requirements, ensuring Halozyme's interests and quality standards are maintained.
    """)
