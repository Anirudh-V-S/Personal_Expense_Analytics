import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Optional

# Premium color scheme
COLOR_PALETTE = {
    "primary": "#3b82f6",     # Blue
    "secondary": "#10b981",   # Emerald Teal
    "warning": "#f59e0b",     # Amber
    "danger": "#f43f5e",      # Rose Coral
    "purple": "#8b5cf6",      # Violet
    "pink": "#ec4899",        # Pink
    "neutral_dark": "#1e293b", # Slate Dark
    "neutral_light": "#f8fafc",# Slate Light
    "colors_list": ["#3b82f6", "#10b981", "#8b5cf6", "#f59e0b", "#f43f5e", "#ec4899", "#14b8a6", "#6366f1", "#f97316"]
}

def apply_chart_theme(fig):
    """
    Applies custom styling to a Plotly figure to make it look premium and modern:
    - Transparent backgrounds
    - Outfitted typography
    - Soft grids
    - Sleek hover labels
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Outfit, Inter, sans-serif", size=12, color="#f8fafc" if True else "#1e293b"),
        margin=dict(l=40, r=40, t=50, b=40),
        hoverlabel=dict(
            bgcolor="#0f172a",
            font_size=13,
            font_family="Outfit, Inter, sans-serif",
            font_color="#f8fafc"
        )
    )
    
    # Update axes styling if they exist
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.15)",
        tickfont=dict(color="rgba(255,255,255,0.7)")
    )
    fig.update_yaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.06)",
        linecolor="rgba(255,255,255,0.15)",
        tickfont=dict(color="rgba(255,255,255,0.7)")
    )
    return fig

def plot_spending_over_time(df: pd.DataFrame) -> go.Figure:
    """
    Plots an interactive line/area chart showing accumulated daily spending.
    """
    daily = df.groupby("Date")["Amount"].sum().reset_index()
    
    # 7-day rolling average to smooth out fluctuations
    daily["7-Day Moving Avg"] = daily["Amount"].rolling(window=7, min_periods=1).mean()
    
    fig = go.Figure()
    
    # Area for Daily Spend
    fig.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily["Amount"],
        mode="lines",
        name="Daily Amount",
        line=dict(color="rgba(59, 130, 246, 0.4)", width=1.5),
        fill="tozeroy",
        fillcolor="rgba(59, 130, 246, 0.08)"
    ))
    
    # Line for Moving Avg
    fig.add_trace(go.Scatter(
        x=daily["Date"],
        y=daily["7-Day Moving Avg"],
        mode="lines",
        name="7-Day Avg Trend",
        line=dict(color=COLOR_PALETTE["primary"], width=3)
    ))
    
    fig.update_layout(
        title="<b>Spending Over Time Trend</b>",
        xaxis_title="Transaction Date",
        yaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return apply_chart_theme(fig)

def plot_category_bar(df_summary: pd.DataFrame) -> go.Figure:
    """
    Plots horizontal bar chart of categories, highlighting the highest one.
    """
    fig = px.bar(
        df_summary,
        x="Total_Amount",
        y="Category",
        text="Total_Amount",
        orientation="h",
        color="Total_Amount",
        color_continuous_scale=[[0, "rgba(59,130,246,0.3)"], [1, COLOR_PALETTE["primary"]]],
        labels={"Total_Amount": "Total Spent ($)", "Category": "Category"}
    )
    
    fig.update_traces(
        texttemplate="$%{text:,.2f}",
        textposition="outside",
        cliponaxis=False,
        marker_line_color="rgba(255,255,255,0.1)",
        marker_line_width=1
    )
    
    fig.update_layout(
        title="<b>Total Expenses by Category</b>",
        coloraxis_showscale=False,
        yaxis=dict(autorange="reversed")
    )
    
    return apply_chart_theme(fig)

def plot_payment_methods_donut(df_summary: pd.DataFrame) -> go.Figure:
    """
    Plots a donut chart of payment methods.
    """
    fig = px.pie(
        df_summary,
        values="Total_Amount",
        names="Payment_Method",
        hole=0.55,
        color_discrete_sequence=COLOR_PALETTE["colors_list"]
    )
    
    fig.update_traces(
        textinfo="percent+label",
        hovertemplate="<b>%{label}</b><br>Spent: $%{value:,.2f}<br>Percentage: %{percent}",
        marker=dict(line=dict(color="rgba(15,23,42,1)", width=2))
    )
    
    fig.update_layout(
        title="<b>Payment Method Distribution</b>",
        showlegend=False
    )
    
    return apply_chart_theme(fig)

def plot_category_treemap(df: pd.DataFrame) -> go.Figure:
    """
    Plots a hierarchical Treemap for deep category/merchant layout.
    """
    # Group by category & merchant
    group = df.groupby(["Category", "Merchant"])["Amount"].sum().reset_index()
    
    fig = px.treemap(
        group,
        path=["Category", "Merchant"],
        values="Amount",
        color="Amount",
        color_continuous_scale="Viridis",
        color_continuous_midpoint=np.average(group['Amount'], weights=group['Amount'])
    )
    
    fig.update_layout(
        title="<b>Hierarchical Category & Merchant Share</b>",
        coloraxis_showscale=False
    )
    
    return apply_chart_theme(fig)

def plot_monthly_trend_comparison(df_monthly: pd.DataFrame) -> go.Figure:
    """
    Plots side-by-side or stacked trend analysis of monthly averages.
    """
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=df_monthly["Month_Year"],
        y=df_monthly["Total_Amount"],
        name="Total Spend",
        marker_color="rgba(16, 185, 129, 0.75)",
        marker_line_color=COLOR_PALETTE["secondary"],
        marker_line_width=1.5
    ))
    
    fig.add_trace(go.Scatter(
        x=df_monthly["Month_Year"],
        y=df_monthly["Average_Amount"] * 10,  # Scaled up for visual harmony on twin axis
        name="Avg Transaction (x10)",
        mode="lines+markers",
        line=dict(color=COLOR_PALETTE["warning"], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title="<b>Monthly Spending Trends</b>",
        xaxis_title="Month",
        yaxis_title="Total Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return apply_chart_theme(fig)

def plot_weekly_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Plots an interactive heat map showing Day of Week vs Expense Category.
    """
    if df.empty:
        return go.Figure()
        
    pivot = df.pivot_table(
        index="Day_Of_Week",
        columns="Category",
        values="Amount",
        aggfunc="sum"
    ).fillna(0.0)
    
    # Reorder weekdays chronologically
    days_ordered = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    pivot = pivot.reindex([d for d in days_ordered if d in pivot.index])
    
    fig = px.imshow(
        pivot,
        labels=dict(x="Expense Category", y="Day of Week", color="Total Spend ($)"),
        x=pivot.columns,
        y=pivot.index,
        color_continuous_scale="Blues"
    )
    
    fig.update_layout(
        title="<b>Spending Activity Heatmap (Days vs. Category)</b>",
        xaxis=dict(tickangle=45),
        coloraxis_showscale=True
    )
    
    return apply_chart_theme(fig)

def plot_budget_vs_actual(df_budget: pd.DataFrame) -> go.Figure:
    """
    Plots a dual horizontal bar chart comparing Budgets vs. Actual spending.
    """
    # Sort by percent used
    df_sorted = df_budget.sort_values(by="Budget", ascending=True)
    
    fig = go.Figure()
    
    # Add Budget Bars
    fig.add_trace(go.Bar(
        y=df_sorted["Category"],
        x=df_sorted["Budget"],
        name="Budget Limit",
        orientation="h",
        marker_color="rgba(255, 255, 255, 0.15)",
        marker_line_color="rgba(255, 255, 255, 0.4)",
        marker_line_width=1
    ))
    
    # Determine color of actual spending based on status
    colors = [
        COLOR_PALETTE["danger"] if row["Status"] == "Over Budget"
        else (COLOR_PALETTE["warning"] if row["Status"] == "Critical (90%+)" else COLOR_PALETTE["secondary"])
        for _, row in df_sorted.iterrows()
    ]
    
    # Add Actual Bars
    fig.add_trace(go.Bar(
        y=df_sorted["Category"],
        x=df_sorted["Actual"],
        name="Actual Spend",
        orientation="h",
        marker_color=colors,
        marker_line_color=colors,
        marker_line_width=1
    ))
    
    fig.update_layout(
        title="<b>Actual Spend vs. Budget Limits</b>",
        barmode="overlay",
        xaxis_title="Amount ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    # Adjust bar widths slightly so they overlay cleanly
    fig.data[0].width = 0.55
    fig.data[1].width = 0.35
    
    return apply_chart_theme(fig)

def plot_forecast(df_forecast: pd.DataFrame, r2: float) -> go.Figure:
    """
    Plots the forecast trend highlighting the historical and future prediction boundaries.
    """
    fig = go.Figure()
    
    hist = df_forecast[df_forecast["Type"] == "Historical"]
    fore = df_forecast[df_forecast["Type"] == "Forecasted"]
    
    # Historical spending line
    fig.add_trace(go.Scatter(
        x=hist["Week"],
        y=hist["Amount"],
        mode="lines+markers",
        name="Historical Spend",
        line=dict(color=COLOR_PALETTE["primary"], width=3),
        marker=dict(size=6)
    ))
    
    # Connecting step (historical last to forecast first)
    connect_df = pd.concat([hist.tail(1), fore.head(1)])
    fig.add_trace(go.Scatter(
        x=connect_df["Week"],
        y=connect_df["Amount"],
        mode="lines",
        name="Forecast Boundary",
        showlegend=False,
        line=dict(color=COLOR_PALETTE["secondary"], width=2.5, dash="dash")
    ))
    
    # Forecasted spending line
    fig.add_trace(go.Scatter(
        x=fore["Week"],
        y=fore["Amount"],
        mode="lines+markers",
        name=f"Forecasted Spend (R²={r2:.2f})",
        line=dict(color=COLOR_PALETTE["secondary"], width=3, dash="dash"),
        marker=dict(size=8, symbol="star")
    ))
    
    fig.update_layout(
        title="<b>Weekly Expense Trend & Forecast</b>",
        xaxis_title="Week Beginning",
        yaxis_title="Weekly Spend ($)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return apply_chart_theme(fig)
