import pandas as pd
import numpy as np
from typing import Tuple, Dict, Optional

# Predefined standard column names we want in our final DataFrame
STANDARD_COLUMNS = {
    "Date": ["date", "transaction date", "transaction_date", "date of purchase", "purchase date", "timestamp", "dt"],
    "Category": ["category", "expense category", "type", "class", "group"],
    "Amount": ["amount", "cost", "price", "expense amount", "value", "spent", "charge"],
    "Payment_Method": ["payment method", "payment_method", "payment", "mode", "method", "pay mode", "pay_method", "card/cash", "type of payment"],
    "Merchant": ["merchant", "description", "merchant / description", "merchant/description", "vendor", "payee", "store", "shop", "place"],
    "Account": ["account", "wallet", "account / wallet", "account/wallet", "source", "card", "bank", "payment source"]
}

def map_columns(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, str], list]:
    """
    Intelligently maps varying column names to standard names:
    ['Date', 'Category', 'Amount', 'Payment_Method', 'Merchant', 'Account']
    
    Returns:
        Mapped DataFrame, dictionary of the mapping applied, and any missing critical columns.
    """
    column_mapping = {}
    missing_critical = []
    
    # Clean the input columns for comparison (lowercase, strip whitespace, remove underscores/dashes)
    df_cols_cleaned = {
        col.lower().replace("_", "").replace("-", "").replace(" ", "").strip(): col 
        for col in df.columns
    }
    
    # Try to find standard columns
    for std_col, variations in STANDARD_COLUMNS.items():
        matched = False
        for var in variations:
            # Clean variation for comparison
            var_cleaned = var.lower().replace("_", "").replace("-", "").replace(" ", "").strip()
            if var_cleaned in df_cols_cleaned:
                original_col = df_cols_cleaned[var_cleaned]
                column_mapping[original_col] = std_col
                matched = True
                break
        
        # If no variation matched, check for exact substring matches as a fallback
        if not matched:
            for cleaned_var, original_col in df_cols_cleaned.items():
                # E.g., if column contains "date" like "txndate" or "amt" in "totalamt"
                for var in variations:
                    var_cleaned = var.lower().replace("_", "").replace("-", "").replace(" ", "").strip()
                    if var_cleaned in cleaned_var and original_col not in column_mapping:
                        column_mapping[original_col] = std_col
                        matched = True
                        break
                if matched:
                    break
                    
        # Mark critical missing columns (Date, Category, Amount are core)
        if not matched and std_col in ["Date", "Category", "Amount"]:
            missing_critical.append(std_col)
            
    # Rename matching columns
    df_mapped = df.rename(columns=column_mapping)
    
    # Fill optional missing columns if they aren't mapped
    if "Payment_Method" not in df_mapped.columns:
        df_mapped["Payment_Method"] = "Unknown"
        column_mapping["(Assigned Default)"] = "Payment_Method"
    if "Merchant" not in df_mapped.columns:
        df_mapped["Merchant"] = "Unknown Merchant"
        column_mapping["(Assigned Default)"] = "Merchant"
    if "Account" not in df_mapped.columns:
        df_mapped["Account"] = "Default Account"
        column_mapping["(Assigned Default)"] = "Account"
        
    return df_mapped, column_mapping, missing_critical

def load_expense_data(file_path_or_buffer) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[Dict[str, str]]]:
    """
    Loads expense data from a CSV, validates it, maps columns, and cleans basic issues.
    
    Returns:
        DataFrame (standardized), Error Message (if any), and Column Mapping used.
    """
    try:
        df = pd.read_csv(file_path_or_buffer)
    except Exception as e:
        return None, f"Failed to read CSV file: {str(e)}", None
        
    if df.empty:
        return None, "The uploaded CSV file is empty.", None
        
    # Standardize columns
    df_mapped, col_map, missing_critical = map_columns(df)
    
    if missing_critical:
        err_msg = (
            f"Unable to find critical columns: {', '.join(missing_critical)}. "
            f"Please ensure your CSV file has headers representing the Date, Category, and Amount."
        )
        return None, err_msg, None
        
    # Reorder columns to a standard format and drop extra columns that weren't mapped
    standard_cols_list = ["Date", "Category", "Amount", "Payment_Method", "Merchant", "Account"]
    df_standard = df_mapped[standard_cols_list].copy()
    
    return df_standard, None, col_map
