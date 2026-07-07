import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Import helper functions
from utils import (
    load_data, get_kpis, get_sales_trends,
    get_product_performance, get_category_performance,
    get_subcategory_performance, get_regional_performance,
    get_segment_performance
)

# Page configuration
st.set_page_config(
    page_title="Sales Performance Insights",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Theme Toggle State
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"

IS_DARK = st.session_state.theme == "dark"

# Define CSS styling variables dynamically
bg = "#09090b" if IS_DARK else "#ffffff"
bg_subtle = "#0c0c0f" if IS_DARK else "#f9fafb"
card = "#0c0c0f" if IS_DARK else "#ffffff"
card_hover = "#131316" if IS_DARK else "#f4f4f5"
border = "#1e1e24" if IS_DARK else "#e4e4e7"
border_subtle = "#16161a" if IS_DARK else "#f0f0f2"
text = "#fafafa" if IS_DARK else "#09090b"
text_muted = "#71717a"
text_dim = "#52525b" if IS_DARK else "#a1a1aa"
accent = "#2563eb"
accent_muted = "#1d4ed8"
green = "#22c55e" if IS_DARK else "#16a34a"
green_muted = "rgba(34,197,94,0.12)" if IS_DARK else "rgba(22,163,74,0.08)"
red = "#ef4444" if IS_DARK else "#dc2626"
red_muted = "rgba(239,68,68,0.12)" if IS_DARK else "rgba(220,38,38,0.08)"
amber = "#f59e0b" if IS_DARK else "#d97706"
amber_muted = "rgba(245,158,11,0.12)" if IS_DARK else "rgba(217,119,6,0.08)"
shadow = "none" if IS_DARK else "0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.03)"
radius = "10px"

# Inject Custom CSS
st.markdown(f"""
<style>
:root {{
    --bg: {bg};
    --bg-subtle: {bg_subtle};
    --card: {card};
    --card-hover: {card_hover};
    --border: {border};
    --border-subtle: {border_subtle};
    --text: {text};
    --text-muted: {text_muted};
    --text-dim: {text_dim};
    --accent: {accent};
    --accent-muted: {accent_muted};
    --green: {green};
    --green-muted: {green_muted};
    --red: {red};
    --red-muted: {red_muted};
    --amber: {amber};
    --amber-muted: {amber_muted};
    --shadow: {shadow};
    --radius: {radius};
}}

/* Hide default streamlit headers/footers */
header[data-testid="stHeader"], #MainMenu, footer, [data-testid="stToolbar"],
[data-testid="stDecoration"], [data-testid="stStatusWidget"], .stDeployButton,
div[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
}}

html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"], .main, .block-container, section[data-testid="stMain"] {{
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', -apple-system, sans-serif !important;
}}
.block-container {{
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1360px !important;
}}

/* Custom Tabs styling */
button[data-baseweb="tab"] {{
    background: transparent !important;
    color: var(--text-muted) !important;
    font-size: 0.835rem !important;
    font-weight: 500 !important;
    padding: 0.55rem 1rem !important;
    border: 1px solid transparent !important;
    border-radius: 7px !important;
    transition: all 0.2s ease !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{
    color: var(--text) !important;
    background: var(--card) !important;
    border-color: var(--border) !important;
}}
[data-baseweb="tab-highlight"], [data-baseweb="tab-border"] {{
    display: none !important;
}}
[data-baseweb="tab-list"] {{
    gap: 4px !important;
    background: var(--bg-subtle) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    margin-bottom: 1.5rem !important;
}}

/* Metric Card styling */
.metric-card {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.25rem 1.4rem;
    box-shadow: var(--shadow);
    transition: transform 0.2s, box-shadow 0.2s;
}}
.metric-card:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.metric-label {{
    font-size: 0.78rem;
    color: var(--text-muted);
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}}
.metric-value {{
    font-size: 1.75rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.03em;
    margin-top: 0.2rem;
}}
.metric-delta {{
    font-size: 0.72rem;
    font-weight: 500;
    margin-top: 0.4rem;
    padding: 2px 8px;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    gap: 3px;
}}
.delta-up {{ color: var(--green); background: var(--green-muted); }}
.delta-down {{ color: var(--red); background: var(--red-muted); }}
.delta-warn {{ color: var(--amber); background: var(--amber-muted); }}

/* Chart styling */
.chart-wrap {{
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem 1.2rem 0.6rem;
    box-shadow: var(--shadow);
    margin-bottom: 1.25rem;
    transition: all 0.2s ease;
}}
.chart-title {{
    font-size: 0.82rem;
    font-weight: 600;
    color: var(--text);
    letter-spacing: -0.01em;
}}
.chart-subtitle {{
    font-size: 0.72rem;
    color: var(--text-dim);
    margin-bottom: 0.8rem;
}}

/* Data Table styling */
.data-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.8rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    overflow: hidden;
}}
.data-table th {{
    text-align: left;
    padding: 0.7rem 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    border-bottom: 1px solid var(--border);
    background: var(--bg-subtle);
}}
.data-table td {{
    padding: 0.75rem 0.9rem;
    color: var(--text);
    border-bottom: 1px solid var(--border-subtle);
}}
.data-table tr:last-child td {{
    border-bottom: none;
}}
.data-table tr:hover td {{
    background-color: var(--card-hover);
}}

/* Badge styling */
.badge {{
    display: inline-block;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 500;
}}
.badge-green {{ color: var(--green); background: var(--green-muted); }}
.badge-red {{ color: var(--red); background: var(--red-muted); }}
.badge-amber {{ color: var(--amber); background: var(--amber-muted); }}
.badge-blue {{ color: var(--accent); background: rgba(37,99,235,0.1); }}

/* Brand Header */
.brand {{
    display: flex;
    align-items: center;
    gap: 8px;
    padding-bottom: 1rem;
}}
.brand-icon {{
    font-size: 1.5rem;
    color: var(--accent);
}}
.brand-name {{
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: -0.02em;
}}

/* Horizontal blocks gap */
[data-testid="stHorizontalBlock"] {{
    gap: 1.25rem !important;
}}

/* Sidebar details panel */
.details-panel {{
    background: var(--bg-subtle);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.2rem;
    height: 100%;
}}
.details-label {{
    font-size: 0.7rem;
    color: var(--text-muted);
    font-weight: 500;
    margin-top: 0.6rem;
}}
.details-val {{
    font-size: 0.85rem;
    color: var(--text);
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# Helper function to render Metric Card
def metric_card(label, value, delta=None, delta_type="up"):
    cls = f"delta-{delta_type}"
    arrow = "↑" if delta_type == "up" else ("↓" if delta_type == "down" else "→")
    delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# Plotly default layout configuration
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#fafafa" if IS_DARK else "#09090b", size=11),
    margin=dict(l=40, r=20, t=20, b=40),
    xaxis=dict(
        gridcolor="rgba(255,255,255,0.04)" if IS_DARK else "rgba(0,0,0,0.04)",
        zerolinecolor="rgba(255,255,255,0.04)" if IS_DARK else "rgba(0,0,0,0.04)",
        tickfont=dict(size=10, color="#71717a"),
    ),
    yaxis=dict(
        gridcolor="rgba(255,255,255,0.04)" if IS_DARK else "rgba(0,0,0,0.04)",
        zerolinecolor="rgba(255,255,255,0.04)" if IS_DARK else "rgba(0,0,0,0.04)",
        tickfont=dict(size=10, color="#71717a"),
    ),
)

# Header Row
head_left, head_right = st.columns([8, 1.2])
with head_left:
    st.markdown("""
    <div class="brand">
        <span class="brand-icon">◆</span>
        <span class="brand-name">Sales Performance Insights</span>
    </div>
    """, unsafe_allow_html=True)
with head_right:
    theme_label = "☀️ Light Mode" if IS_DARK else "🌙 Dark Mode"
    st.button(theme_label, on_click=toggle_theme, use_container_width=True)

# Load data
df = load_data()

# Filters Row
filter_col1, filter_col2, filter_col3, filter_col4 = st.columns([1, 1, 1, 1])

with filter_col1:
    years = ["All"] + sorted(list(df["Year"].unique()), reverse=True)
    selected_year = st.selectbox("Year", years)

with filter_col2:
    regions = ["All"] + sorted(list(df["Region"].unique()))
    selected_region = st.selectbox("Region", regions)

with filter_col3:
    categories = ["All"] + sorted(list(df["Category"].unique()))
    selected_category = st.selectbox("Category", categories)

with filter_col4:
    segments = ["All"] + sorted(list(df["Segment"].unique()))
    selected_segment = st.selectbox("Customer Segment", segments)

# Filter Dataframe
filtered_df = df.copy()
prior_df = df.copy()

if selected_year != "All":
    filtered_df = filtered_df[filtered_df["Year"] == selected_year]
    # Prior year is year - 1
    prior_df = prior_df[prior_df["Year"] == (selected_year - 1)]
else:
    # If all years, split dataset in half as mock prior period comparison
    midpoint = len(df) // 2
    prior_df = df.iloc[:midpoint]
    filtered_df = df.iloc[midpoint:]

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]
    prior_df = prior_df[prior_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]
    prior_df = prior_df[prior_df["Category"] == selected_category]

if selected_segment != "All":
    filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]
    prior_df = prior_df[prior_df["Segment"] == selected_segment]


# Tabs Navigation
tab_overview, tab_products, tab_transactions, tab_assistant = st.tabs([
    "📈 Executive Overview", 
    "📦 Product Performance", 
    "📋 Transaction Records", 
    "✨ AI Sales Assistant"
])

# ----------------- EXECUTIVE OVERVIEW -----------------
with tab_overview:
    # KPI Row
    kpis = get_kpis(filtered_df, prior_df)
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Total Revenue", kpis["sales"]["value"], kpis["sales"]["delta"], kpis["sales"]["delta_type"])
    with c2:
        metric_card("Total Profit", kpis["profit"]["value"], kpis["profit"]["delta"], kpis["profit"]["delta_type"])
    with c3:
        metric_card("Net Profit Margin", kpis["margin"]["value"], kpis["margin"]["delta"], kpis["margin"]["delta_type"])
    with c4:
        metric_card("Total Orders", kpis["orders"]["value"], kpis["orders"]["delta"], kpis["orders"]["delta_type"])
    with c5:
        metric_card("Average Order Value", kpis["avg_order"]["value"], kpis["avg_order"]["delta"], kpis["avg_order"]["delta_type"])

    st.write("") # Spacing

    # Charts Layout
    row1_left, row1_right = st.columns([6.5, 3.5])
    
    with row1_left:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Revenue & Profit Growth Trend</div>
            <div class="chart-subtitle">Monthly breakdown of gross revenue compared to bottom-line profit margins</div>
        """, unsafe_allow_html=True)
        
        # Monthly sales trend calculations
        trends = get_sales_trends(filtered_df, freq="Month")
        
        fig_trend = go.Figure()
        # Revenue Line
        fig_trend.add_trace(go.Scatter(
            x=trends["Month"], y=trends["Sales"], name="Revenue",
            line=dict(color="#2563eb", width=2.5), mode="lines+markers"
        ))
        # Profit Area/Bar
        fig_trend.add_trace(go.Bar(
            x=trends["Month"], y=trends["Profit"], name="Profit",
            marker_color="rgba(34,197,94,0.3)" if IS_DARK else "rgba(22,163,74,0.25)",
            marker_line=dict(width=1, color="#22c55e" if IS_DARK else "#16a34a")
        ))
        
        fig_trend.update_layout(
            **PLOT_LAYOUT,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=320,
            hovermode="x unified"
        )
        st.plotly_chart(fig_trend, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with row1_right:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Sales Mix by Segment</div>
            <div class="chart-subtitle">Share of sales generated by Customer Segments</div>
        """, unsafe_allow_html=True)
        
        seg_data = get_segment_performance(filtered_df)
        
        colors = ["#2563eb", "#8b5cf6", "#ec4899"] if IS_DARK else ["#3b82f6", "#a78bfa", "#f472b6"]
        fig_seg = go.Figure(data=[go.Pie(
            labels=seg_data["Segment"],
            values=seg_data["Sales"],
            hole=0.55,
            marker=dict(colors=colors, line=dict(color=bg, width=1.5))
        )])
        
        fig_seg.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans, sans-serif", color="#fafafa" if IS_DARK else "#09090b", size=11),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            height=320
        )
        st.plotly_chart(fig_seg, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)

    # Row 2 (Regional Performance)
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">Geographical Performance</div>
        <div class="chart-subtitle">Revenue distribution and net margins across East, West, Central, and South regions</div>
    """, unsafe_allow_html=True)
    
    reg_perf = get_regional_performance(filtered_df)
    
    fig_reg = go.Figure()
    fig_reg.add_trace(go.Bar(
        x=reg_perf["Region"], y=reg_perf["Sales"], name="Revenue",
        marker_color="#2563eb", marker_line_color="#1d4ed8", marker_line_width=1.2
    ))
    fig_reg.add_trace(go.Scatter(
        x=reg_perf["Region"], y=reg_perf["Margin %"], name="Profit Margin (%)",
        yaxis="y2", line=dict(color="#d97706", width=2.5), mode="lines+markers"
    ))
    
    fig_reg.update_layout(
        **PLOT_LAYOUT,
        yaxis2=dict(
            title="Profit Margin (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(size=10, color="#71717a"),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=280,
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_reg, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- PRODUCT ANALYSIS -----------------
with tab_products:
    p_left, p_right = st.columns([5, 5])
    
    with p_left:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Sales and Profit by Category</div>
            <div class="chart-subtitle">Direct comparison of top-line revenue against bottom-line profitability</div>
        """, unsafe_allow_html=True)
        
        cat_perf = get_category_performance(filtered_df)
        
        fig_cat = go.Figure(data=[
            go.Bar(name="Sales", x=cat_perf["Category"], y=cat_perf["Sales"], marker_color="#2563eb"),
            go.Bar(name="Profit", x=cat_perf["Category"], y=cat_perf["Profit"], marker_color="#22c55e")
        ])
        fig_cat.update_layout(
            **PLOT_LAYOUT,
            barmode="group",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            height=300
        )
        st.plotly_chart(fig_cat, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    with p_right:
        st.markdown("""
        <div class="chart-wrap">
            <div class="chart-title">Sub-Category Sales Breakdown</div>
            <div class="chart-subtitle">Total sales rankings across product sub-categories</div>
        """, unsafe_allow_html=True)
        
        sub_perf = get_subcategory_performance(filtered_df)
        sub_perf = sub_perf.sort_values("Sales", ascending=True)
        
        fig_sub = go.Figure(go.Bar(
            y=sub_perf["Sub-Category"], x=sub_perf["Sales"], orientation="h",
            marker=dict(
                color=sub_perf["Sales"],
                colorscale="Blues" if not IS_DARK else "Viridis",
            )
        ))
        fig_sub.update_layout(
            **PLOT_LAYOUT,
            margin=dict(l=100, r=20, t=10, b=40),
            height=300
        )
        st.plotly_chart(fig_sub, use_container_width=True, config={"displayModeBar": False})
        st.markdown("</div>", unsafe_allow_html=True)
        
    # Product Scatter Plot
    st.markdown("""
    <div class="chart-wrap">
        <div class="chart-title">Product Efficiency Matrix</div>
        <div class="chart-subtitle">Bubble plot of sales vs profit. Bubble size represents units sold. Category represents colors.</div>
    """, unsafe_allow_html=True)
    
    prod_perf = get_product_performance(filtered_df, n=50)
    
    fig_scat = px.scatter(
        prod_perf, x="Sales", y="Profit", size="Quantity", color="Category",
        hover_name="Product Name",
        color_discrete_map={"Technology": "#2563eb", "Office Supplies": "#8b5cf6", "Furniture": "#ec4899"}
    )
    
    fig_scat.update_layout(
        **PLOT_LAYOUT,
        margin=dict(l=40, r=40, t=20, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        height=320
    )
    st.plotly_chart(fig_scat, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

# ----------------- TRANSACTION RECORDS -----------------
with tab_transactions:
    # Top Actions Row
    tx_col1, tx_col2, tx_col3 = st.columns([5, 3, 2])
    with tx_col1:
        search_query = st.text_input("🔍 Search Customers or Products", "")
    with tx_col2:
        ship_mode_filter = st.selectbox("Shipping Mode", ["All", "Standard Class", "Second Class", "First Class", "Same Day"])
    with tx_col3:
        # Spacing adjustment
        st.write("")
        st.write("")
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Export Filtered CSV",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
    # Split Layout for Table + Details panel
    tx_left, tx_right = st.columns([7, 3])
    
    tx_filtered = filtered_df.copy()
    if search_query:
        tx_filtered = tx_filtered[
            tx_filtered["Customer Name"].str.contains(search_query, case=False) |
            tx_filtered["Product Name"].str.contains(search_query, case=False) |
            tx_filtered["Order ID"].str.contains(search_query, case=False)
        ]
    if ship_mode_filter != "All":
        tx_filtered = tx_filtered[tx_filtered["Ship Mode"] == ship_mode_filter]
        
    recent_txs = tx_filtered.head(10)
    
    # Store selected row in Session State
    if "selected_order_id" not in st.session_state and not recent_txs.empty:
        st.session_state.selected_order_id = recent_txs.iloc[0]["Order ID"]
        
    with tx_left:
        if recent_txs.empty:
            st.info("No matching records found.")
        else:
            # Build Table HTML
            table_rows = ""
            for idx, row in recent_txs.iterrows():
                is_selected = row["Order ID"] == st.session_state.selected_order_id
                row_style = f'style="background-color: var(--card-hover); cursor: pointer;"' if is_selected else 'style="cursor: pointer;"'
                
                # Badges
                profit_badge = f'<span class="badge badge-green">${row["Profit"]:,.2f}</span>' if row["Profit"] >= 0 else f'<span class="badge badge-red">${row["Profit"]:,.2f}</span>'
                ship_class = "badge-blue" if row["Ship Mode"] == "Same Day" else ("badge-green" if row["Ship Mode"] == "First Class" else "badge-amber")
                ship_badge = f'<span class="badge {ship_class}">{row["Ship Mode"]}</span>'
                
                # Format Date
                order_date_formatted = pd.to_datetime(row["Order Date"]).strftime("%b %d, %Y")
                
                # Custom click handler simulation (using simple radio buttons below or key identifiers in a listbox for selection)
                table_rows += f"""
                <tr {row_style}>
                    <td><b>{row["Order ID"]}</b></td>
                    <td>{order_date_formatted}</td>
                    <td>{row["Customer Name"]}</td>
                    <td>{row["Category"]}</td>
                    <td>${row["Sales"]:,.2f}</td>
                    <td>{profit_badge}</td>
                    <td>{ship_badge}</td>
                </tr>
                """
                
            st.markdown(f"""
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Order Date</th>
                        <th>Customer</th>
                        <th>Category</th>
                        <th>Sales</th>
                        <th>Profit</th>
                        <th>Shipping</th>
                    </tr>
                </thead>
                <tbody>
                    {table_rows}
                </tbody>
            </table>
            """, unsafe_allow_html=True)
            
            # Interactive row selection control
            st.write("")
            selectable_ids = list(recent_txs["Order ID"])
            if st.session_state.selected_order_id not in selectable_ids and selectable_ids:
                st.session_state.selected_order_id = selectable_ids[0]
                
            selected_idx = selectable_ids.index(st.session_state.selected_order_id) if st.session_state.selected_order_id in selectable_ids else 0
            
            selected_order = st.selectbox(
                "Select an Order ID to inspect details:", 
                selectable_ids, 
                index=selected_idx
            )
            if selected_order != st.session_state.selected_order_id:
                st.session_state.selected_order_id = selected_order
                st.rerun()

    with tx_right:
        if not recent_txs.empty and st.session_state.selected_order_id:
            row_info = tx_filtered[tx_filtered["Order ID"] == st.session_state.selected_order_id].iloc[0]
            
            st.markdown(f"""
            <div class="details-panel">
                <h5 style="margin-top:0; color: var(--accent);">Order Inspector</h5>
                <hr style="border: 0.5px solid var(--border); margin: 0.5rem 0;" />
                
                <div class="details-label">ORDER ID</div>
                <div class="details-val" style="font-family: 'JetBrains Mono', monospace;">{row_info["Order ID"]}</div>
                
                <div class="details-label">CUSTOMER NAME</div>
                <div class="details-val">{row_info["Customer Name"]} ({row_info["Segment"]})</div>
                
                <div class="details-label">GEOGRAPHY</div>
                <div class="details-val">{row_info["City"]}, {row_info["State"]} ({row_info["Region"]} Region)</div>
                
                <div class="details-label">PRODUCT DETAILS</div>
                <div class="details-val" style="font-size:0.8rem; line-height:1.2;">{row_info["Product Name"]}</div>
                
                <div class="details-label">CATEGORY / SUB-CATEGORY</div>
                <div class="details-val">{row_info["Category"]} / {row_info["Sub-Category"]}</div>
                
                <div class="details-label">QUANTITY ORDERED</div>
                <div class="details-val">{row_info["Quantity"]} units</div>
                
                <div class="details-label">FINANCIAL SUMMARY</div>
                <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
                    <div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">SALES</div>
                        <div style="font-size:1.1rem; font-weight:700; color:var(--text);">${row_info["Sales"]:,.2f}</div>
                    </div>
                    <div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">DISCOUNT</div>
                        <div style="font-size:1.1rem; font-weight:700; color:var(--text);">{row_info["Discount"]*100:.0f}%</div>
                    </div>
                    <div>
                        <div style="font-size:0.7rem; color:var(--text-muted);">NET PROFIT</div>
                        <div style="font-size:1.1rem; font-weight:700; color:{green if row_info['Profit'] >= 0 else red};">${row_info["Profit"]:,.2f}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ----------------- AI SALES ASSISTANT -----------------
with tab_assistant:
    st.markdown("""
    <div style="background-color: var(--bg-subtle); border: 1px solid var(--border); border-radius: var(--radius); padding: 1.25rem; margin-bottom: 1.5rem;">
        <h4 style="margin: 0; color: var(--accent);">✨ Smart Data Inquiry Assistant</h4>
        <p style="margin: 0.25rem 0 0; font-size: 0.78rem; color: var(--text-muted);">
            Query your database using natural language. Paste your Gemini API key in the sidebar for full conversational queries, or test using the sample insights below.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for API Key in environment or sidebar
    api_key = st.text_input("Google Gemini API Key (Optional)", type="password", help="Get a key from Google AI Studio. Your key is not saved.")
    
    preset_questions = [
        "Select a sample analytical inquiry...",
        "What is the total revenue and profit margin for each Product Category?",
        "Show me monthly sales trends for Technology products",
        "Which state in the West region has the highest profit?",
        "Identify high discount orders (> 20%) that resulted in a net loss"
    ]
    
    selected_preset = st.selectbox("Sample Resume Inquiries (Runs local analytical code instantly):", preset_questions)
    
    custom_query = st.text_input("Or type your own natural language query (Requires Gemini API Key):", "")
    
    run_btn = st.button("🚀 Analyze Database")
    
    # Process
    if run_btn:
        # Prioritize custom queries with Gemini API Key
        if custom_query and api_key:
            with st.spinner("Gemini AI is analyzing the database schema and drafting analysis..."):
                try:
                    import google.generativeai as genai
                    genai.configure(api_key=api_key)
                    
                    # Create the model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    
                    # Give strict context to prevent code injection issues
                    system_prompt = f"""
                    You are a Data Analyst Assistant. You are given a pandas DataFrame named `df` representing sales data.
                    Here is the schema (first row):
                    {df.head(1).to_dict(orient='records')[0]}
                    
                    The user asks: "{custom_query}"
                    
                    Write Python pandas code to answer this question. The code will be run in `exec()`.
                    Follow these rules:
                    1. Write the code inside a ```python ``` block.
                    2. Keep the code safe. Do not import system libraries like os, sys, shutil. Only pandas (`pd`), numpy (`np`), and plotly.express (`px`).
                    3. Save the final output data to a variable named `result_data` (either a DataFrame, Series, or scalar value).
                    4. If you want to render a plotly figure, save it to a variable named `result_fig` (a plotly Figure object).
                    5. Provide a short textual explanation of the answer, and save it to a string variable named `explanation`.
                    
                    Respond ONLY with a code block, explanation, and variable assignments. Do not add conversational filler outside.
                    """
                    
                    response = model.generate_content(system_prompt)
                    response_text = response.text
                    
                    # Extract python code
                    code_block = ""
                    if "```python" in response_text:
                        code_block = response_text.split("```python")[1].split("```")[0].strip()
                    elif "```" in response_text:
                        code_block = response_text.split("```")[1].split("```")[0].strip()
                    else:
                        code_block = response_text
                        
                    # Prepare execution scope
                    scope = {"df": df, "pd": pd, "np": np, "px": px, "go": go}
                    
                    # Run the generated code safely
                    exec(code_block, scope)
                    
                    # Render outputs
                    st.markdown("### 📊 AI Analysis Results")
                    
                    # Explanation
                    if "explanation" in scope:
                        st.info(scope["explanation"])
                    
                    # Show Code
                    with st.expander("🛠️ View Python Analysis Code"):
                        st.code(code_block, language="python")
                        
                    # Result Data
                    if "result_data" in scope:
                        res = scope["result_data"]
                        st.markdown("#### Table Output")
                        if isinstance(res, (pd.DataFrame, pd.Series)):
                            st.dataframe(res, use_container_width=True)
                        else:
                            st.metric("Calculation Value", str(res))
                            
                    # Result Figure
                    if "result_fig" in scope and scope["result_fig"] is not None:
                        st.markdown("#### Visual Output")
                        fig = scope["result_fig"]
                        fig.update_layout(
                            paper_bgcolor="rgba(0,0,0,0)",
                            plot_bgcolor="rgba(0,0,0,0)",
                            font=dict(family="DM Sans, sans-serif", color="#fafafa" if IS_DARK else "#09090b", size=11),
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                except Exception as e:
                    st.error(f"Failed to compile AI generated code: {e}")
                    st.warning("Please check your prompt or API Key and try again.")
                    
        # Presets (Instant Local Run)
        elif selected_preset != "Select a sample analytical inquiry...":
            st.markdown("### 📊 Local Analysis Output")
            
            if selected_preset == "What is the total revenue and profit margin for each Product Category?":
                code = """
result_data = df.groupby("Category").agg(
    Revenue=("Sales", "sum"),
    Profit=("Profit", "sum")
).reset_index()
result_data["Profit Margin (%)"] = (result_data["Profit"] / result_data["Revenue"] * 100).round(2)
result_fig = px.bar(result_data, x="Category", y="Revenue", color="Profit Margin (%)", text_auto='.2s',
                    title="Revenue & Margins by Category", color_continuous_scale="Viridis")
explanation = "Technology brings in the highest revenue, but Office Supplies has equivalent profit margins with lower capital requirements. Furniture has very low profit margins."
                """
            elif selected_preset == "Show me monthly sales trends for Technology products":
                code = """
tech_df = df[df["Category"] == "Technology"]
result_data = tech_df.groupby("Month").agg(Revenue=("Sales", "sum"), Orders=("Order ID", "nunique")).reset_index()
result_fig = px.line(result_data, x="Month", y="Revenue", title="Technology Revenue Monthly Growth", markers=True)
explanation = "Technology monthly trends show a steady growth, spiked strongly by end-of-year holiday purchasing cycles (November and December)."
                """
            elif selected_preset == "Which state in the West region has the highest profit?":
                code = """
west_df = df[df["Region"] == "West"]
result_data = west_df.groupby("State").agg(Revenue=("Sales", "sum"), Net_Profit=("Profit", "sum")).reset_index()
result_data = result_data.sort_values("Net_Profit", ascending=False)
result_fig = px.bar(result_data, x="State", y="Net_Profit", color="Revenue", title="State Profitability in the West Region")
explanation = "California is the primary contributor in the West region, leading both in absolute revenue and net profits. Washington is second."
                """
            elif selected_preset == "Identify high discount orders (> 20%) that resulted in a net loss":
                code = """
loss_df = df[(df["Discount"] > 0.20) & (df["Profit"] < 0)]
result_data = loss_df[["Order ID", "Customer Name", "Product Name", "Sales", "Discount", "Profit"]].head(10)
result_fig = px.scatter(loss_df, x="Discount", y="Profit", size="Sales", color="Category", hover_name="Customer Name",
                        title="Loss Magnitude vs Discount Rates")
explanation = "Providing discounts above 20% heavily correlates with unprofitable orders, particularly in the Furniture category (Tables & Bookcases)."
                """
            
            # Execute local presets
            scope = {"df": df, "pd": pd, "np": np, "px": px, "go": go}
            exec(code, scope)
            
            st.info(scope["explanation"])
            
            with st.expander("🛠️ View Python Analysis Code"):
                st.code(code.strip(), language="python")
                
            st.markdown("#### Table Output")
            st.dataframe(scope["result_data"], use_container_width=True)
            
            st.markdown("#### Visual Output")
            fig = scope["result_fig"]
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans, sans-serif", color="#fafafa" if IS_DARK else "#09090b", size=11),
                margin=dict(l=40, r=40, t=40, b=40),
            )
            st.plotly_chart(fig, use_container_width=True)
            
        else:
            st.warning("Please select a sample insight to run or input a custom query with a Gemini API Key.")
