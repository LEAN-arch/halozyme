# pages/Technology_Transfer_Dashboard.py
import streamlit as st
import pandas as pd
from utils import generate_tech_transfer_checklist, generate_manufacturing_risk_data

st.set_page_config(
    page_title="Tech Transfer Dashboard | Halozyme",
    layout="wide"
)

st.title("✈️ Technology Transfer Dashboard")
st.markdown("### Managing the end-to-end transfer of downstream manufacturing processes to our CDMO partners.")

with st.expander("🌐 MSAT Role & Regulatory Context for Technology Transfer"):
    st.markdown("""
    Technology transfer is the formal process of transferring knowledge, processes, and specifications from Halozyme to our CDMO partners to ensure they can reproduce our manufacturing process consistently and compliantly. As the Principal MSAT Engineer, I lead this activity.

    - **ICH Q10, Section 2.7 (Management of Outsourced Activities and Purchased Materials):** This guideline emphasizes the need for a formal agreement and a structured process for transferring process knowledge. This dashboard is our primary tool for managing this process.
    - **FDA Guidance for Industry - Technology Transfer:** While not a binding regulation, FDA guidance outlines best practices, including the use of a tech transfer plan/protocol, risk assessments, and clear documentation—all of which are managed through this hub.
    - **The Goal:** To ensure the receiving unit (the CDMO) has the operational, technical, and regulatory capability to perform the process as intended, leading to successful engineering runs and process validation (PV) batches. A successful transfer is the foundation for a reliable supply chain.
    """)

# --- Select a Project to View ---
st.header("Select a Technology Transfer Project")
project_name = st.selectbox(
    "Select an active tech transfer project to view its status:",
    ("Product B to CDMO Beta", "Product D to CDMO Epsilon")
)
st.subheader(f"Status for: **{project_name}**")
st.divider()


# --- Data Generation ---
checklist_df = generate_tech_transfer_checklist()
risk_df = generate_manufacturing_risk_data()

# --- Kanban Board for Major Phases ---
st.header("Technology Transfer Phase Kanban Board")
st.caption("Tracking high-level progress through the major phases of the tech transfer lifecycle.")

# Simplified Kanban data for this view
phases = {
    'Phase 1: Familiarization': [('Transfer Process Description', 'Complete'), ('Gap Analysis', 'Complete')],
    'Phase 2: Facility Fit & Eng.': [('Raw Material Sourcing', 'In Progress'), ('Engineering Batch', 'Complete')],
    'Phase 3: Validation': [('PV Batch #1', 'At Risk'), ('PV Batch #2', 'Not Started'), ('PV Batch #3', 'Not Started')],
    'Phase 4: Regulatory & Closeout': [('PV Report Drafting', 'Not Started'), ('Regulatory Filing Update', 'Not Started')]
}

cols = st.columns(len(phases))
column_map = dict(zip(phases.keys(), cols))

for stage, col in column_map.items():
    with col:
        st.subheader(stage)
        for task, status in phases.get(stage, []):
            if status == 'Complete':
                st.success(f"**{task}**\n\n*Status: {status}*")
            elif status == 'At Risk':
                st.error(f"**{task}**\n\n*Status: {status}*")
            else:
                st.info(f"**{task}**\n\n*Status: {status}*")

st.divider()

# --- Granular Checklist and Risk ---
col1, col2 = st.columns((2, 1))

with col1:
    st.header("Detailed Tech Transfer Checklist")
    st.caption("A granular, auditable checklist of all required tasks and deliverables for the selected project.")
    
    st.data_editor(
        checklist_df,
        column_config={
            "Status": st.column_config.SelectboxColumn(
                "Status",
                help="Update the status of the task",
                options=["Not Started", "In Progress", "Complete", "At Risk"],
                required=True,
            )
        },
        use_container_width=True,
        hide_index=True,
        height=400
    )

with col2:
    st.header("Key Risks & Mitigations")
    st.caption("Top risks specifically associated with this technology transfer project.")
    
    # Filter risks for the selected project
    project_risks = risk_df[risk_df['CDMO Site'] == project_name.split(' to ')[1]].head(5)
    st.dataframe(
        project_risks[['Risk Description', 'Owner', 'Risk Score', 'Mitigation Status']],
        use_container_width=True,
        hide_index=True,
        height=400
    )

with st.expander("📊 **MSAT Action & Decision-Making**"):
    st.markdown("""
    #### Analysis of Current Status
    - **Kanban Board:** The high-level view immediately flags that the **Process Validation phase is 'At Risk'**. Specifically, PV Batch #1 has encountered an issue. This requires my immediate attention.
    - **Detailed Checklist:** The checklist provides the next level of detail. I can see that while most of the early-stage tasks are complete, the validation and regulatory tasks are lagging. The 'At Risk' status of the PV batches is the critical path item.
    - **Risk Register:** The top risk for CDMO Beta is a "Discrepancy in scale-down model." This is a highly probable cause for the issues seen in the PV batch.

    #### My Role as MSAT Lead
    1.  **Immediate Action:** My first priority is to convene a meeting with the CDMO technical team to perform a detailed technical assessment of the deviation that occurred during PV Batch #1.
    2.  **Hypothesis:** Based on the risk register, my primary hypothesis is that the scale-up from our lab's scale-down model to the CDMO's full-scale equipment was not linear for a key impurity.
    3.  **Path Forward:** I will lead the effort to analyze the data from PV Batch #1 and compare it to our scale-down model. The likely outcome is a proposal to execute an additional engineering batch with modified parameters before attempting PV Batch #2.
    4.  **Communication:** I will summarize these findings and the proposed path forward for the internal CMC team, clearly communicating the impact on project timelines and budget. This dashboard provides all the necessary data to support that communication.
    """)
