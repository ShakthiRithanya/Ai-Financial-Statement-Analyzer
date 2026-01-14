import pandas as pd
import numpy as np
import re

# Mapping of common financial terms to standardized keys
FINANCIAL_MAPPING = {
    'revenue': ['revenue', 'sales', 'total revenue', 'turnover', 'net sales'],
    'net_income': ['net income', 'net profit', 'profit for the year', 'earnings', 'net loss'],
    'operating_income': ['operating income', 'ebit', 'operating profit'],
    'total_assets': ['total assets', 'assets'],
    'total_liabilities': ['total liabilities', 'liabilities'],
    'equity': ['equity', "shareholders' equity", "total equity", "equity attributable"],
    'current_assets': ['current assets'],
    'current_liabilities': ['current liabilities'],
    'operating_cash_flow': ['operating cash flow', 'cash from operating activities', 'net cash from operating activities'],
    'capital_expenditure': ['capex', 'capital expenditure', 'purchase of property', 'purchase of ppe'],
    'total_debt': ['total debt', 'long term debt', 'short term debt', 'borrowings']
}

def clean_value(val):
    """
    Cleans string values into floats. Handles (parentheses) as negative numbers.
    """
    if pd.isna(val) or val == '':
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    
    val = str(val).strip().replace(',', '')
    if '(' in val and ')' in val:
        val = '-' + val.replace('(', '').replace(')', '')
    
    # Remove non-numeric characters except . and -
    val = re.sub(r'[^\d.-]', '', val)
    
    try:
        return float(val)
    except ValueError:
        return 0.0

def normalize_dataframe(df):
    """
    Attempts to find horizontal headers (years) and vertical labels (line items).
    """
    # Clean the dataframe column names
    df.columns = [str(c).strip().lower() for c in df.columns]
    
    # Try to identify the 'Label' column (usually the first one with text)
    label_col = df.columns[0]
    
    results = {}
    
    # Identify relevant years (columns that look like 2022, 2023, etc.)
    year_cols = []
    for col in df.columns:
        if re.match(r'20\d{2}', col):
            year_cols.append(col)
    
    if not year_cols:
        # If no years in headers, maybe they are in the first row?
        # For simplicity in MVP, we expect years as headers or we use indices
        year_cols = [c for c in df.columns if c != label_col]

    for standardized_key, aliases in FINANCIAL_MAPPING.items():
        for _, row in df.iterrows():
            label = str(row[label_col]).lower().strip()
            if any(alias in label for alias in aliases):
                # Found a match, extract values for available years
                data_points = {}
                for year in year_cols:
                    try:
                        data_points[year] = clean_value(row[year])
                    except:
                        continue
                results[standardized_key] = data_points
                break # Move to next standardized key
                
    return results

def process_multiple_tables(list_of_dfs):
    """
    Combines results from multiple tables into a single master dictionary.
    """
    master_data = {}
    for df in list_of_dfs:
        norm_data = normalize_dataframe(df)
        for key, year_data in norm_data.items():
            if key not in master_data:
                master_data[key] = year_data
            else:
                master_data[key].update(year_data)
    
    # Convert to DataFrame: Years as index, Line items as columns
    final_df = pd.DataFrame(master_data).sort_index()
    return final_df
