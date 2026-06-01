import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_sample_data(output_path: str):
    np.random.seed(42)
    categories = [
        "Groceries", "Dining Out", "Transport", "Rent & Utilities", 
        "Entertainment", "Shopping", "Healthcare", "Subscriptions", "Miscellaneous"
    ]
    payment_methods = ["Credit Card", "Debit Card", "UPI / Wallet", "Cash"]
    
    merchants = {
        "Groceries": ["Whole Foods", "Walmart", "Target", "Trader Joe's", "Kroger"],
        "Dining Out": ["Starbucks", "McDonald's", "Local Pizzeria", "Subway", "Olive Garden", "Chipotle"],
        "Transport": ["Uber", "Lyft", "Shell Gas Station", "ExxonMobil", "Subway Transit"],
        "Rent & Utilities": ["Landlord Inc.", "Electric Utility", "Water & Sewage Corp", "Comcast Cable"],
        "Entertainment": ["Netflix", "Spotify", "AMC Theatres", "Steam Games", "Concert Venue"],
        "Shopping": ["Amazon", "H&M", "Zara", "Nike Store", "Apple Store", "Target"],
        "Healthcare": ["CVS Pharmacy", "Walgreens", "City Dental", "Family Medical Clinic"],
        "Subscriptions": ["Adobe Creative Cloud", "Gym Membership", "Amazon Prime", "Github Copilot"],
        "Miscellaneous": ["Local Corner Store", "Laundromat", "Post Office", "Parking Meter"]
    }
    
    # Let's generate data over the last 180 days
    start_date = datetime.now() - timedelta(days=180)
    data = []
    
    # We want to simulate about 150-200 rows of transactions
    # Rent is paid on the 1st of every month
    current_date = start_date
    while current_date <= datetime.now():
        # Rent on 1st
        if current_date.day == 1:
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Rent & Utilities",
                "Amount": round(float(np.random.normal(1200, 50)), 2),
                "Payment_Method": "Debit Card",
                "Merchant / Description": "Landlord Inc.",
                "Account / Wallet": "Primary Checking"
            })
        
        # Utilities on 5th
        if current_date.day == 5:
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Rent & Utilities",
                "Amount": round(float(np.random.normal(150, 15)), 2),
                "Payment_Method": "UPI / Wallet",
                "Merchant / Description": "Electric Utility",
                "Account / Wallet": "Savings Account"
            })
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Rent & Utilities",
                "Amount": round(float(np.random.normal(60, 5)), 2),
                "Payment_Method": "UPI / Wallet",
                "Merchant / Description": "Water & Sewage Corp",
                "Account / Wallet": "Primary Checking"
            })
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Rent & Utilities",
                "Amount": round(float(np.random.normal(85, 2)), 2),
                "Payment_Method": "Credit Card",
                "Merchant / Description": "Comcast Cable",
                "Account / Wallet": "Credit Card"
            })

        # Regular monthly subscriptions
        if current_date.day == 10:
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Subscriptions",
                "Amount": 15.49,
                "Payment_Method": "Credit Card",
                "Merchant / Description": "Netflix",
                "Account / Wallet": "Credit Card"
            })
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Subscriptions",
                "Amount": 10.99,
                "Payment_Method": "Credit Card",
                "Merchant / Description": "Spotify",
                "Account / Wallet": "Credit Card"
            })
        
        if current_date.day == 15:
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": "Subscriptions",
                "Amount": 49.99,
                "Payment_Method": "Credit Card",
                "Merchant / Description": "Gym Membership",
                "Account / Wallet": "Credit Card"
            })

        # Other daily transactions (random probability based on day of week)
        # Weekends have higher dining out and shopping expenses
        is_weekend = current_date.weekday() >= 5
        num_transactions = np.random.choice([0, 1, 2, 3], p=[0.2, 0.4, 0.3, 0.1] if not is_weekend else [0.1, 0.3, 0.4, 0.2])
        
        for _ in range(num_transactions):
            if is_weekend:
                cat = np.random.choice(categories, p=[0.15, 0.25, 0.1, 0.0, 0.20, 0.20, 0.02, 0.0, 0.08])
            else:
                cat = np.random.choice(categories, p=[0.25, 0.15, 0.2, 0.0, 0.08, 0.10, 0.05, 0.02, 0.15])
            
            # Rent and Subscriptions are already handled deterministically
            if cat in ["Rent & Utilities", "Subscriptions"]:
                continue
                
            merchant = np.random.choice(merchants[cat])
            
            # Select realistic amounts
            if cat == "Groceries":
                amt = round(float(np.random.exponential(45) + 10), 2)
            elif cat == "Dining Out":
                amt = round(float(np.random.exponential(25) + 8), 2)
            elif cat == "Transport":
                amt = round(float(np.random.normal(15, 5) if "Gas" in merchant else np.random.exponential(12) + 5), 2)
            elif cat == "Entertainment":
                amt = round(float(np.random.exponential(20) + 12), 2)
            elif cat == "Shopping":
                amt = round(float(np.random.exponential(75) + 15), 2)
            elif cat == "Healthcare":
                amt = round(float(np.random.normal(50, 25)), 2)
            else:  # Miscellaneous
                amt = round(float(np.random.exponential(10) + 2), 2)
                
            # Restrict amounts to positive values
            amt = max(1.5, amt)
            
            pay_m = np.random.choice(payment_methods, p=[0.45, 0.25, 0.20, 0.10])
            acc = "Credit Card" if pay_m == "Credit Card" else ("Primary Checking" if pay_m == "Debit Card" else ("Savings Account" if pay_m == "UPI / Wallet" else "Cash"))
            
            data.append({
                "Date": current_date.strftime("%Y-%m-%d"),
                "Category": cat,
                "Amount": amt,
                "Payment_Method": pay_m,
                "Merchant / Description": merchant,
                "Account / Wallet": acc
            })
            
        current_date += timedelta(days=1)
        
    df = pd.DataFrame(data)
    # Shuffle slightly to make it look like a log file (except dates should be chronological)
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values(by='Date').reset_index(drop=True)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Sample data generated successfully at {output_path} with {len(df)} rows.")

if __name__ == "__main__":
    generate_sample_data("d:/CodTEchIT_INTERN/Personal_Expense_Analytics/data/sample_expenses.csv")
