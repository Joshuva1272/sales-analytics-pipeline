import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_FILE = "db/sales_analytics.db"
FIG_DIR = "outputs/figures"

os.makedirs(FIG_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")


def sales_by_region():
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT region, SUM(sales) AS total_sales
        FROM sales
        GROUP BY region
        ORDER BY total_sales DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="region", y="total_sales")
    plt.title("Sales by Region")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/sales_by_region.png")
    plt.close()


def monthly_sales_trend():
    conn = sqlite3.connect(DB_FILE)
    query = """
        SELECT
            order_year,
            order_month,
            SUM(sales) AS monthly_sales
        FROM sales
        GROUP BY order_year, order_month
        ORDER BY order_year, order_month;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df["year_month"] = df["order_year"].astype(str) + "-" + df["order_month"].astype(str).str.zfill(2)

    plt.figure(figsize=(12, 5))
    sns.lineplot(data=df, x="year_month", y="monthly_sales", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{FIG_DIR}/monthly_sales_trend.png")
    plt.close()


if __name__ == "__main__":
    sales_by_region()
    monthly_sales_trend()