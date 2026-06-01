import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Import local modules
from src.data_loader import load_expense_data
from src.preprocessing import preprocess_expenses
from src.analytics import (
    calculate_kpis,
    get_category_summary,
    get_payment_method_summary,
    get_monthly_trends,
    get_budget_status,
    get_savings_estimation,
    forecast_weekly_expenses
)
from src.visualizations import (
    plot_spending_over_time,
    plot_category_bar,
    plot_payment_methods_donut,
    plot_category_treemap,
    plot_monthly_trend_comparison,
    plot_weekly_heatmap,
    plot_budget_vs_actual,
    plot_forecast
)
from src.helpers import inject_custom_css, render_kpi_cards, generate_text_report

# 1. Page Configuration
st.set_page_config(
    page_title="Personal Expense Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Theme
inject_custom_css()

# 3. Header Section
st.markdown("""
    <div style='text-align: center; margin-bottom: 30px;'>
        <h1 class='gradient-text' style='font-size: 3rem; margin-bottom: 5px;'>Personal Expense Analytics Dashboard</h1>
        <p style='color: rgba(255, 255, 255, 0.7); font-size: 1.15rem; max-width: 800px; margin: 0 auto;'>
            Transform raw financial logs into interactive visual intelligence. Explore spending behavior, 
            track budget thresholds, perform advanced forecast modeling, and export publication-ready reports.
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. Sidebar Configuration
st.sidebar.markdown("""
    <div style='text-align: center; margin-bottom: 20px;'>
        <h2 style='font-size: 1.4rem; color: #3b82f6;'>⚙️ Dashboard Controls</h2>
    </div>
""", unsafe_allow_html=True)

# A. Data Source Selector
st.sidebar.subheader("📂 1. Ingest Expense Data")
data_source = st.sidebar.radio("Data Ingestion Mode", ["Use Polished Sample Dataset", "Upload Custom CSV Log"])

raw_df = None
column_mapping = None
error_msg = None

if data_source == "Upload Custom CSV Log":
    uploaded_file = st.sidebar.file_uploader("Select CSV File", type=["csv"])
    if uploaded_file is not None:
        raw_df, error_msg, column_mapping = load_expense_data(uploaded_file)
        if error_msg:
            st.sidebar.error(error_msg)
    else:
        st.sidebar.info("Waiting for file upload. Using sample dataset in the meantime.")
        # Fallback to sample
        raw_df, error_msg, column_mapping = load_expense_data("data/sample_expenses.csv")
else:
    # Load default sample
    raw_df, error_msg, column_mapping = load_expense_data("data/sample_expenses.csv")
    if error_msg:
        st.error(f"Sample data load error: {error_msg}")

# Only proceed if data loaded successfully
if raw_df is not None:
    # Preprocess
    df, preproc_warnings = preprocess_expenses(raw_df)
    
    # Display preprocessing warnings if any in sidebar
    if preproc_warnings:
        with st.sidebar.expander("⚠️ Data Cleaning Logs", expanded=False):
            for warn in preproc_warnings:
                st.write(f"- {warn}")

    # B. Filters Section
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔍 2. Filter Operations")
    
    # Date Range Filter
    min_date = df["Date"].min().to_pydatetime()
    max_date = df["Date"].max().to_pydatetime()
    
    start_date, end_date = st.sidebar.slider(
        "Date Range Selection",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    
    # Category Multi-Select
    unique_categories = sorted(df["Category"].unique())
    selected_categories = st.sidebar.multiselect(
        "Select Expense Categories",
        options=unique_categories,
        default=unique_categories
    )
    
    # Payment Method Multi-Select
    unique_payments = sorted(df["Payment_Method"].unique())
    selected_payments = st.sidebar.multiselect(
        "Select Payment Methods",
        options=unique_payments,
        default=unique_payments
    )
    
    # Apply filters to Data
    filtered_df = df[
        (df["Date"] >= pd.to_datetime(start_date)) & 
        (df["Date"] <= pd.to_datetime(end_date)) & 
        (df["Category"].isin(selected_categories)) & 
        (df["Payment_Method"].isin(selected_payments))
    ]

    # C. Financial Parameters
    st.sidebar.markdown("---")
    st.sidebar.subheader("💰 3. Financial Inputs")
    
    monthly_income = st.sidebar.number_input(
        "Estimated Monthly Income ($)",
        min_value=0.0,
        value=5000.0,
        step=100.0
    )
    
    # Dynamic Budget Setup in Sidebar
    st.sidebar.subheader("🎯 4. Budget Configurations")
    with st.sidebar.expander("Configure Category Budgets", expanded=False):
        budget_dict = {}
        # Pre-populate defaults for common categories
        default_budgets = {
            "Rent & Utilities": 1500.0,
            "Groceries": 500.0,
            "Dining Out": 250.0,
            "Transport": 200.0,
            "Entertainment": 150.0,
            "Shopping": 300.0,
            "Healthcare": 100.0,
            "Subscriptions": 100.0,
            "Miscellaneous": 100.0
        }
        
        for cat in unique_categories:
            default_val = default_budgets.get(cat, 100.0)
            budget_dict[cat] = st.number_input(
                f"{cat} Limit ($)",
                min_value=0.0,
                value=float(default_val),
                step=50.0,
                key=f"budget_{cat}"
            )
            
    # Sidebar footer
    st.sidebar.markdown("""
        <div style='text-align: center; margin-top: 30px; font-size: 0.8rem; color: rgba(255, 255, 255, 0.4);'>
            CodTech IT Solutions Internship<br>
            <b>Data Analytics Portfolio Project</b>
        </div>
    """, unsafe_allow_html=True)

    # 5. Core Execution & UI Tabs Assembly
    if filtered_df.empty:
        st.warning("⚠️ No records match the active combination of filter rules. Adjust date range, payment types, or category selections in the sidebar.")
    else:
        # Calculate primary analytics
        kpis = calculate_kpis(filtered_df)
        cat_summary = get_category_summary(filtered_df)
        pm_summary = get_payment_method_summary(filtered_df)
        monthly_trends = get_monthly_trends(filtered_df)
        budget_summary = get_budget_status(filtered_df, budget_dict)
        savings_est = get_savings_estimation(filtered_df, monthly_income)

        # High-Fidelity App Tabs
        tabs = st.tabs([
            "📊 Executive Overview", 
            "🏷️ Category Analysis", 
            "⏰ Time-Series Patterns", 
            "🎯 Budget & Savings Tracker",
            "📈 Forecast Modeling",
            "📁 Raw Financial Log"
        ])
        
        # --------------------- TAB 1: EXECUTIVE OVERVIEW ---------------------
        with tabs[0]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Executive Financial Summary</h3>", unsafe_allow_html=True)
            
            # KPI Cards
            render_kpi_cards(
                kpis["total_expense"],
                kpis["avg_expense"],
                kpis["max_expense"],
                kpis["txn_count"]
            )
            
            # Budget overspending toast/alerts
            over_budget_cats = budget_summary[budget_summary["Status"] == "Over Budget"]["Category"].tolist()
            if over_budget_cats:
                st.error(f"🚨 **Budget Alert**: You have exceeded your budget limits in these categories: **{', '.join(over_budget_cats)}**!")
            elif budget_summary[budget_summary["Status"] == "Critical (90%+)"]["Category"].tolist():
                crit_cats = budget_summary[budget_summary["Status"] == "Critical (90%+)"]["Category"].tolist()
                st.warning(f"⚠️ **Attention**: You are close to exceeding 90% of budget limit in: **{', '.join(crit_cats)}**.")
            
            # Split Layout
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_spending_over_time(filtered_df), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_payment_methods_donut(pm_summary), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Treemap category distribution
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.plotly_chart(plot_category_treemap(filtered_df), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --------------------- TAB 2: CATEGORY ANALYSIS ---------------------
        with tabs[1]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Expense Category Breakdown</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_category_bar(cat_summary), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_weekly_heatmap(filtered_df), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Category table
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Category Expenditure Variance Table")
            formatted_cat = cat_summary.copy()
            formatted_cat["Total_Amount"] = formatted_cat["Total_Amount"].apply(lambda x: f"${x:,.2f}")
            formatted_cat["Average_Amount"] = formatted_cat["Average_Amount"].apply(lambda x: f"${x:,.2f}")
            formatted_cat["Percentage"] = formatted_cat["Percentage"].apply(lambda x: f"{x}%")
            
            st.dataframe(formatted_cat, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --------------------- TAB 3: TIME-SERIES PATTERNS ---------------------
        with tabs[2]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Chronological Spending Habits</h3>", unsafe_allow_html=True)
            
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_monthly_trend_comparison(monthly_trends), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col2:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.markdown("<h4>Weekend vs. Weekday Patterns</h4>", unsafe_allow_html=True)
                
                # Weekend vs Weekday analysis
                week_group = filtered_df.groupby("Is_Weekend")["Amount"].agg(
                    Total="sum", Avg="mean", Count="count"
                ).reset_index()
                week_group["Is_Weekend"] = week_group["Is_Weekend"].map({True: "Weekend (Sat/Sun)", False: "Weekday (Mon-Fri)"})
                
                # Format
                for idx, row in week_group.iterrows():
                    st.metric(
                        label=f"{row['Is_Weekend']} Expense Share",
                        value=f"${row['Total']:,.2f}",
                        delta=f"{row['Count']} transactions (Avg: ${row['Avg']:.2f})"
                    )
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Additional Time breakdown cards
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Transactions Breakdown by Day of Week")
            day_group = filtered_df.groupby("Day_Of_Week")["Amount"].agg(
                Total_Spent="sum", Avg_Spent="mean", Transaction_Count="count"
            ).reindex(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]).dropna().reset_index()
            
            # Format
            day_group["Total_Spent"] = day_group["Total_Spent"].apply(lambda x: f"${x:,.2f}")
            day_group["Avg_Spent"] = day_group["Avg_Spent"].apply(lambda x: f"${x:,.2f}")
            st.table(day_group)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --------------------- TAB 4: BUDGET & SAVINGS TRACKER ---------------------
        with tabs[3]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Budget Optimization & Personal Savings Estimator</h3>", unsafe_allow_html=True)
            
            # Savings Metrics
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            col_s1, col_s2, col_s3, col_s4 = st.columns(4)
            with col_s1:
                st.metric("Expected Monthly Income", f"${savings_est['monthly_income']:,.2f}")
            with col_s2:
                st.metric("Avg Monthly Expense", f"${savings_est['avg_monthly_expense']:,.2f}")
            with col_s3:
                st.metric("Estimated Net Savings", f"${savings_est['est_monthly_savings']:,.2f}")
            with col_s4:
                st.metric("Projected Savings Rate", f"{savings_est['savings_rate']}%")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Budget VS Actual Graphic
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.plotly_chart(plot_budget_vs_actual(budget_summary), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Detailed budget table
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("Budget Allocation & Limit Variance Sheet")
            
            # Color row backgrounds depending on budget status
            formatted_budget = budget_summary.copy()
            formatted_budget["Budget"] = formatted_budget["Budget"].apply(lambda x: f"${x:,.2f}")
            formatted_budget["Actual"] = formatted_budget["Actual"].apply(lambda x: f"${x:,.2f}")
            formatted_budget["Remaining"] = formatted_budget["Remaining"].apply(lambda x: f"${x:,.2f}")
            formatted_budget["Percent_Used"] = formatted_budget["Percent_Used"].apply(lambda x: f"{x}%")
            
            st.dataframe(formatted_budget, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # --------------------- TAB 5: FORECAST MODELING ---------------------
        with tabs[4]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Weekly Expenses Linear Trend Forecasting</h3>", unsafe_allow_html=True)
            st.markdown("""
                This tab utilizes an **Ordinary Least Squares (OLS) Linear Regression model** to predict expenditure trends. 
                By grouping financial logs into weekly buckets, the model fits a trend line ($y = mx + c$) 
                to project your expected spending patterns for the next 4 weeks.
            """)
            
            # Fit and forecast model
            forecast_df, r2_score, avg_forecast_val = forecast_weekly_expenses(filtered_df)
            
            if forecast_df.empty:
                st.warning("⚠️ High-resolution linear modeling requires at least **2 weeks** of financial date logs in your data selection. Expand your date slider selection.")
            else:
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.plotly_chart(plot_forecast(forecast_df, r2_score), use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
                # Model evaluation metrics & observations
                st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
                st.subheader("Linear Regression Model Interpretation")
                col_m1, col_m2 = st.columns(2)
                
                # Determine R2 description
                if r2_score > 0.7:
                    fit_desc = "Strong Linear Relationship (highly predictive of repeating habits)"
                elif r2_score > 0.4:
                    fit_desc = "Moderate Linear Trend (spending has visible patterns but contains noise)"
                else:
                    fit_desc = "Low Linear Correlation (spending fluctuates significantly week-to-week)"
                    
                with col_m1:
                    st.metric("Model Goodness of Fit (R² Score)", f"{r2_score:.4f}", help="Indicates the proportion of variance in expenditure explained by time.")
                    st.write(f"**Interpretation**: {fit_desc}")
                    
                with col_m2:
                    st.metric("Average Weekly Forecasted Spend", f"${avg_forecast_val:,.2f}", help="Predicted weekly run rate for the next month.")
                    monthly_projected = avg_forecast_val * 4
                    st.write(f"**Projected Monthly Spend Rate**: ${monthly_projected:,.2f}")
                st.markdown("</div>", unsafe_allow_html=True)
                
        # --------------------- TAB 6: RAW FINANCIAL LOG ---------------------
        with tabs[5]:
            st.markdown("<h3 style='color: #3b82f6; margin-bottom: 20px;'>Cleaned Ledger & Data Exporters</h3>", unsafe_allow_html=True)
            
            # Search & Filter controls
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            search_query = st.text_input("🔍 Search Merchant or Category Description", "")
            
            display_df = filtered_df.copy()
            if search_query:
                display_df = display_df[
                    display_df["Merchant"].str.contains(search_query, case=False, na=False) |
                    display_df["Category"].str.contains(search_query, case=False, na=False)
                ]
                
            st.subheader(f"Ledger Logs ({len(display_df)} records)")
            st.dataframe(display_df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Data Export Utilities
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.subheader("📦 Exporter Operations & Project Submission Utilities")
            
            col_ex1, col_ex2 = st.columns(2)
            
            with col_ex1:
                st.markdown("<h4>1. Export Ledger to CSV File</h4>", unsafe_allow_html=True)
                st.write("Extract your fully cleaned, standardized, and filtered transaction logs as a standard CSV format.")
                
                # Convert DF to CSV
                csv_data = filtered_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Cleaned CSV Ledger",
                    data=csv_data,
                    file_name="cleaned_personal_expenses.csv",
                    mime="text/csv"
                )
                
            with col_ex2:
                st.markdown("<h4>2. Export Analytical Summary Report</h4>", unsafe_allow_html=True)
                st.write("Generate a formatted text summary report including core KPI performance, category shares, budget statuses, and savings estimation.")
                
                report_txt = generate_text_report(kpis, cat_summary, budget_summary, savings_est)
                st.download_button(
                    label="📝 Download Summary Report (.txt)",
                    data=report_txt,
                    file_name="expense_analytics_report.txt",
                    mime="text/plain"
                )
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.error("❌ Failed to resolve data inputs. Please check that you provided a valid CSV containing structural column configurations.")
