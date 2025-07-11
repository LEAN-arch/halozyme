MSAT Command Center for External Manufacturing Oversight
Overview
The MSAT Command Center is a strategic Streamlit dashboard designed for the Manufacturing Sciences & Technology (MSAT) team at Halozyme. It provides a centralized, data-driven platform for the technical oversight of our global network of Contract Development and Manufacturing Organizations (CDMOs) responsible for producing our biologic drug substances, such as rHuPH20.

This application transforms raw manufacturing data and project status updates into actionable intelligence, enabling proactive management of technology transfers, process performance, and quality systems. It is built to support our "One Team" culture by fostering transparent, data-driven collaboration between Halozyme and our external partners.

Author: Principal Engineer 1, MSAT
Contact: p.engineer@halozyme.com

Key Features & Dashboards
This application is organized into a series of specialized dashboards, each tailored to a core responsibility of the MSAT role:

🏠 MSAT Command Center (app.py): The strategic home page providing a high-level overview of the entire CDMO network.

KPIs: Tracks network-wide batch success rates, open critical deviations, and active campaigns.

Portfolio View: A Gantt chart visualizing all ongoing manufacturing campaigns and technology transfers across all CDMO sites.

Risk Matrix: An ICH Q9-aligned risk register for prioritizing and managing risks to supply and quality.

🔬 Process Characterization Hub: A workspace for analyzing data from downstream process characterization (PC) studies.

Chromatography Analysis: Visualize and compare elution profiles to assess purity and impurity clearance.

UF/DF Performance: Monitor flux and transmembrane pressure (TMP) to characterize membrane performance and detect fouling.

🤖 Predictive Process Monitoring: Advanced analytics to proactively manage process health.

Deviation Prediction: Utilizes multivariate models to generate a "Deviation Risk Score" for batches, enabling intervention before a failure occurs.

Automated Root Cause Insights: A Pareto analysis of historical deviations to identify systemic issues and guide long-term improvement strategies.

🧪 Process Optimization (DOE): An interactive tool for designing and analyzing experiments to optimize manufacturing processes.

"Sweet Spot" Plot: Visualize the optimal operating window by overlaying multiple response contours (e.g., maximizing yield while minimizing an impurity).

✈️ Technology Transfer Dashboard: A tactical hub for managing the end-to-end transfer of a process to a new CDMO.

Kanban Board: Tracks high-level progress through the key phases of tech transfer.

Interactive Checklist: A granular, auditable checklist for all required tasks and deliverables.

📈 CDMO Oversight Dashboard: A dedicated view for monitoring the performance of individual CDMO partners.

Performance Trending: Tracks quarterly batch success rates and deviation trends per site.

Supply Chain Readiness: Monitors the inventory of critical raw materials at each CDMO to mitigate supply chain risks.

📊 Continued Process Verification (CPV): The home of our CPV program for commercial products.

Control Charts: Monitor Critical Process Parameters (CPPs) and Critical Quality Attributes (CQAs) for process drift or special cause variation.

Process Capability (Cpk): Periodically assess the ability of our process to meet specifications.

📋 Deviation & Change Control Hub: The interface to our Quality Management System for externally manufactured products.

Deviation Tracker: Manage and provide technical assessment for active deviations at CDMOs.

Change Control Log: Track and evaluate proposed changes to validated processes.

📄 Data Analytics Platform Info: A static page summarizing the validation status and intended use of our GxP-compliant data analysis tools, ensuring regulatory readiness.
