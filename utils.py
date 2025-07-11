# utils.py

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import date, timedelta
from scipy import stats, signal
from scipy.optimize import minimize

# --- ML/Advanced Analytics Library Imports ---
import lightgbm as lgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, PolynomialFeatures, StandardScaler
from sklearn.linear_model import LinearRegression

# --- Custom Plotly Template for Halozyme ---
halozyme_template = {
    "layout": {
        "font": {"family": "Arial, sans-serif", "size": 12, "color": "#4A4A4A"},
        "title": {"font": {"family": "Arial, sans-serif", "size": 18, "color": "#002F6C"}, "x": 0.05},
        "plot_bgcolor": "#F8F8F8",
        "paper_bgcolor": "#FFFFFF",
        "colorway": ["#005EB8", "#F36633", "#00A9E0", "#8DC63F", "#6F1D77", "#FFB81C"],
        "xaxis": {"gridcolor": "#DCDCDC", "linecolor": "#B0B0B0", "zerolinecolor": "#DCDCDC", "title_font": {"size": 14}},
        "yaxis": {"gridcolor": "#DCDCDC", "linecolor": "#B0B0B0", "zerolinecolor": "#DCDCDC", "title_font": {"size": 14}},
        "legend": {"bgcolor": "rgba(255,255,255,0.85)", "bordercolor": "#CCCCCC", "borderwidth": 1}
    }
}
pio.templates["halozyme"] = halozyme_template
pio.templates.default = "halozyme"

# === CORE DATA GENERATION (MSAT & CDMO Oversight) ===

def generate_campaign_portfolio_data():
    """Generates portfolio data for manufacturing campaigns and tech transfers at CDMOs."""
    data = {
        'Campaign / Transfer': [
            'rHuPH20 2024 H1 Campaign',
            'Product B Tech Transfer',
            'rHuPH20 2024 H2 Campaign',
            'Product C Process Validation',
            'Product B Engineering Runs'
        ],
        'Product': ['rHuPH20', 'Product B', 'rHuPH20', 'Product C', 'Product B'],
        'CDMO Site': ['CDMO Alpha', 'CDMO Beta', 'CDMO Alpha', 'CDMO Gamma', 'CDMO Beta'],
        'Phase': ['Commercial Manufacturing', 'Tech Transfer', 'Commercial Manufacturing', 'Process Validation', 'Engineering Runs'],
        'Status': ['Complete', 'In Progress', 'In Progress', 'At Risk', 'On Hold'],
        'Lead Engineer': ['P. Engineer', 'J. Doe', 'P. Engineer', 'S. Smith', 'J. Doe'],
        'Batch Success Rate (%)': [100, 100, 95, 80, 100],
        'Open Critical Deviations': [0, 1, 2, 1, 0],
        'Start Date': [date(2024, 1, 15), date(2024, 3, 1), date(2024, 7, 1), date(2024, 6, 10), date(2024, 9, 1)],
        'End Date': [date(2024, 6, 30), date(2024, 12, 31), date(2024, 12, 20), date(2024, 9, 15), date(2024, 11, 30)],
    }
    df = pd.DataFrame(data)
    df['Start Date'] = pd.to_datetime(df['Start Date'])
    df['End Date'] = pd.to_datetime(df['End Date'])
    return df

def generate_manufacturing_risk_data():
    """Generates risk data relevant to external biomanufacturing."""
    data = {
        'Risk ID': ['RISK-SUP-01', 'RISK-PROC-01', 'RISK-COMP-01', 'RISK-TRANS-01'],
        'CDMO Site': ['CDMO Alpha', 'CDMO Gamma', 'CDMO Alpha', 'CDMO Beta'],
        'Risk Description': [
            'Single-source supplier for Protein A resin faces potential shortage.',
            'New viral filtration membrane shows higher-than-expected pressure increase.',
            'Aging UF/DF skid control system has no modern equivalent for replacement.',
            'Discrepancy in scale-down model for impurity clearance at new site.'
        ],
        'Impact': [5, 4, 4, 3], 'Probability': [3, 4, 2, 4],
        'Owner': ['Supply Chain / MSAT', 'P. Engineer', 'Engineering / MSAT', 'MSAT'],
        'Mitigation Status': ['In Progress', 'Investigation Open', 'CAPA Proposed', 'Additional Studies Planned']
    }
    df = pd.DataFrame(data)
    df['Risk Score'] = df['Impact'] * df['Probability']
    return df.sort_values(by='Risk Score', ascending=False)

# === PROCESS CHARACTERIZATION DATA ===

def generate_chromatography_data(high_impurity=False):
    """Generates a simulated chromatogram for a downstream purification step."""
    time = np.linspace(0, 60, 600)
    peak_impurity_1 = stats.norm.pdf(time, 15, 0.8) * (25 if high_impurity else 5)
    peak_product = stats.norm.pdf(time, 25, 2.5) * 100
    peak_impurity_2 = stats.norm.pdf(time, 35, 1.2) * (30 if high_impurity else 8)
    baseline = np.random.rand(600) * 0.5 + (time / 60) * 2
    signal = peak_impurity_1 + peak_product + peak_impurity_2 + baseline
    return pd.DataFrame({'Time (min)': time, 'UV (mAU)': signal})

def generate_ufdf_data():
    """Generates data for a UF/DF (TFF) run, including a pressure event."""
    volume = np.linspace(20, 2, 30) # Liters
    base_flux = 60 - np.linspace(0, 15, 30) # LMH, linear decay
    flux = base_flux + np.random.normal(0, 1.5, 30)
    tmp = 15 + np.log(61 - base_flux) + np.random.normal(0, 0.2, 30) # psi
    # Simulate a fouling event
    flux[20:] = flux[20:] - np.linspace(0, 10, 10)
    tmp[20:] = tmp[20:] + np.linspace(0, 5, 10)
    return pd.DataFrame({'Volume (L)': volume, 'Flux (LMH)': flux, 'TMP (psi)': tmp})

# === CONTINUED PROCESS VERIFICATION (CPV) DATA ===

def generate_cpv_data():
    """Generates historical batch data for CPV monitoring of CPPs and CQAs."""
    np.random.seed(123)
    n_batches = 50
    batches = [f"B0{i+100}" for i in range(n_batches)]
    # CQA: Purity by RP-HPLC (%)
    purity = np.random.normal(98.5, 0.25, n_batches)
    purity[30:35] = np.random.normal(97.8, 0.1, 5) # Process shift
    # CPP: IEX Pool Conductivity (mS/cm)
    conductivity = np.random.normal(15.2, 0.5, n_batches)
    conductivity[40] = 17.5 # Special cause variation
    # CPP: UF/DF Concentration Factor
    conc_factor = np.random.normal(10.1, 0.15, n_batches)
    return pd.DataFrame({'Batch ID': batches, 'Purity (%)': purity, 'Conductivity (mS/cm)': conductivity, 'Concentration Factor': conc_factor})

# === DOE DATA (Downstream Process Optimization) ===

def generate_process_optimization_doe_data():
    """Generates DOE data for optimizing a chromatography step."""
    np.random.seed(42)
    # Factors: pH and Salt Concentration (NaCl)
    ph_levels = np.array([-1.414, -1, 1, -1, 1, 0, 0, 0, 0, -1.414, 1.414])
    salt_levels = np.array([0, -1, -1, 1, 1, -1.414, 1.414, 0, 0, 0, 0])
    
    ph_real = ph_levels * 0.2 + 7.0  # e.g., 6.8-7.2 range
    salt_real = salt_levels * 25 + 100 # e.g., 75-125 mM range

    # Response 1: Yield (%)
    true_yield = 90 - (2*ph_levels**2) - (4*salt_levels**2) + (1.5*ph_levels*salt_levels)
    measured_yield = true_yield + np.random.normal(0, 1.2, len(ph_real))
    
    # Response 2: Impurity Clearance (log removal value - LRV)
    true_lrv = 2.5 + (0.3*ph_levels) - (0.5*salt_levels) - (0.2*ph_levels*salt_levels)
    measured_lrv = true_lrv + np.random.normal(0, 0.1, len(ph_real))
    
    return pd.DataFrame({'pH': ph_real, 'NaCl (mM)': salt_real, 'Yield (%)': measured_yield, 'Impurity LRV': measured_lrv})

# === DEVIATION & CHANGE CONTROL DATA ===

def generate_deviation_data():
    """Generates data for a deviation tracker."""
    data = {
        'Deviation ID': ['DEV-24-051', 'DEV-24-052', 'DEV-24-053'],
        'CDMO Site': ['CDMO Alpha', 'CDMO Gamma', 'CDMO Alpha'],
        'Product': ['rHuPH20', 'Product C', 'rHuPH20'],
        'Event Description': [
            'IEX chromatography pool conductivity out of spec (high).',
            'Pressure failed to hold during pre-use filter integrity test.',
            'Column HETP value exceeded alert limit during requalification.'
        ],
        'MSAT Assessment Lead': ['P. Engineer', 'S. Smith', 'P. Engineer'],
        'Status': ['Root Cause Investigation', 'Impact Assessment Complete', 'CAPA Implementation'],
        'Age (Days)': [5, 12, 45]
    }
    return pd.DataFrame(data)

def generate_change_control_data():
    """Generates data for a change control tracker."""
    data = {
        'Change ID': ['CC-24-012', 'CC-24-013'],
        'CDMO Site': ['CDMO Alpha', 'CDMO Beta'],
        'Change Description': [
            'Proposal to replace aging UF/DF skid with new model.',
            'Introduction of a new buffer supplier for Product B campaign.'
        ],
        'Regulatory Impact': ['CBE-30', 'Annual Report'],
        'MSAT Lead': ['P. Engineer', 'J. Doe'],
        'Status': ['Awaiting Funding Approval', 'Implementation Plan Drafted']
    }
    return pd.DataFrame(data)

def generate_pareto_data():
    """Generates data for a deviation root cause Pareto chart."""
    return pd.DataFrame({
        'Root Cause Category': ['Buffer Preparation Error', 'Operator Error', 'Column Performance', 'Equipment Malfunction', 'Raw Material Variability', 'Procedure Ambiguity'],
        'Count': [12, 7, 5, 3, 2, 1]
    }).sort_values('Count', ascending=False)
    
# === TECHNOLOGY TRANSFER DATA ===

def generate_tech_transfer_checklist():
    """Generates a checklist for a typical downstream tech transfer project."""
    data = {
        'Phase': [
            "1. Process Familiarization", "1. Process Familiarization",
            "2. Facility Fit & Engineering", "2. Facility Fit & Engineering", "2. Facility Fit & Engineering",
            "3. Validation & Execution", "3. Validation & Execution", "3. Validation & Execution"
        ],
        'Task': [
            'Transfer Process Description & Batch Records',
            'On-site "Person-in-Plant" for demonstration runs',
            'Raw Material & Consumable Sourcing/Equivalency',
            'Equipment Qualification Review (IQ/OQ)',
            'Execute Small-Scale Engineering/Tox Batch',
            'Execute Process Validation (PV) Batches (3x)',
            'Complete PV Summary Report',
            'Update Regulatory Filing with New Site Data'
        ],
        'Owner': ['MSAT Lead', 'MSAT/CDMO', 'CDMO/Supply Chain', 'CDMO QA/Eng', 'CDMO/MSAT', 'CDMO Ops', 'MSAT Lead', 'Regulatory/MSAT'],
        'Status': ['Complete', 'Complete', 'In Progress', 'Complete', 'Complete', 'At Risk', 'Not Started', 'Not Started']
    }
    return pd.DataFrame(data)
