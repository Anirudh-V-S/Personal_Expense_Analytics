import pandas as pd
import numpy as np
from typing import Tuple

def preprocess_expenses(df: pd.DataFrame) -> Tuple[pd.DataFrame, list]:
    """
    Cleans expense columns, handles data types, missing values, and extracts rich time-based fields.
    
    Returns:
        Preprocessed DataFrame and a list of warnings (if any data cleaning anomalies occurred).
    """
    df_clean = df.copy()
    warnings = []
    
    # 1. Clean Amount Column
    if df_clean['Amount'].dtype == object:
        # Strip currency symbols and commas if present
        df_clean['Amount'] = (
            df_clean['Amount']
            .astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
            .str.strip()
        )
    
    df_clean['Amount'] = pd.to_numeric(df_clean['Amount'], errors='coerce')
    
    # Check for NaNs in Amount
    nan_amounts = df_clean['Amount'].isna().sum()
    if nan_amounts > 0:
        df_clean = df_clean.dropna(subset=['Amount'])
        warnings.append(f"Removed {nan_amounts} row(s) with invalid or missing expense amounts.")
        
    # Check for negative amounts
    negative_amounts = (df_clean['Amount'] < 0).sum()
    if negative_amounts > 0:
        df_clean['Amount'] = df_clean['Amount'].abs()
        warnings.append(f"Converted {negative_amounts} negative expense amount(s) to absolute values.")
        
    # Remove zero amount transactions
    zero_amounts = (df_clean['Amount'] == 0).sum()
    if zero_amounts > 0:
        df_clean = df_clean[df_clean['Amount'] > 0]
        warnings.append(f"Filtered out {zero_amounts} row(s) with zero expense amount.")

    # 2. Clean Date Column
    df_clean['Date'] = pd.to_datetime(df_clean['Date'], errors='coerce')
    
    # Check for NaNs in Date
    nan_dates = df_clean['Date'].isna().sum()
    if nan_dates > 0:
        df_clean = df_clean.dropna(subset=['Date'])
        warnings.append(f"Removed {nan_dates} row(s) with invalid or unparsable dates.")
        
    df_clean = df_clean.sort_values(by='Date').reset_index(drop=True)
    
    # Extract rich time features
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Month_Name'] = df_clean['Date'].dt.strftime('%B')
    df_clean['Month_Year'] = df_clean['Date'].dt.to_period('M').astype(str)
    df_clean['Day'] = df_clean['Date'].dt.day
    df_clean['Day_Of_Week'] = df_clean['Date'].dt.strftime('%A')
    df_clean['Is_Weekend'] = df_clean['Date'].dt.weekday.isin([5, 6])
    
    # 3. Clean Text Columns
    text_cols = ['Category', 'Payment_Method', 'Merchant', 'Account']
    for col in text_cols:
        df_clean[col] = df_clean[col].astype(str).str.strip()
        # Handle empty/missing categories or payment methods
        df_clean[col] = df_clean[col].replace(['nan', 'None', '', 'NULL'], np.nan)
        
        # Fill default values
        default_val = "Unknown"
        if col == "Category":
            default_val = "Miscellaneous"
        elif col == "Payment_Method":
            default_val = "Cash"
        elif col == "Merchant":
            default_val = "Unknown Merchant"
        elif col == "Account":
            default_val = "Default Account"
            
        df_clean[col] = df_clean[col].fillna(default_val)
        
        # Standardize capitalization
        df_clean[col] = df_clean[col].str.title()
        
    return df_clean, warnings
