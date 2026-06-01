import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from typing import Dict, Tuple, List

def calculate_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Computes key performance indicators (KPIs) for expense data.
    """
    if df.empty:
        return {
            "total_expense": 0.0,
            "avg_expense": 0.0,
            "max_expense": 0.0,
            "min_expense": 0.0,
            "txn_count": 0
        }
    return {
        "total_expense": float(df["Amount"].sum()),
        "avg_expense": float(df["Amount"].mean()),
        "max_expense": float(df["Amount"].max()),
        "min_expense": float(df["Amount"].min()),
        "txn_count": int(df.shape[0])
    }

def get_category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates a aggregate summary for each expense category.
    """
    if df.empty:
        return pd.DataFrame(columns=["Category", "Total_Amount", "Transaction_Count", "Average_Amount", "Percentage"])
        
    total_all = df["Amount"].sum()
    summary = df.groupby("Category")["Amount"].agg(
        Total_Amount="sum",
        Transaction_Count="count",
        Average_Amount="mean"
    ).reset_index()
    
    summary["Percentage"] = (summary["Total_Amount"] / total_all * 100).round(2)
    summary = summary.sort_values(by="Total_Amount", ascending=False).reset_index(drop=True)
    return summary

def get_payment_method_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Generates an aggregate summary of expenses by payment methods.
    """
    if df.empty:
        return pd.DataFrame(columns=["Payment_Method", "Total_Amount", "Transaction_Count", "Percentage"])
        
    total_all = df["Amount"].sum()
    summary = df.groupby("Payment_Method")["Amount"].agg(
        Total_Amount="sum",
        Transaction_Count="count"
    ).reset_index()
    
    summary["Percentage"] = (summary["Total_Amount"] / total_all * 100).round(2)
    summary = summary.sort_values(by="Total_Amount", ascending=False).reset_index(drop=True)
    return summary

def get_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extracts month-on-month expense trends.
    """
    if df.empty:
        return pd.DataFrame(columns=["Month_Year", "Total_Amount", "Transaction_Count", "Average_Amount"])
        
    # Group by Month_Year (e.g. '2026-01') which preserves chronological order
    trend = df.groupby(["Month_Year", "Year", "Month"])["Amount"].agg(
        Total_Amount="sum",
        Transaction_Count="count",
        Average_Amount="mean"
    ).reset_index()
    
    # Sort chronologically by Year and Month
    trend = trend.sort_values(by=["Year", "Month"]).reset_index(drop=True)
    return trend

def get_budget_status(df: pd.DataFrame, budget_dict: Dict[str, float]) -> pd.DataFrame:
    """
    Compares category-wise actual spending vs category budgets.
    """
    cat_summary = get_category_summary(df)
    
    # Create budget df
    budget_data = []
    for cat, budget in budget_dict.items():
        budget_data.append({"Category": cat, "Budget": float(budget)})
    budget_df = pd.DataFrame(budget_data)
    
    if cat_summary.empty:
        merged = budget_df.copy()
        merged["Actual"] = 0.0
        merged["Remaining"] = merged["Budget"]
        merged["Percent_Used"] = 0.0
        merged["Status"] = "On Track"
        return merged
        
    # Merge actual with budgets
    merged = pd.merge(budget_df, cat_summary[["Category", "Total_Amount"]], on="Category", how="outer")
    merged = merged.rename(columns={"Total_Amount": "Actual"})
    merged["Actual"] = merged["Actual"].fillna(0.0)
    merged["Budget"] = merged["Budget"].fillna(0.0) # For items that had spend but no budget
    
    # Calculations
    merged["Remaining"] = merged["Budget"] - merged["Actual"]
    merged["Percent_Used"] = np.where(
        merged["Budget"] > 0,
        (merged["Actual"] / merged["Budget"] * 100).round(2),
        np.where(merged["Actual"] > 0, 100.0, 0.0)
    )
    
    # Categorize status
    def determine_status(row):
        if row["Budget"] == 0:
            return "No Budget Set"
        elif row["Percent_Used"] > 100:
            return "Over Budget"
        elif row["Percent_Used"] >= 90:
            return "Critical (90%+)"
        else:
            return "On Track"
            
    merged["Status"] = merged.apply(determine_status, axis=1)
    merged = merged.sort_values(by="Percent_Used", ascending=False).reset_index(drop=True)
    return merged

def get_savings_estimation(df: pd.DataFrame, monthly_income: float) -> Dict[str, float]:
    """
    Estimates monthly savings based on actual spending and user-provided monthly income.
    We compute monthly averages from the historical data and subtract from income.
    """
    monthly_trend = get_monthly_trends(df)
    
    if monthly_trend.empty:
        return {
            "avg_monthly_expense": 0.0,
            "monthly_income": monthly_income,
            "est_monthly_savings": monthly_income,
            "savings_rate": 100.0 if monthly_income > 0 else 0.0
        }
        
    # Average expense across all historical months in dataset
    avg_expense = float(monthly_trend["Total_Amount"].mean())
    savings = monthly_income - avg_expense
    savings_rate = (savings / monthly_income * 100) if monthly_income > 0 else 0.0
    
    return {
        "avg_monthly_expense": round(avg_expense, 2),
        "monthly_income": round(monthly_income, 2),
        "est_monthly_savings": round(savings, 2),
        "savings_rate": round(max(-100.0, savings_rate), 2) # bound negative rate
    }

def forecast_weekly_expenses(df: pd.DataFrame, forecast_weeks: int = 4) -> Tuple[pd.DataFrame, float, float]:
    """
    Fits a simple Linear Regression model to weekly aggregated expense data
    to forecast the next N weeks of spending.
    
    Returns:
        DataFrame containing historical + forecasted weeks, 
        R-squared score of the model (accuracy indicator),
        Average forecasted weekly amount.
    """
    if df.empty or len(df["Date"].unique()) < 14:
        # Return dummy empty structures if not enough data
        return pd.DataFrame(), 0.0, 0.0
        
    df_temp = df.copy()
    df_temp["Date"] = pd.to_datetime(df_temp["Date"])
    
    # Resample to weekly start (e.g. 'W-MON')
    weekly = df_temp.set_index("Date")["Amount"].resample("W-MON").sum().reset_index()
    weekly.columns = ["Week_Start", "Total_Amount"]
    
    # Check if we have enough weeks (need at least 4 to do regression)
    if len(weekly) < 4:
        return pd.DataFrame(), 0.0, 0.0
        
    # Prepare data for training
    weekly["Week_Index"] = np.arange(len(weekly))
    
    X = weekly[["Week_Index"]].values
    y = weekly["Total_Amount"].values
    
    model = LinearRegression()
    model.fit(X, y)
    r2 = float(model.score(X, y))
    
    # Forecast
    future_indices = np.arange(len(weekly), len(weekly) + forecast_weeks)
    future_dates = [weekly["Week_Start"].max() + pd.Timedelta(weeks=int(i)) for i in range(1, forecast_weeks + 1)]
    
    predictions = model.predict(future_indices.reshape(-1, 1))
    predictions = np.clip(predictions, 0, None) # Spend can't be negative
    
    # Build results dataframe
    historical_df = pd.DataFrame({
        "Week": weekly["Week_Start"].dt.strftime("%Y-%m-%d"),
        "Amount": weekly["Total_Amount"],
        "Type": "Historical"
    })
    
    forecasted_df = pd.DataFrame({
        "Week": [d.strftime("%Y-%m-%d") for d in future_dates],
        "Amount": predictions,
        "Type": "Forecasted"
    })
    
    combined_df = pd.concat([historical_df, forecasted_df], ignore_index=True)
    avg_forecast = float(predictions.mean())
    
    return combined_df, r2, avg_forecast
