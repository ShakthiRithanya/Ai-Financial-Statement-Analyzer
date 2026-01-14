import pandas as pd
import streamlit as st

def validate_financial_data(df):
    """
    Checks if critical columns are present.
    """
    critical_cols = ['revenue', 'net_income']
    missing = [col for col in critical_cols if col not in df.columns]
    
    if missing:
        return False, f"Missing critical data: {', '.join(missing)}"
    return True, "Data validated."

def format_currency(val):
    """Format large numbers for display."""
    if abs(val) >= 1_000_000_000:
        return f"${val/1_000_000_000:.2f}B"
    if abs(val) >= 1_000_000:
        return f"${val/1_000_000:.2f}M"
    return f"${val:,.0f}"

def get_demo_data():
    """Returns sample financial data for Apple Inc. (Approximate)."""
    data = {
        'revenue': {'2021': 365817, '2022': 394328, '2023': 383285},
        'net_income': {'2021': 94680, '2022': 99803, '2023': 96995},
        'operating_income': {'2021': 108949, '2022': 119437, '2023': 114301},
        'current_assets': {'2021': 134836, '2022': 135405, '2023': 143566},
        'current_liabilities': {'2021': 125481, '2022': 153982, '2023': 145308},
        'total_debt': {'2021': 124719, '2022': 120069, '2023': 111088},
        'equity': {'2021': 63090, '2022': 50672, '2023': 62146},
        'operating_cash_flow': {'2021': 104038, '2022': 122151, '2023': 110543},
        'capital_expenditure': {'2021': -11085, '2022': -10708, '2023': -10959}
    }
    return pd.DataFrame(data)

def custom_metric_card(label, value, delta=None, icon="📈", fixed_height=True):
    """
    Returns HTML string for a custom premium metric card - LIGHT THEME VERSION.
    """
    delta_html = ""
    if delta:
        color = "#10b981" if not str(delta).startswith("-") else "#ef4444"
        prefix = "+" if not str(delta).startswith("-") else ""
        delta_html = f'<div style="color: {color}; font-size: 0.9rem; font-weight: 700; margin-top: 4px;">{prefix}{delta}</div>'
    
    height_style = "min-height: 200px; display: flex; flex-direction: column; justify-content: space-between;" if fixed_height else ""
        
    html = f"""
<div style="background: linear-gradient(135deg, rgba(255, 255, 255, 0.9) 0%, rgba(243, 244, 246, 0.8) 100%); backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px); border: 2px solid rgba(139, 92, 246, 0.2); border-radius: 24px; padding: 24px; color: #1a1a2e; box-shadow: 0 12px 40px 0 rgba(139, 92, 246, 0.15); position: relative; overflow: hidden; margin-bottom: 20px; {height_style}">
<div style="position: absolute; top: -10px; right: -10px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%); border-radius: 50%;"></div>
<div style="display: flex; justify-content: space-between; align-items: flex-start; z-index: 1; position: relative; width: 100%;">
<div style="flex-grow: 1;">
<div style="font-size: 0.75rem; color: #8b5cf6; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px;">{label}</div>
<div style="font-size: 2rem; font-weight: 800; margin: 8px 0; letter-spacing: -0.5px; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.2;">{value}</div>
{delta_html}
</div>
<div style="font-size: 1.8rem; background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(236, 72, 153, 0.1)); padding: 12px; border-radius: 16px; border: 2px solid rgba(139, 92, 246, 0.2); margin-left: 10px;">{icon}</div>
</div>
</div>
"""
    return html
