import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DB_FILE = "db/sales_analytics.db"
OUTPUT_IMAGE = "outputs/dashboard_report.png"

def main():
    os.makedirs("outputs", exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    conn.close()

    # Set styling
    sns.set_theme(style="whitegrid")
    fig, axes = plt.subplots(2, 2, figsize=(20, 15))
    fig.suptitle("Superstore Performance Dashboard", fontsize=24, fontweight='bold')

    # 1. Overview: Sales by Segment
    segment_sales = df.groupby('segment')['sales'].sum().reset_index()
    sns.barplot(x='segment', y='sales', data=segment_sales, ax=axes[0, 0], palette="viridis")
    axes[0, 0].set_title("Total Sales by Segment", fontsize=16)
    axes[0, 0].set_ylabel("Sales ($)")

    # 2. Product: Sales by Category
    cat_sales = df.groupby('category')['sales'].sum().reset_index()
    sns.barplot(x='category', y='sales', data=cat_sales, ax=axes[0, 1], palette="magma")
    axes[0, 1].set_title("Total Sales by Category", fontsize=16)
    axes[0, 1].set_ylabel("Sales ($)")

    # 3. Region: Profit by Region
    region_profit = df.groupby('region')['profit'].sum().reset_index()
    sns.barplot(x='region', y='profit', data=region_profit, ax=axes[1, 0], palette="rocket")
    axes[1, 0].set_title("Total Profit by Region", fontsize=16)
    axes[1, 0].set_ylabel("Profit ($)")

    # 4. Trend: Monthly Sales
    monthly_sales = df.groupby(['order_year', 'order_month'])['sales'].sum().reset_index()
    monthly_sales['period'] = monthly_sales['order_year'].astype(str) + "-" + monthly_sales['order_month'].astype(str).str.zfill(2)
    sns.lineplot(x='period', y='sales', data=monthly_sales, ax=axes[1, 1], marker='o', color='teal')
    axes[1, 1].set_title("Monthly Sales Trend", fontsize=16)
    axes[1, 1].set_ylabel("Sales ($)")
    plt.setp(axes[1, 1].get_xticklabels(), rotation=45)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.savefig(OUTPUT_IMAGE)
    print(f"Dashboard saved to: {OUTPUT_IMAGE}")

if __name__ == "__main__":
    main()
