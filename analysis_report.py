import pandas as pd
import numpy as np

def run_analysis():
    print("=========================================================")
    print("       SALES ANALYSIS REPORT - PANDAS DATA EXPLORATION   ")
    print("=========================================================\n")
    
    # 1. Load the dataset
    print("[1] Loading sales_data.csv...")
    df = pd.read_csv("sales_data.csv")
    print(f"    Loaded {len(df):,} sales records successfully.\n")
    
    # 2. Clean & preprocess
    print("[2] Cleaning and preprocessing data...")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Sales"] = pd.to_numeric(df["Sales"])
    df["Profit"] = pd.to_numeric(df["Profit"])
    
    # Check for missing values
    missing_count = df.isnull().sum().sum()
    print(f"    Checking for null values: {missing_count} found.")
    
    # Add Quarter field
    df["Quarter"] = df["Order Date"].dt.to_period("Q")
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.strftime("%Y-%m")
    print("    Pre-processing complete. Derived Quarter and Month periods.\n")
    
    # 3. Analyze Quarter-on-Quarter (QoQ) Trends
    print("[3] Running Quarter-on-Quarter (QoQ) Revenue analysis...")
    quarterly_sales = df.groupby("Quarter")["Sales"].sum().reset_index()
    quarterly_sales["QoQ Change %"] = quarterly_sales["Sales"].pct_change() * 100
    
    print("\n    Quarterly Sales Performance Summary:")
    print("    -----------------------------------------------------")
    print("    Quarter       Total Sales ($)       QoQ Growth (%)")
    print("    -----------------------------------------------------")
    for _, row in quarterly_sales.iterrows():
        growth_str = f"{row['QoQ Change %']:+.2f}%" if not pd.isna(row['QoQ Change %']) else "N/A"
        print(f"    {row['Quarter']}       ${row['Sales']:,.2f}       {growth_str}")
    print("    -----------------------------------------------------")
    
    # Specific Check for Q3 2025 decline vs Q2 2025
    q2_2025_sales = df[df["Quarter"] == "2025Q2"]["Sales"].sum()
    q3_2025_sales = df[df["Quarter"] == "2025Q3"]["Sales"].sum()
    q3_decline_pct = ((q3_2025_sales - q2_2025_sales) / q2_2025_sales) * 100
    
    print(f"\n    [ALERT] Q3 2025 Sales: ${q3_2025_sales:,.2f} | Q2 2025 Sales: ${q2_2025_sales:,.2f}")
    print(f"    [ALERT] Detected decline rate: {q3_decline_pct:.2f}%\n")
    
    # 4. Top Performing Product Categories
    print("[4] Identifying top-performing categories...")
    category_summary = df.groupby("Category").agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).reset_index()
    category_summary["Net_Margin_%"] = (category_summary["Total_Profit"] / category_summary["Total_Sales"]) * 100
    category_summary = category_summary.sort_values("Total_Sales", ascending=False)
    
    print("\n    Category Performance Summary:")
    print("    -------------------------------------------------------------------------")
    print("    Category          Sales ($)         Profit ($)        Net Margin (%)")
    print("    -------------------------------------------------------------------------")
    for _, row in category_summary.iterrows():
        print(f"    {row['Category']:<16}  ${row['Total_Sales']:,.2f}    ${row['Total_Profit']:,.2f}    {row['Net_Margin_%']:.2f}%")
    print("    -------------------------------------------------------------------------")
    
    # 5. Export results
    report_file = "analysis_report.txt"
    with open(report_file, "w") as f:
        f.write("=========================================================\n")
        f.write("       SALES ANALYSIS REPORT - PANDAS DATA EXPLORATION   \n")
        f.write("=========================================================\n\n")
        f.write(f"Total Records Analyzed: {len(df):,}\n")
        f.write(f"Pre-processing Date range: {df['Order Date'].min().strftime('%Y-%m-%d')} to {df['Order Date'].max().strftime('%Y-%m-%d')}\n\n")
        
        f.write("1. QUARTERLY SALES TRENDS & QOQ GROWTH:\n")
        f.write("-----------------------------------------------------\n")
        f.write("Quarter       Total Sales ($)       QoQ Growth (%)\n")
        f.write("-----------------------------------------------------\n")
        for _, row in quarterly_sales.iterrows():
            growth_str = f"{row['QoQ Change %']:+.2f}%" if not pd.isna(row['QoQ Change %']) else "N/A"
            f.write(f"{row['Quarter']}       ${row['Sales']:,.2f}       {growth_str}\n")
        f.write("-----------------------------------------------------\n\n")
        
        f.write(f"Key Insight: Detected a {abs(q3_decline_pct):.2f}% decline in Q3 2025 sales (${q3_2025_sales:,.2f}) compared to Q2 2025 (${q2_2025_sales:,.2f}).\n\n")
        
        f.write("2. PRODUCT CATEGORY METRICS:\n")
        f.write("-------------------------------------------------------------------------\n")
        f.write("Category          Sales ($)         Profit ($)        Net Margin (%)\n")
        f.write("-------------------------------------------------------------------------\n")
        for _, row in category_summary.iterrows():
            f.write(f"{row['Category']:<16}  ${row['Total_Sales']:,.2f}    ${row['Total_Profit']:,.2f}    {row['Net_Margin_%']:.2f}%\n")
        f.write("-------------------------------------------------------------------------\n")
        
    print(f"\n[5] Analysis completed successfully. Report saved to '{report_file}'.")
    print("=========================================================")

if __name__ == "__main__":
    run_analysis()
