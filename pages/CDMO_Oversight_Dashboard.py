# pages/CDMO_Oversight_Dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="CDMO Oversight | Halozyme",
    layout="wide"
)

st.title("📈 CDMO Performance & Oversight Dashboard")
st.markdown("### Monitoring the operational performance, quality metrics, and supply chain readiness of our external manufacturing partners.")

with st.expander("🌐 MSAT Role in Managing Outsourced Activities"):
    st.markdown("""
    As the MSAT lead, I am accountable for the technical oversight of all manufacturing activities at our Contract Development and Manufacturing Organizations (CDMOs). This dashboard is my central tool for data-driven management of these critical partnerships, in line with ICH Q10 guidelines.

    - **Performance Monitoring:** I use this data to monitor key performance indicators (KPIs) for each CDMO, which serves as the basis for technical discussions during Quarterly Business Reviews (QBRs).
    - **Quality & Compliance:** Tracking batch success rates and deviation trends provides a real-time view of a CDMO's quality culture and their ability to operate our process in a state of control.
    - **Supply Chain Assurance:** Proactively monitoring the inventory of critical, long-lead-time raw materials at our CDMOs is essential for preventing production delays and ensuring continuity of supply.
    - **Risk Management:** The data presented here serves as a direct input into our Quality Risk Management program, helping us to identify and mitigate risks associated with our external manufacturing network.
    """)

# --- Mock Data Generation ---
def generate_cdmo_performance_data():
    data = {
        'CDMO Site': ['CDMO Alpha', 'CDMO Beta', 'CDMO Gamma', 'CDMO Alpha', 'CDMO Beta', 'CDMO Gamma', 'CDMO Alpha'],
        'Quarter': ['2023 Q4', '2023 Q4', '2023 Q4', '2024 Q1', '2024 Q1', '2024 Q1', '2024 Q2'],
        'Batches Planned': [20, 5, 3, 22, 6, 4, 18],
        'Batches Successful': [20, 5, 3, 21, 6, 3, 18],
        'Total Deviations': [5, 2, 4, 6, 3, 5, 4],
        'Critical Deviations': [0, 0, 1, 1, 0, 1, 0]
    }
    df = pd.DataFrame(data)
    df['Batch Success Rate (%)'] = (df['Batches Successful'] / df['Batches Planned']) * 100
    return df

def generate_material_inventory_data():
    data = {
        'CDMO Site': ['CDMO Alpha', 'CDMO Alpha', 'CDMO Beta', 'CDMO Gamma'],
        'Material': ['Protein A Resin', 'Viral Filter', 'IEX-2 Resin', 'Viral Filter'],
        'Lot Number': ['A-PR-2301', 'VF-SART-055', 'B-IEX-004', 'VF-PALL-098'],
        'Quantity (Batches Remaining)': [5, 12, 3, 2],
        'Status': ['Sufficient', 'Sufficient', 'Re-order Point', 'Below Safety Stock']
    }
    return pd.DataFrame(data)

cdmo_df = generate_cdmo_performance_data()
inventory_df = generate_material_inventory_data()

# --- KPIs ---
st.header("1. CDMO Network: Key Performance Metrics (YTD 2024)")
ytd_df = cdmo_df[cdmo_df['Quarter'].str.contains('2024')]
ytd_success_rate = (ytd_df['Batches Successful'].sum() / ytd_df['Batches Planned'].sum()) * 100
ytd_crit_devs = ytd_df['Critical Deviations'].sum()

kpi1, kpi2, kpi3 = st.columns(3)
kpi1.metric("Network Batch Success Rate (YTD)", f"{ytd_success_rate:.1f}%")
kpi2.metric("Total Critical Deviations (YTD)", ytd_crit_devs, delta=f"{ytd_crit_devs} events", delta_color="inverse")
kpi3.metric("Sites Below Safety Stock", "1", help="Number of sites with at least one critical material below safety stock level.")

st.divider()

# --- 2. Performance Trending ---
st.header("2. Quarterly Performance by CDMO Site")
col1, col2 = st.columns(2)
with col1:
    st.subheader("Batch Success Rate (%)")
    fig_bsr = px.line(
        cdmo_df, x="Quarter", y="Batch Success Rate (%)", color="CDMO Site",
        title="Batch Success Rate Trend by Site", markers=True,
        range_y=[70, 105]
    )
    fig_bsr.add_hline(y=95, line_dash="dash", line_color="red", annotation_text="Target")
    st.plotly_chart(fig_bsr, use_container_width=True)
with col2:
    st.subheader("Deviation Trends")
    fig_dev = px.bar(
        cdmo_df, x="Quarter", y="Total Deviations", color="CDMO Site",
        barmode='group', title="Total Deviations per Quarter by Site"
    )
    st.plotly_chart(fig_dev, use_container_width=True)

with st.expander("🔬 **MSAT Analysis & Actions**"):
    st.markdown("""
    These trends provide a high-level view of the operational health of each partner.
    - **CDMO Gamma Performance:** This site is a clear concern. Their batch success rate dropped significantly in Q1 and Q2 2024, corresponding with a sustained high number of deviations. This indicates a potential systemic issue with their quality systems or operational discipline. **Action:** As the MSAT lead, I would schedule a deep-dive technical meeting with CDMO Gamma to review every deviation from the last quarter and co-develop a robust CAPA plan.
    - **CDMO Alpha Improvement:** This site experienced a critical deviation in Q1 but has since maintained a 100% success rate with a declining deviation trend in Q2. This suggests that their corrective actions were effective. **Action:** I will follow up during our next QBR to confirm the sustainability of this improvement.
    """)
st.divider()

# --- 3. Supply Chain Readiness ---
st.header("3. Critical Raw Material Inventory at CDMO Sites")
st.caption("Proactively monitoring long-lead-time material inventory to ensure continuity of supply.")

def style_inventory(df):
    style = pd.DataFrame('', index=df.index, columns=df.columns)
    style.loc[df['Status'] == 'Below Safety Stock', :] = 'background-color: #d62728; color: white'
    style.loc[df['Status'] == 'Re-order Point', :] = 'background-color: #FFB81C; color: black'
    return style

st.dataframe(inventory_df.style.apply(style_inventory, axis=None), use_container_width=True, hide_index=True)

with st.expander("🔬 **MSAT Analysis & Supply Chain Actions**"):
    st.markdown("""
    This table provides crucial visibility into potential supply chain bottlenecks that could halt production.
    - **Immediate Risk:** The **Viral Filter** at **CDMO Gamma** is below safety stock. This is a critical, long-lead-time item. A production delay is imminent if a new order is not expedited. **Action:** I will immediately contact our supply chain group and the CDMO to understand the status of the next delivery and assess the immediate risk to the upcoming campaign.
    - **Proactive Action:** The **IEX-2 Resin** at **CDMO Beta** has hit its re-order point. **Action:** I will confirm with our supply chain counterparts that a new purchase order has been placed to prevent a future stockout.
    """)
