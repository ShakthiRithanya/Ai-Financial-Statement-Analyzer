import pandas as pd

def calculate_ratios(df):
    """
    Calculates financial ratios from the normalized dataframe.
    Expected columns in df: revenue, net_income, operating_income, total_assets, 
    total_liabilities, equity, current_assets, current_liabilities, 
    operating_cash_flow, capital_expenditure, total_debt.
    """
    results = {}
    
    # Check if we have the necessary columns
    cols = df.columns
    
    # 1. Profitability Ratios
    if 'revenue' in cols and 'net_income' in cols:
        results['Net Profit Margin'] = (df['net_income'] / df['revenue']) * 100
        
    if 'revenue' in cols and 'operating_income' in cols:
        results['Operating Margin'] = (df['operating_income'] / df['revenue']) * 100

    if 'revenue' in cols:
        results['Revenue Growth (%)'] = df['revenue'].pct_change() * 100

    # 2. Liquidity Ratios
    if 'current_assets' in cols and 'current_liabilities' in cols:
        results['Current Ratio'] = df['current_assets'] / df['current_liabilities']

    # 3. Solvency Ratios
    if 'total_debt' in cols and 'equity' in cols:
        results['Debt-to-Equity'] = df['total_debt'] / df['equity']
    elif 'total_liabilities' in cols and 'equity' in cols:
        # Fallback if total_debt isn't explicitly found
        results['Liabilities-to-Equity'] = df['total_liabilities'] / df['equity']

    # 4. Efficiency Ratios
    if 'net_income' in cols and 'equity' in cols:
        results['ROE (%)'] = (df['net_income'] / df['equity']) * 100

    # 5. Cash Flow Ratios
    if 'operating_cash_flow' in cols and 'capital_expenditure' in cols:
        # FCF = OCF - CapEx (CapEx is usually negative in our cleaning, or positive if extracted as absolute)
        # We adjust based on assumption: if CapEx is negative, add it. If positive, subtract it.
        # But our clean_value handles (val) as negative.
        results['Free Cash Flow'] = df['operating_cash_flow'] + df['capital_expenditure']
    
    # 6. Cash Runway (Simplified)
    # If operating cash flow is negative, how many months can they last with Current Assets?
    if 'operating_cash_flow' in cols and 'current_assets' in cols:
        def calc_runway(row):
            if row['operating_cash_flow'] < 0:
                burn_rate = abs(row['operating_cash_flow']) / 12  # monthly burn
                return row['current_assets'] / burn_rate if burn_rate > 0 else float('inf')
            return float('nan')
        
        results['Cash Runway (Months)'] = df.apply(calc_runway, axis=1)

    return pd.DataFrame(results)
