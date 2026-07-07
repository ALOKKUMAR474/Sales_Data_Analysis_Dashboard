import pandas as pd
import numpy as np
import streamlit as st

@st.cache_data
def load_data(filepath="sales_data.csv"):
    """
    Loads and cleans the sales dataset.
    Caches the results to improve dashboard performance.
    """
    df = pd.read_csv(filepath)
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Ship Date"] = pd.to_datetime(df["Ship Date"])
    
    # Sort chronologically
    df = df.sort_values("Order Date").reset_index(drop=True)
    
    # Extract temporal components for easier filtering
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.strftime("%Y-%m")
    df["Month_Name"] = df["Order Date"].dt.strftime("%b")
    df["Day_Of_Week"] = df["Order Date"].dt.strftime("%a")
    df["Quarter"] = df["Order Date"].dt.to_period("Q").astype(str)
    
    # Calculate order-level metrics
    df["Margin %"] = (df["Profit"] / df["Sales"] * 100).round(2)
    
    return df

def get_kpis(df, df_prior=None):
    """
    Calculates key metrics: Total Sales, Total Profit, Profit Margin, Total Orders.
    Optionally compares against a prior period to compute growth.
    """
    metrics = {}
    
    # Current Period Metrics
    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()
    margin = (total_profit / total_sales * 100) if total_sales > 0 else 0
    total_orders = df["Order ID"].nunique()
    avg_order_val = (total_sales / total_orders) if total_orders > 0 else 0
    
    metrics["sales"] = {"value": f"${total_sales:,.2f}", "raw": total_sales}
    metrics["profit"] = {"value": f"${total_profit:,.2f}", "raw": total_profit}
    metrics["margin"] = {"value": f"{margin:.1f}%", "raw": margin}
    metrics["orders"] = {"value": f"{total_orders:,}", "raw": total_orders}
    metrics["avg_order"] = {"value": f"${avg_order_val:,.2f}", "raw": avg_order_val}
    
    # Prior Period Metrics for Delta Calculations
    if df_prior is not None and not df_prior.empty:
        prior_sales = df_prior["Sales"].sum()
        prior_profit = df_prior["Profit"].sum()
        prior_margin = (prior_profit / prior_sales * 100) if prior_sales > 0 else 0
        prior_orders = df_prior["Order ID"].nunique()
        prior_avg_order = (prior_sales / prior_orders) if prior_orders > 0 else 0
        
        # Calculate Delta %
        metrics["sales"]["delta"] = f"{((total_sales - prior_sales) / prior_sales * 100):+.1f}%" if prior_sales > 0 else None
        metrics["sales"]["delta_type"] = "up" if (total_sales >= prior_sales) else "down"
        
        metrics["profit"]["delta"] = f"{((total_profit - prior_profit) / prior_profit * 100):+.1f}%" if prior_profit > 0 else None
        metrics["profit"]["delta_type"] = "up" if (total_profit >= prior_profit) else "down"
        
        margin_diff = margin - prior_margin
        metrics["margin"]["delta"] = f"{margin_diff:+.1f}%"
        metrics["margin"]["delta_type"] = "up" if (margin_diff >= 0) else "down"
        
        metrics["orders"]["delta"] = f"{((total_orders - prior_orders) / prior_orders * 100):+.1f}%" if prior_orders > 0 else None
        metrics["orders"]["delta_type"] = "up" if (total_orders >= prior_orders) else "down"
        
        metrics["avg_order"]["delta"] = f"{((avg_order_val - prior_avg_order) / prior_avg_order * 100):+.1f}%" if prior_avg_order > 0 else None
        metrics["avg_order"]["delta_type"] = "up" if (avg_order_val >= prior_avg_order) else "down"
    else:
        # Defaults if no prior period
        for key in ["sales", "profit", "margin", "orders", "avg_order"]:
            metrics[key]["delta"] = None
            metrics[key]["delta_type"] = "up"
            
    return metrics

def get_sales_trends(df, freq="Month"):
    """
    Computes sales and profit trends grouped by Month or Quarter.
    """
    group_col = "Month" if freq == "Month" else "Quarter"
    trend = df.groupby(group_col).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()
    
    # Sort to ensure chronological order
    trend = trend.sort_values(group_col)
    return trend

def get_product_performance(df, n=10):
    """
    Computes top performing products by total sales.
    """
    prod = df.groupby(["Product Name", "Category"]).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    ).reset_index()
    return prod.sort_values("Sales", ascending=False).head(n)

def get_category_performance(df):
    """
    Computes performance metrics across Product Categories.
    """
    cat = df.groupby("Category").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    ).reset_index()
    cat["Margin %"] = (cat["Profit"] / cat["Sales"] * 100).round(2)
    return cat.sort_values("Sales", ascending=False)

def get_subcategory_performance(df, category=None):
    """
    Computes performance metrics for Sub-Categories.
    Optionally filters for a specific Category.
    """
    filtered_df = df if category is None else df[df["Category"] == category]
    subcat = filtered_df.groupby(["Sub-Category", "Category"]).agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Quantity=("Quantity", "sum")
    ).reset_index()
    subcat["Margin %"] = (subcat["Profit"] / subcat["Sales"] * 100).round(2)
    return subcat.sort_values("Sales", ascending=False)

def get_regional_performance(df):
    """
    Computes sales and profit metrics across geographical regions.
    """
    reg = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()
    reg["Margin %"] = (reg["Profit"] / reg["Sales"] * 100).round(2)
    return reg.sort_values("Sales", ascending=False)

def get_segment_performance(df):
    """
    Computes performance metrics across Customer Segments.
    """
    seg = df.groupby("Segment").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Order ID", "nunique")
    ).reset_index()
    seg["Margin %"] = (seg["Profit"] / seg["Sales"] * 100).round(2)
    return seg.sort_values("Sales", ascending=False)
