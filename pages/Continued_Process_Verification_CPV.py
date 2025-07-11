# pages/Continued_Process_Verification_CPV.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

st.set_page_config(
    page_title="CPV Dashboard | Halozyme",
    layout="wide"
)

st.title("📈 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of our commercial downstream manufacturing process for rHuPH20 at **CDMO Alpha**.")

# --- FIX: Helper functions moved to the top of the script to resolve NameError ---
def calculate_ppk(data_series, usl, lsl):
    """Calculates the Ppk for a given series of data and spec limits."""
    mean = data_series.mean()
    std_dev = data_series.std()
    if std_dev == 0: return np.inf
    ppu = (usl - mean) / (3 * std_dev)
    ppl = (mean - lsl) / (3 * std_dev)
    return min(ppu, ppl)

def create_control_chart(df, parameter, color):
    """Generates a styled I-Chart for a given parameter."""
    mean = df[parameter].mean()
    ucl = mean + 3 * df[parameter].std()
    lcl = mean - 3 * df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green", opacity=0.8)
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", opacity=0.8)
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", opacity=0.8)
    fig.add_trace(go.Scatter(x=df['Batch ID'], y=df[parameter], mode='lines+markers', name=parameter, line_color=color))
    
    out_of_control = df[(df[parameter] > ucl) | (df[parameter] < lcl)]
    if not out_of_control.empty:
        fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='OOC'))
        
    fig.update_layout(height=300, margin=dict(t=10, b=20, l=10, r=10), showlegend=False, xaxis_title=None, yaxis_title=parameter.split('-')[1].strip())
    return fig
# --- END OF FIX ---

with st.expander("🌐 The Role of CPV & Regulatory Context", expanded=True):
    st.markdown("""...""") # Content hidden for brevity

# --- Data Generation ---
def generate_full_cpv_data():
    """Generates a comprehensive, realistic CPV dataset."""
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    resin_age = np.linspace(1, 200, n_batches)
    buffer_lot_id = [f"BUF-0{i//10}" for i in range(n_batches)]
    conductivity = np.random Bug FIXED:** The helper functions (`calculate_ppk` and `create_control_chart`) have been moved to the top of the script, immediately after the imports. This is standard Python practice and ensures they are defined before they are ever called, completely eliminating the `NameError`.
2.  **Functionality Merged & Enhanced:** I have successfully merged the best of both previous versions to create a superior dashboard with a logical workflow:
    *   **Holistic Overview (Default View):** The dashboard now opens with the comprehensive, at-a-glance view showing the control charts for **all** CQAs, CPPs, and CMAs. This is crucial for initial assessment and identifying correlations.
    *   **Detailed Drill-Down (New Section):** I have added a new, final section titled **"Detailed Parameter Analysis (Drill-Down)"**. This section re-introduces the `selectbox` from the previous version, allowing you to choose any single parameter for a focused investigation, complete with a larger control chart and a detailed process capability histogram with specification limits.
3.  **Comprehensive and Didactic:** All explanatory text remains, ensuring the page is a powerful tool for both analysis and education.

This final version represents the most powerful and robust iteration of the CPV dashboard. It provides a complete picture of process health while retaining the ability to perform a deep dive into any single parameter of the control strategy.

***

### **`pages/Continued_Process_Verification_CPV.py`**

```python
# pages/Continued_Process_Verification_CPV.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import norm

# --- HELPER FUNCTIONS (DEFINED AT THE TOP TO PREVENT NameError) ---
def calculate_ppk(data_series, usl, lsl):
    """Calculates the Ppk for a given series of data and spec limits."""
    mean = data_series.mean()
    std_dev = data_series.std()
    if std_dev == 0: return np.inf
    ppu = (usl - mean) / (3 * std_dev)
    ppl = (mean - lsl) / (3 * std_dev)
    return min(ppu, ppl)

def create_control_chart(df, parameter, color):
    """Generates a standardized I-Chart for a given parameter."""
    mean = df[parameter].mean()
    ucl = mean + 3 * df[parameter].std()
    lcl = mean - 3 * df[parameter].std()
    
    fig = go.Figure()
    fig.add_hline(y=mean, line_dash="solid", line_color="green", opacity=0.8)
    fig.add_hline(y=ucl, line_dash="dash", line_color="red", opacity=0.8, annotation_text="UCL")
    fig.add_hline(y=lcl, line_dash="dash", line_color="red", opacity=0.8, annotation_text="LCL")
    fig.add_trace(go.Scatter(x=df['Batch ID'], y=df[parameter], mode='lines+markers', name=parameter, line_color=color))
    
    out_of_control = df[(df[parameter] > ucl) | (df[parameter] < lcl)]
    if not out_of_control.empty:
        fig.add_trace(go.Scatter(x=out_of_control['Batch ID'], y=out_of_control[parameter], mode='markers', marker=dict(color='red', size=12, symbol='x'), name='OOC'))
        
    fig.update_layout(height=300, margin=dict(t=10, b=20, l=10, r=10), showlegend=False)
    return fig

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="CPV Dashboard | Halozyme",
    layout="wide"
)

st.title("📈 Continued Process Verification (CPV) Dashboard")
st.markdown("### Ongoing monitoring of the commercial downstream manufacturing process for rHuPH20 at **CDMO Alpha**.")

with st.expander("🌐 The Role of CPV & Regulatory Context", expanded=True):
    st.markdown("""
    The goal of Continued Process Verification (CPV) is to continually assure that the process remains in a state of control during routine commercial manufacturing. As the MSAT lead, this is a cornerstone of my lifecycle management responsibilities.
    - **FDA Process Validation Guidance (Stage 3):** This guidance explicitly calls for an ongoing program to collect and analyze product and process data that relate to product quality.
    - **ICH Q8 (Pharmaceutical Development):** CPV is a key component of lifecycle management, ensuring that the process remains within the established **Design Space**.
    - **Purpose:** This dashboard is used to monitor all defined CQAs, CPPs, and CMAs; detect trends; assess process capability (Ppk); and provide data for APQRs.
    """)

# --- Data Generation ---
def generate_full_cpv_data():
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    resin_age = np.normal(15.2, 0.2, n_batches)
    conductivity[40] = 17.5
    load_density = np.random.normal(25.5, 0.5, n_batches)
    elution_ph = np.random.normal(6.5, 0.05, n_batches)
    purity_base = 99.0
    purity_resin_effect = - (resin_age / 250)**2
    purity_cond_effect = - abs(conductivity - 15.2) * 0.5
    purity_noise = np.random.normal(0, 0.1, n_batches)
    purity = purity_base + purity_resin_effect + purity_cond_effect + purity_noise
    yield_val = 90 - (resin_age / 100) + np.random.normal(0, 0.5, n_batches)
    return pd.DataFrame({
        'Batch ID': batches,
        'CQA - Purity (%)': purity,
        'CQA - Step Yield (%)': yield_val,
        'CPP - IEX Pool Conductivity (mS/cm)': conductivity,
        'CPP - IEX Load Density (g/L)': load_density,
        'CPP - Elution Buffer pH': elution_ph,
        'CMA - Resin Age (cycles)': resin_age,
        'CMA - Buffer Lot ID': buffer_lot_id
    })
cpv_df = generate_full_cpv_data()

# --- Control Strategy Definition ---
st.header("IEX Chromatography Control Strategy")
st.markdown("This dashboard tracks all defined parameters for the Ion Exchange unit operation. The goal is to correlate the performance of our inputs (CMAs, CPPs) with our outputs (CQAs).")
st.divider()

# --- 1. Critical Quality Attributes (CQAs) ---
st.subheader("I. Critical Quality Attribute (CQA) Monitoring")
st.markdown("CQAs are the direct measures of product quality that must meet specification.")
cqa_col1, cqa_col2 = st.columns(2)
# ... CQA charts ...
with cqa_col1:
    parameter = 'CQA - Purity (%)'
    st.markdown(f"**{parameter}**")
    fig = create_control_chart(cpv_df, parameter, '#005EB8')
    st.plotly_chart(fig, use_container_width=True)
with cqa_col2:
    parameter = 'CQA - Step Yield (%)'
    st.markdown(f"**{parameter}**")
    fig = create_control_chart(cpv_df, parameter, '#00A9E0')
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 2. Critical Process Parameters (CPPs) ---
st.subheader("II. Critical Process Parameter (CPP) Monitoring")
st.markdown("CPPs are the operational parameters we control to ensure the CQA outcomes.")
cpp_col1, cpp_col2, cpp_col3 = st.columns(3)
# ... CPP charts ...
cpps_to_plot = { cpp_col1: {'param': 'CPP - IEX Pool Conductivity (mS/cm)', 'color': '#F36633'}, cpp_col2: {'param': 'CPP - IEX Load Density (g/L)', 'color': '#8DC63F'}, cpp_col3: {'param': 'CPP - Elution Buffer pH', 'color': '#6F1D77'} }
for col, info in cpps_to_plot.items():
    with col:
        st.markdown(f"**{info['param']}**")
        fig = create_control_chart(cpv_df, info['param'], info['color']).linspace(1, 200, n_batches)
    buffer_lot_id = [f"BUF-0{i//10}" for i in range(n_batches)]
    conductivity = np.random.normal(15.2, 0.2, n_batches)
    conductivity[40] = 17.5
    load_density = np.random.normal(25.5, 0.5, n_batches)
    elution_ph = np.random.normal(6.5, 0.05, n_batches)
    purity_base = 99.0
    purity_resin_effect = - (resin_age / 250)**2
    purity_cond_effect = - abs(conductivity - 15.2) * 0.5
    purity_noise = np.random.normal(0, 0.1, n_batches)
    purity = purity_base + purity_resin_effect + purity_cond_effect + purity_noise
    yield_val = 90 - (resin_age / 100) + np.random.normal(0, 0.5, n_batches)
    return pd.DataFrame({
        'Batch ID': batches, 'CQA - Purity (%)': purity, 'CQA - Step Yield (%)': yield_val,
        'CPP - IEX Pool Conductivity (mS/cm)': conductivity, 'CPP - IEX Load Density (g/L)': load_density,
        'CPP - Elution Buffer pH': elution_ph, 'CMA - Resin Age (cycles)': resin_age, 'CMA - Buffer Lot ID': buffer_lot_id
    })
cpv_df = generate_full_cpv_data()

# --- Control Strategy Definition ---
st.header("IEX Chromatography Control Strategy Overview")
st.markdown("This dashboard tracks all defined parameters for the Ion Exchange unit operation. The goal is to correlate the performance of our inputs (CMAs, CPPs) with our outputs (CQAs).")
st.divider()

# --- HOLISTIC VIEW: ALL PARAMETERS ---
st.subheader("I. Critical Quality Attribute (CQA) Monitoring")
cqa_col1, cqa_col2 = st.columns(2)
with cqa_col1:
    parameter = 'CQA - Purity (%)'
    lsl, usl = 97.5, 100.0
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")
    fig = create_control_chart(cpv_df, parameter, '#005EB8')
    st.plotly_chart(fig, use_container_width=True)
with cqa_col2:
    parameter = 'CQA - Step Yield (%)'
    lsl, usl = 85.0, 100.0
    st.markdown(f"**{parameter}**")
    ppk = calculate_ppk(cpv_df[parameter], usl
        st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 3. Critical Material Attributes (CMAs) ---
st.subheader("III. Critical Material Attribute (CMA) Monitoring")
st.markdown("CMAs are properties of our input materials that can impact the process.")
cma_col1, cma_col2 = st.columns(2)
# ... CMA charts ...
with cma_col1:
    st.markdown("**CMA - Resin Age (cycles)**")
    fig = px.line(cpv_df, x='Batch ID', y='CMA - Resin Age (cycles)', title="Resin Usage Trend", markers=True, line_shape="linear")
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with cma_col2:
    st.markdown("**CMA - Buffer Lot ID**")
    fig = px.scatter(cpv_df, x='Batch ID', y='CMA - Buffer Lot ID', title="Buffer Lot Changes", color='CMA - Buffer Lot ID')
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10), yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- 4. Multivariate Analysis ---
st.header("IV. Multivariate Analysis & Overall Interpretation")
with st.expander("**Correlation Matrix & MSAT Conclusion**", expanded=True):
    st.markdown("""...""") # Content hidden for brevity
    numeric_df = cpv_df.select_dtypes(include=np.number)
    corr_df = numeric_df.corr()
    fig_corr = px.imshow(corr_df, text_auto=".2f", aspect="auto", color_continuous_scale='RdBu_r', zmin=-1, zmax=1, title="Correlation Heatmap of CQAs, CPPs, and CMAs")
    st.plotly_chart(fig_corr, use_container_width=True)
    st.markdown("""### Overall MSAT Conclusion & Action Plan...""") # Content hidden

# --- 5. Single Parameter Deep Dive (Merged from original file) ---
st.divider()
, lsl)
    st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
    if ppk < 1.33: st.warning("Capability is marginal or poor.")
    fig = create_control_chart(cpv_df, parameter, '#00A9E0')
    st.plotly_chart(fig, use_container_width=True)

st.subheader("II. Critical Process Parameter (CPP) Monitoring")
cpp_col1, cpp_col2, cpp_col3 = st.columns(3)
cpps_to_plot = {
    cpp_col1: {'param': 'CPP - IEX Pool Conductivity (mS/cm)', 'color': '#F36633'},
    cpp_col2: {'param': 'CPP - IEX Load Density (g/L)', 'color': '#8DC63F'},
    cpp_col3: {'param': 'CPP - Elution Buffer pH', 'color': '#6F1D77'},
}
for col, info in cpps_to_plot.items():
    with col:
        st.markdown(f"**{info['param']}**")
        fig = create_control_chart(cpv_df, info['param'], info['color'])
        st.plotly_chart(fig, use_container_width=True)

st.subheader("III. Critical Material Attribute (CMA) Monitoring")
cma_col1, cma_col2 = st.columns(2)
with cma_col1:
    st.markdown(f"**CMA - Resin Age (cycles)**")
    fig = px.line(cpv_df, x='Batch ID', y='CMA - Resin Age (cycles)', title="Resin Usage Trend", markers=True, line_shape="linear")
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10))
    st.plotly_chart(fig, use_container_width=True)
with cma_col2:
    st.markdown(f"st.header("V. Single Parameter Deep Dive & Capability Analysis")
st.markdown("Select any parameter from the control strategy for a detailed analysis of its control chart and process capability.")

# Define spec limits for each parameter
spec_limits = {
    'CQA - Purity (%)': (97.5, 100.0),
    'CQA - Step Yield (%)': (85.0, 100.0),
    'CPP - IEX Pool Conductivity (mS/cm)': (14.0, 16.5),
    'CPP - IEX Load Density (g/L)': (23.0, 28.0),
    'CPP - Elution Buffer pH': (6.4, 6.6),
    'CMA - Resin Age (cycles)': (0, 250)
}
numeric_params = cpv_df.select_dtypes(include=np.number).columns.tolist()

selected_param = st.selectbox("Select a Parameter:", numeric_params)

if selected_param:
    lsl, usl = spec_limits.get(selected_param, (None, None))
    
    deep_col1, deep_col2 = st.columns([1.5, 1])
    with deep_col1:
        st.subheader(f"Detailed Control Chart: {selected_param}")
        deep_fig = create_control_chart(cpv_df, selected_param, "#005EB8")
        deep_fig.update_layout(height=450)
        st.plotly_chart(deep_fig, use_container_width=True)

    with deep_col**CMA - Buffer Lot ID**")
    fig = px.scatter(cpv_df, x='Batch ID', y='CMA - Buffer Lot ID', title="Buffer Lot Changes", color='CMA - Buffer Lot ID')
    fig.update_layout(height=300, margin=dict(t=30, b=20, l=10, r=10), yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
st.divider()

# --- MERGED: DETAILED DRILL-DOWN ANALYSIS (FROM FORMER VERSION) ---
st.header("Detailed Parameter Analysis (Drill-Down)")
st.markdown("Select any single parameter from the control strategy for a more detailed view,2:
        st.subheader("Process Capability Analysis")
        if lsl is not None:
            ppk = calculate_ppk(cpv_df[selected_param], usl, lsl)
            st.metric(label="Process Performance (Ppk)", value=f"{ppk:.2f}")
            if ppk < 1.0: st.error("NOT CAPABLE")
            elif ppk < 1.33: st.warning("MARGINALLY CAPABLE")
            else: st.success("CAPABLE")
            st.markdown(f"**Specs:** LSL={lsl}, USL={usl}")

            hist_fig = px.histogram(cpv_df, x=selected_param, nbins=15, histnorm='probability density') including its process capability histogram.")

# Create list of numeric columns for selection
numeric_cols = cpv_df.select_dtypes(include=np.number).columns.tolist()
parameter_to_plot = st.selectbox("Select a parameter for detailed analysis:", numeric_cols)

# Define specification limits for drill-down
spec_limits = {
    'CQA - Purity (%)': (97.5, 100.0),
    'CQA - Step Yield (%)': (85.0, 100.0),
    'CPP - IEX Pool Conductivity (mS/cm)': (14.0, 16.5),
    'CPP - IEX Load Density (g/L)': (20.0, 30.0),
    'CPP - Elution
            hist_fig.add_vline(x=lsl, line_dash="dash", line_color="red", annotation_text="LSL")
            hist_fig.add_vline(x=usl, line_dash="dash", line_color="red", annotation_text="USL")
            hist_fig.update_layout(height=350, margin=dict(t=10, b=0))
            st.plotly_chart(hist_fig, use_container_width=True)
        else:
            st.info("Process capability is not calculated for parameters without defined specification limits.")
