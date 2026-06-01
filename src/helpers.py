import streamlit as st
import pandas as pd
from typing import Dict

def inject_custom_css():
    """
    Injects professional CSS styles into the Streamlit app to create a gorgeous UI
    using modern fonts, glassmorphism containers, smooth gradients, and clean tables.
    """
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');
        
        /* Apply fonts globally */
        html, body, [class*="css"], .stMarkdown {
            font-family: 'Outfit', 'Inter', sans-serif !important;
        }
        
        /* App Background styling */
        .stApp {
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%) !important;
            color: #f8fafc !important;
        }
        
        /* Top Navigation Header Styling */
        header {
            background-color: transparent !important;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background: rgba(15, 23, 42, 0.9) !important;
            backdrop-filter: blur(10px) !important;
            border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        }
        
        /* Glassmorphic Container Cards */
        .glass-card {
            background: rgba(255, 255, 255, 0.03) !important;
            backdrop-filter: blur(16px) !important;
            -webkit-backdrop-filter: blur(16px) !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 16px !important;
            padding: 24px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        
        .glass-card:hover {
            border: 1px solid rgba(59, 130, 246, 0.4) !important;
            box-shadow: 0 12px 40px 0 rgba(59, 130, 246, 0.15) !important;
            transform: translateY(-2px) !important;
        }
        
        /* KPI Cards Styling */
        .kpi-container {
            display: flex;
            justify-content: space-between;
            gap: 15px;
            margin-bottom: 25px;
            flex-wrap: wrap;
        }
        
        .kpi-card {
            flex: 1;
            min-width: 180px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.04) 0%, rgba(255, 255, 255, 0.01) 100%);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }
        
        .kpi-card:hover {
            border-color: rgba(59, 130, 246, 0.3);
            transform: scale(1.02);
        }
        
        .kpi-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 4px;
        }
        
        .kpi-total::before { background: #3b82f6; }
        .kpi-avg::before { background: #10b981; }
        .kpi-max::before { background: #f59e0b; }
        .kpi-count::before { background: #8b5cf6; }
        
        .kpi-value {
            font-size: 24px;
            font-weight: 700;
            color: #ffffff;
            margin-top: 8px;
            letter-spacing: -0.5px;
        }
        
        .kpi-label {
            font-size: 13px;
            font-weight: 600;
            color: rgba(255, 255, 255, 0.6);
            text-transform: uppercase;
            letter-spacing: 0.8px;
        }
        
        /* Gradient Typography */
        .gradient-text {
            background: linear-gradient(90deg, #3b82f6 0%, #10b981 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
        }
        
        .subgradient-text {
            background: linear-gradient(90deg, #a78bfa 0%, #f472b6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 700 !important;
        }
        
        /* Tab formatting */
        .stTabs [data-baseweb="tab-list"] {
            gap: 10px;
            background-color: rgba(255, 255, 255, 0.02) !important;
            padding: 8px !important;
            border-radius: 12px !important;
            border: 1px solid rgba(255, 255, 255, 0.04) !important;
        }
        
        .stTabs [data-baseweb="tab"] {
            border-radius: 8px !important;
            color: rgba(255, 255, 255, 0.7) !important;
            padding: 10px 20px !important;
            transition: all 0.2s ease !important;
            border: none !important;
            font-weight: 600 !important;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(59, 130, 246, 0.15) !important;
            color: #3b82f6 !important;
            border: 1px solid rgba(59, 130, 246, 0.3) !important;
        }
        
        /* Hide native streamlit elements */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Buttons styling */
        .stButton>button {
            background: linear-gradient(90deg, #3b82f6 0%, #2563eb 100%) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 10px 24px !important;
            box-shadow: 0 4px 14px 0 rgba(59, 130, 246, 0.3) !important;
            transition: all 0.2s ease !important;
        }
        .stButton>button:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 20px 0 rgba(59, 130, 246, 0.4) !important;
        }
        
        /* Success/Info boxes styling */
        div[data-testid="stNotification"] {
            background-color: rgba(16, 185, 129, 0.1) !important;
            border: 1px solid rgba(16, 185, 129, 0.3) !important;
            color: #10b981 !important;
            border-radius: 10px !important;
        }
        
        </style>
        """,
        unsafe_allow_html=True
    )

def render_kpi_cards(total_expense: float, avg_expense: float, max_expense: float, txn_count: int):
    """
    Renders top KPI metric cards with professional Glassmorphism look and feel.
    """
    st.markdown(
        f"""
        <div class="kpi-container">
            <div class="kpi-card kpi-total">
                <div class="kpi-label">Total Spent</div>
                <div class="kpi-value">${total_expense:,.2f}</div>
            </div>
            <div class="kpi-card kpi-avg">
                <div class="kpi-label">Average Trans.</div>
                <div class="kpi-value">${avg_expense:,.2f}</div>
            </div>
            <div class="kpi-card kpi-max">
                <div class="kpi-label">Largest Expense</div>
                <div class="kpi-value">${max_expense:,.2f}</div>
            </div>
            <div class="kpi-card kpi-count">
                <div class="kpi-label">Transactions</div>
                <div class="kpi-value">{txn_count}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def generate_text_report(kpis: Dict[str, float], 
                         cat_summary: pd.DataFrame, 
                         budget_summary: pd.DataFrame, 
                         savings_est: Dict[str, float]) -> str:
    """
    Generates a professional Markdown-formatted text report for downloading.
    """
    report = []
    report.append("==========================================================================")
    report.append("                   PERSONAL EXPENSE ANALYTICS SUMMARY")
    report.append("                       Internship Project Report")
    report.append("==========================================================================\n")
    
    report.append("1. EXECUTIVE SUMMARY METRICS")
    report.append("--------------------------------------------------------------------------")
    report.append(f"  * Total Historical Expense   : ${kpis['total_expense']:,.2f}")
    report.append(f"  * Average Expense Amount     : ${kpis['avg_expense']:,.2f}")
    report.append(f"  * Highest Registered Expense : ${kpis['max_expense']:,.2f}")
    report.append(f"  * Lowest Registered Expense  : ${kpis['min_expense']:,.2f}")
    report.append(f"  * Total Transactions Logged  : {kpis['txn_count']}")
    report.append("")
    
    report.append("2. BUDGET & SAVINGS ANALYSIS")
    report.append("--------------------------------------------------------------------------")
    report.append(f"  * User Input Monthly Income  : ${savings_est['monthly_income']:,.2f}")
    report.append(f"  * Average Monthly Expenses   : ${savings_est['avg_monthly_expense']:,.2f}")
    report.append(f"  * Estimated Monthly Savings  : ${savings_est['est_monthly_savings']:,.2f}")
    report.append(f"  * Projected Savings Rate    : {savings_est['savings_rate']}%")
    report.append("")
    
    report.append("3. TOP CATEGORIES OF EXPENDITURE")
    report.append("--------------------------------------------------------------------------")
    if not cat_summary.empty:
        # Top 5
        top_cats = cat_summary.head(5)
        for idx, row in top_cats.iterrows():
            report.append(f"  {idx+1}. {row['Category']:<20} | Total Spent: ${row['Total_Amount']:>9,.2f} ({row['Percentage']}% of total)")
    else:
        report.append("  No category data available.")
    report.append("")
        
    report.append("4. BUDGET VARIANCE STATUS BY CATEGORY")
    report.append("--------------------------------------------------------------------------")
    if not budget_summary.empty:
        report.append(f"  {'Category':<20} | {'Budget ($)':<12} | {'Actual ($)':<12} | {'Percent Used':<12} | {'Status':<15}")
        report.append("  " + "-"*75)
        for _, row in budget_summary.iterrows():
            report.append(f"  {row['Category']:<20} | {row['Budget']:>12,.2f} | {row['Actual']:>12,.2f} | {row['Percent_Used']:>11}% | {row['Status']:<15}")
    else:
        report.append("  No budget parameters were specified.")
    report.append("")
    
    report.append("==========================================================================")
    report.append("Report generated automatically by Personal Expense Analytics Dashboard")
    report.append("==========================================================================")
    
    return "\n".join(report)
