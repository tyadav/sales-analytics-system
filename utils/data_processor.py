import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    Returns: float (sum of Quantity * UnitPrice)
    """
    return sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)

def analyze_sales(df):
    """
    Aggregates sales data by product, customer, and region.
    Returns: dictionary of summaries
    """
    product_summary = df.groupby("ProductName")["Revenue"].sum().reset_index().sort_values(by="Revenue", ascending=False)
    customer_summary = df.groupby("CustomerID")["Revenue"].sum().reset_index().sort_values(by="Revenue", ascending=False)
    region_summary = df.groupby("Region")["Revenue"].sum().reset_index().sort_values(by="Revenue", ascending=False)

    return {
        "product_summary": product_summary,
        "customer_summary": customer_summary,
        "region_summary": region_summary
    }
    
def average_order_value(transactions):
    """
    Calculates the average order value.

    Parameters:
    - transactions: list of transaction dictionaries

    Returns:
    - float: average revenue per transaction
    """
    if not transactions:
        return 0.0
    total = sum(tx["Quantity"] * tx["UnitPrice"] for tx in transactions)
    return total / len(transactions)
    
def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Parameters:
    - transactions: list of dictionaries with keys: CustomerID, Quantity, UnitPrice, ProductName

    Returns:
    - dict: customer statistics sorted by total_spent descending
    """
    from collections import defaultdict

    stats = defaultdict(lambda: {
        "total_spent": 0.0,
        "purchase_count": 0,
        "products_bought": set()
    })

    # Aggregate stats
    for tx in transactions:
        cid = tx["CustomerID"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        stats[cid]["total_spent"] += amount
        stats[cid]["purchase_count"] += 1
        stats[cid]["products_bought"].add(tx["ProductName"])

    # Finalize stats with avg_order_value and list conversion
    for cid in stats:
        total = stats[cid]["total_spent"]
        count = stats[cid]["purchase_count"]
        stats[cid]["avg_order_value"] = round(total / count, 2)
        stats[cid]["products_bought"] = sorted(stats[cid]["products_bought"])

    # Sort by total_spent descending
    sorted_stats = dict(sorted(stats.items(), key=lambda item: item[1]["total_spent"], reverse=True))

    return sorted_stats

def region_performance(transactions):
    """
    Calculates region-wise performance.

    Returns: DataFrame with Region, Sales, Transactions
    """
    df = pd.DataFrame(transactions)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    region_stats = (
        df.groupby("Region")
        .agg(Sales=("Revenue", "sum"), Transactions=("TransactionID", "count"))
        .reset_index()
        .sort_values("Sales", ascending=False)
    )
    return region_stats

def top_products(transactions, n=5):
    """
    Finds top N products by revenue.

    Returns: DataFrame with ProductName, Quantity, Revenue
    """
    df = pd.DataFrame(transactions)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    product_stats = (
        df.groupby("ProductName")
        .agg(Quantity=("Quantity", "sum"), Revenue=("Revenue", "sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(n)
    )
    return product_stats

def top_customers(transactions, n=5):
    """
    Finds top N customers by total spend.

    Returns: DataFrame with CustomerID, TotalSpent, Orders
    """
    df = pd.DataFrame(transactions)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    customer_stats = (
        df.groupby("CustomerID")
        .agg(TotalSpent=("Revenue", "sum"), Orders=("TransactionID", "count"))
        .reset_index()
        .sort_values("TotalSpent", ascending=False)
        .head(n)
    )
    return customer_stats

def daily_sales_stats(transactions):
    """
    Calculates daily sales trend.

    Returns: DataFrame with Date, Revenue, Transactions, UniqueCustomers
    """
    df = pd.DataFrame(transactions)
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    daily_stats = (
        df.groupby("Date")
        .agg(Revenue=("Revenue", "sum"),
             Transactions=("TransactionID", "count"),
             UniqueCustomers=("CustomerID", "nunique"))
        .reset_index()
        .sort_values("Date")
    )
    return daily_stats


def generate_report(analysis, output_path="output/report.txt"):
    """
    Writes a text report summarizing sales analysis.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("Sales Summary Report\n")
        f.write("====================\n\n")

        f.write("Top Products:\n")
        for _, row in analysis["product_summary"].head(5).iterrows():
            f.write(f"- {row['ProductName']}: ₹{row['Revenue']:.2f}\n")
        f.write("\n")

        f.write("Top Customers:\n")
        for _, row in analysis["customer_summary"].head(5).iterrows():
            f.write(f"- {row['CustomerID']}: ₹{row['Revenue']:.2f}\n")
        f.write("\n")

        f.write("Regional Sales:\n")
        for _, row in analysis["region_summary"].iterrows():
            f.write(f"- {row['Region']}: ₹{row['Revenue']:.2f}\n")
            
def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date.

    Parameters:
    - transactions: list of dictionaries with keys: Date, CustomerID, Quantity, UnitPrice

    Returns:
    - dict: {date: {revenue, transaction_count, unique_customers}}
    """
    from collections import defaultdict

    daily_stats = defaultdict(lambda: {
        "revenue": 0.0,
        "transaction_count": 0,
        "unique_customers": set()
    })

    # Aggregate by date
    for tx in transactions:
        date = tx["Date"]
        amount = tx["Quantity"] * tx["UnitPrice"]
        daily_stats[date]["revenue"] += amount
        daily_stats[date]["transaction_count"] += 1
        daily_stats[date]["unique_customers"].add(tx["CustomerID"])

    # Finalize stats (convert sets to counts)
    for date in daily_stats:
        daily_stats[date]["unique_customers"] = len(daily_stats[date]["unique_customers"])

    # Sort chronologically
    sorted_stats = dict(sorted(daily_stats.items(), key=lambda item: item[0]))

    return sorted_stats

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue.

    Parameters:
    - transactions: list of dictionaries with keys: Date, CustomerID, Quantity, UnitPrice

    Returns:
    - tuple: (date, revenue, transaction_count)
    """
    daily_stats = daily_sales_trend(transactions)

    # Find max revenue day
    peak_date, peak_data = max(daily_stats.items(), key=lambda item: item[1]["revenue"])

    return (peak_date, peak_data["revenue"], peak_data["transaction_count"])

def generate_charts(analysis, output_dir="output"):
    """
    Generates bar and pie charts for sales summaries.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Top Products Bar Chart
    top_products = analysis["product_summary"].head(5)
    plt.figure(figsize=(8, 5))
    plt.bar(top_products["ProductName"], top_products["Revenue"], color="skyblue")
    plt.title("Top 5 Products by Revenue")
    plt.xlabel("Product")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_products.png"))
    plt.close()

    # Top Customers Bar Chart
    top_customers = analysis["customer_summary"].head(5)
    plt.figure(figsize=(8, 5))
    plt.bar(top_customers["CustomerID"], top_customers["Revenue"], color="lightgreen")
    plt.title("Top 5 Customers by Spend")
    plt.xlabel("Customer ID")
    plt.ylabel("Revenue (₹)")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "top_customers.png"))
    plt.close()

    # Regional Sales Pie Chart
    regions = analysis["region_summary"]
    plt.figure(figsize=(6, 6))
    plt.pie(regions["Revenue"], labels=regions["Region"], autopct="%1.1f%%", startangle=140)
    plt.title("Regional Sales Distribution")
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "regional_sales.png"))
    plt.close()
    
def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales.

    Parameters:
    - transactions: list of dictionaries with keys: ProductName, Quantity, UnitPrice
    - threshold: minimum quantity to be considered "low performing"

    Returns:
    - list of tuples: (ProductName, TotalQuantity, TotalRevenue)
    """
    from collections import defaultdict

    product_stats = defaultdict(lambda: {"quantity": 0, "revenue": 0.0})

    # Aggregate stats per product
    for tx in transactions:
        pname = tx["ProductName"]
        qty = tx["Quantity"]
        amount = qty * tx["UnitPrice"]

        product_stats[pname]["quantity"] += qty
        product_stats[pname]["revenue"] += amount

    # Filter products below threshold
    low_products = [
        (pname, stats["quantity"], stats["revenue"])
        for pname, stats in product_stats.items()
        if stats["quantity"] < threshold
    ]

    # Sort by total quantity ascending
    low_products.sort(key=lambda x: x[1])

    return low_products

    
def generate_daily_sales_chart(daily_stats, output_dir="output"):
    """
    Generates a line chart of daily sales revenue over time.

    Parameters:
    - daily_stats: dict returned by daily_sales_trend()
    - output_dir: folder to save chart
    """
    import matplotlib.pyplot as plt
    import os

    os.makedirs(output_dir, exist_ok=True)

    # Extract dates and revenues
    dates = list(daily_stats.keys())
    revenues = [daily_stats[date]["revenue"] for date in dates]

    # Plot line chart
    plt.figure(figsize=(10, 5))
    plt.plot(dates, revenues, marker="o", linestyle="-", color="blue")
    plt.title("Daily Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Revenue (₹)")
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Save chart
    plt.savefig(os.path.join(output_dir, "daily_sales_trend.png"))
    plt.close()
    
def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report with 8 sections.
    """

    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(transactions)
    enriched_df = pd.DataFrame(enriched_transactions)

    # 1. HEADER
    total_records = len(transactions)
    generation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 2. OVERALL SUMMARY
    df["Revenue"] = df["Quantity"] * df["UnitPrice"]
    total_revenue = df["Revenue"].sum()
    total_transactions = len(df)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0
    date_range = f"{df['Date'].min()} to {df['Date'].max()}"

    # 3. REGION-WISE PERFORMANCE
    region_stats = (
        df.groupby("Region")
        .agg(Sales=("Revenue", "sum"), Transactions=("TransactionID", "count"))
        .reset_index()
    )
    region_stats["PctTotal"] = (region_stats["Sales"] / total_revenue) * 100
    region_stats = region_stats.sort_values("Sales", ascending=False)

    # 4. TOP 5 PRODUCTS
    product_stats = (
        df.groupby("ProductName")
        .agg(Quantity=("Quantity", "sum"), Revenue=("Revenue", "sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
        .head(5)
    )

    # 5. TOP 5 CUSTOMERS
    customer_stats = (
        df.groupby("CustomerID")
        .agg(TotalSpent=("Revenue", "sum"), Orders=("TransactionID", "count"))
        .reset_index()
        .sort_values("TotalSpent", ascending=False)
        .head(5)
    )

    # 6. DAILY SALES TREND
    daily_stats = (
        df.groupby("Date")
        .agg(Revenue=("Revenue", "sum"),
             Transactions=("TransactionID", "count"),
             UniqueCustomers=("CustomerID", "nunique"))
        .reset_index()
        .sort_values("Date")
    )

    # 7. PRODUCT PERFORMANCE ANALYSIS
    # Best selling day
    peak_day = daily_stats.loc[daily_stats["Revenue"].idxmax()]
    # Low performing products
    low_products = (
        df.groupby("ProductName")
        .agg(Quantity=("Quantity", "sum"), Revenue=("Revenue", "sum"))
        .reset_index()
    )
    low_products = low_products[low_products["Quantity"] < 10].sort_values("Quantity")
    # Avg transaction value per region
    avg_tx_region = (
        df.groupby("Region")
        .agg(AvgTxValue=("Revenue", "mean"))
        .reset_index()
    )

    # 8. API ENRICHMENT SUMMARY
    enriched_count = enriched_df["API_Match"].sum()
    total_enriched = len(enriched_df)
    success_rate = (enriched_count / total_enriched * 100) if total_enriched else 0
    failed_products = enriched_df.loc[~enriched_df["API_Match"], "ProductName"].unique()

    # ---------------- WRITE REPORT ----------------
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("============================================\n")
        f.write("           SALES ANALYTICS REPORT\n")
        f.write(f"         Generated: {generation_time}\n")
        f.write(f"         Records Processed: {total_records}\n")
        f.write("============================================\n\n")

        # OVERALL SUMMARY
        f.write("OVERALL SUMMARY\n")
        f.write("--------------------------------------------\n")
        f.write(f"Total Revenue:        ₹{total_revenue:,.2f}\n")
        f.write(f"Total Transactions:   {total_transactions}\n")
        f.write(f"Average Order Value:  ₹{avg_order_value:,.2f}\n")
        f.write(f"Date Range:           {date_range}\n\n")

        # REGION-WISE PERFORMANCE
        f.write("REGION-WISE PERFORMANCE\n")
        f.write("--------------------------------------------\n")
        f.write("Region    Sales         % of Total  Transactions\n")
        for _, row in region_stats.iterrows():
            f.write(f"{row['Region']:<8} ₹{row['Sales']:,.0f}   {row['PctTotal']:.2f}%      {row['Transactions']}\n")
        f.write("\n")

        # TOP 5 PRODUCTS
        f.write("TOP 5 PRODUCTS\n")
        f.write("--------------------------------------------\n")
        f.write("Rank  Product Name        Quantity   Revenue\n")
        for i, row in enumerate(product_stats.itertuples(), start=1):
            f.write(f"{i:<5}{row.ProductName:<18}{row.Quantity:<10}{'₹'+format(row.Revenue, ',.0f')}\n")
        f.write("\n")

        # TOP 5 CUSTOMERS
        f.write("TOP 5 CUSTOMERS\n")
        f.write("--------------------------------------------\n")
        f.write("Rank  Customer ID   Total Spent   Orders\n")
        for i, row in enumerate(customer_stats.itertuples(), start=1):
            f.write(f"{i:<5}{row.CustomerID:<13}₹{row.TotalSpent:,.0f}   {row.Orders}\n")
        f.write("\n")

        # DAILY SALES TREND
        f.write("DAILY SALES TREND\n")
        f.write("--------------------------------------------\n")
        f.write("Date         Revenue       Transactions   Unique Customers\n")
        for _, row in daily_stats.iterrows():
            f.write(f"{row['Date']}   ₹{row['Revenue']:,.0f}   {row['Transactions']}   {row['UniqueCustomers']}\n")
        f.write("\n")

        # PRODUCT PERFORMANCE ANALYSIS
        f.write("PRODUCT PERFORMANCE ANALYSIS\n")
        f.write("--------------------------------------------\n")
        f.write(f"Best Selling Day: {peak_day['Date']} (₹{peak_day['Revenue']:,.0f}, {peak_day['Transactions']} transactions)\n")
        f.write("Low Performing Products:\n")
        for _, row in low_products.iterrows():
            f.write(f"  {row['ProductName']} - Qty={row['Quantity']}, Revenue=₹{row['Revenue']:,.0f}\n")
        f.write("Average Transaction Value per Region:\n")
        for _, row in avg_tx_region.iterrows():
            f.write(f"  {row['Region']}: ₹{row['AvgTxValue']:,.2f}\n")
        f.write("\n")

        # API ENRICHMENT SUMMARY
        f.write("API ENRICHMENT SUMMARY\n")
        f.write("--------------------------------------------\n")
        f.write(f"Total Products Enriched: {enriched_count}/{total_enriched}\n")
        f.write(f"Success Rate: {success_rate:.2f}%\n")
        f.write("Failed Products:\n")
        for p in failed_products:
            f.write(f"  {p}\n")
        f.write("\n")

    print(f"✅ Sales report generated at {output_file}")

def export_to_excel(analysis, output_path="output/report.xlsx"):
    """
    Exports sales analysis summaries to an Excel file with separate sheets.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with pd.ExcelWriter(output_path, engine="xlsxwriter") as writer:
        analysis["product_summary"].to_excel(writer, sheet_name="Top Products", index=False)
        analysis["customer_summary"].to_excel(writer, sheet_name="Top Customers", index=False)
        analysis["region_summary"].to_excel(writer, sheet_name="Regional Sales", index=False)

    print(f"Excel report saved to {output_path}")   
