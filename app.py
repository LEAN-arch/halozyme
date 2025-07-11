# app.py
import streamlit as st
import pandas as pd
import plotly.express as px
from utils import generate_campaign_portfolio_data, generate_manufacturing_risk_data
from datetime import date

# --- Page Configuration ---
st.set_page_config(
    page_title="MSAT Command Center | Halozyme",
    page_icon="🏭",
    layout="wide"
)

# --- Data Loading ---
# These utils functions are now overhauled to generate data for external manufacturing oversight
portfolio_df = generate_campaign_portfolio_data()
risks_df = generate_manufacturing_risk_data()

# --- Page Title and Header ---
st.image("https://www.halozyme.com/wp-content/uploads/2023/07/logo-halozyme-1.svg", width=250)
st.title("MSAT Command Center for External Manufacturing")
st.markdown("### Strategic oversight of Halozyme's global CDMO network, technology transfers, and manufacturing campaigns for biologic drug substances.")

# --- KPIs: Health of the External Manufacturing Network ---
st.header("CDMO Network Health: Key Performance Indicators")

# Calculate KPIs
total_campaigns = len(portfolio_df)
active_campaigns = portfolio_df[portfolio_df['Status'].isin(['In Progress', 'At Risk'])].shape[0]
batch_success_rate = portfolio_df['Batch Success Rate (%)'].mean()
open_critical_deviations = portfolio_df['Open Critical Deviations'].sum()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Active Campaigns & Tech Transfers", f"{active_campaigns}")
col2.metric("Network Batch Success Rate (YTD)", f"{batch_success_rate:.1f}%")
col3.metric("Open Critical Deviations", f"{open_critical_deviations}", delta=f"{open_critical_deviations} Active", delta_color="inverse")
col4.metric("CDMOs Under Active Mgmt", f"{portfolio_df['CDMO Site'].nunique()}")

st.divider()

# --- Main Content Area ---
col1, col2 = st.columns((2, 1.2))

with col1:
    st.header("Manufacturing Campaign & Tech Transfer Portfolio")
    st.caption("Timelines for all major activities across our external manufacturing network.")
    fig = px.timeline(
        portfolio_df,
        x_start="Start Date",
        x_end="End Date",
        y="Campaign / Transfer",
        color="CDMO Site",
        title="Active Campaigns by CDMO Site & Phase",
        hover_name="Campaign / Transfer",
        hover_data={
            "Lead Engineer": True,
            "Phase": True,
            "Status": True,
            "Start Date": "|%B %d, %Y",
            "End Date": "|%B %d, %Y",
        }
    )
    fig.update_yaxes(categoryorder="total ascending", title=None)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Manufacturing Risk Matrix (ICH Q9)")
    st.caption("Prioritizing risks to product quality, supply continuity, and regulatory compliance.")
    fig_risk = px.scatter(
        risks_df, x="Probability", y="Impact", size="Risk Score", color="Risk Score",
        color_continuous_scale=px.colors.sequential.OrRd, hover_name="Risk Description",
        hover_data=["CDMO Site", "Owner", "Mitigation Status"], size_max=40, title="Impact vs. Probability of Manufacturing Risks"
    )
    fig_risk.update_layout(
        xaxis=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['Remote', 'Unlikely', 'Possible', 'Likely', 'Almost Certain'], title='Probability of Occurrence'),
        yaxis=dict(tickvals=[1, 2, 3, 4, 5], ticktext=['Negligible', 'Minor', 'Moderate', 'Major', 'Catastrophic'], title='Impact on Supply / Quality'),
        coloraxis_showscale=False
    )
    fig_risk.add_shape(type="rect", xref="x", yref="y", x0=3.5, y0=3.5, x1=5.5, y1=5.5, fillcolor="rgba(214, 39, 40, 0.2)", layer="below", line_width=0)
    fig_risk.add_annotation(x=4.5, y=4.5, text="High Risk Zone", showarrow=False, font=dict(color="#d62728", size=14, family="Arial, bold"))
    st.plotly_chart(fig_risk, use_container_width=True)

st.header("CDMO Portfolio Details")
st.dataframe(
    portfolio_df[['Campaign / Transfer', 'CDMO Site', 'Phase', 'Status', 'Lead Engineer', 'Batch Success Rate (%)', 'Open Critical Deviations']],
    use_container_width=True,
    hide_index=True
)

# --- REGULATORY CONTEXT & DASHBOARD PURPOSE ---
st.divider()
with st.expander("🌐 Purpose, Scope, and Regulatory Context for MSAT"):
    st.markdown("""
    As the MSAT authority for Halozyme's downstream drug substance manufacturing, this Command Center is my primary tool for ensuring the consistency, robustness, and compliance of our externally manufactured products. It provides a single source of truth for data-driven oversight and decision-making, in line with our "One Team" culture of collaboration.

    #### **How This Dashboard Supports My Role and Halozyme's Mission:**

    - **External Manufacturing Oversight (Per ICH Q10):**
        - This dashboard provides the data necessary for effective management of our CDMO partners, including performance metrics for Quarterly Business Reviews (QBRs) and a clear view of all ongoing manufacturing campaigns. The **CDMO Oversight Dashboard** provides deeper analytics on site-specific performance.

    - **Technology Transfer (Per ICH Q10, 2.7):**
        - The **Portfolio Gantt Chart** tracks the progress of all technology transfer activities, ensuring a structured and efficient transfer of process knowledge to our CDMO partners. The **Technology Transfer Dashboard** provides a granular, checklist-driven view of each transfer project.

    - **Process Validation (PV) & Continued Process Verification (CPV):**
        - This tool allows for the tracking of PV campaign execution at our CDMOs.
        - For our commercial products like rHuPH20, it serves as the entry point to the **Continued Process Verification (CPV) Dashboard**, which monitors Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) to ensure our processes remain in a state of control.

    - **Quality Risk Management (Per ICH Q9):**
        - The **Risk Matrix** is a direct implementation of ICH Q9 principles. It is our central tool for identifying, evaluating, and mitigating risks related to manufacturing processes, supply chain, and compliance at our CDMOs.

    - **Deviation & Change Control Management (Per 21 CFR 211):**
        - The KPIs for critical deviations provide an immediate signal of potential quality issues. This dashboard links directly to the **Deviation & Change Control Hub**, where I perform technical assessments of events originating from our CDMOs, ensuring timely investigation and robust corrective actions.

    - **CMC & Regulatory Submission Support:**
        - This Command Center provides a consolidated, data-rich environment that is essential for authoring and reviewing CMC sections of our regulatory submissions (e.g., BLAs, CBE-30s, PAS). It is my primary resource when responding to Health Authority Requests for Information (RFIs) regarding our manufacturing processes.
    """)
