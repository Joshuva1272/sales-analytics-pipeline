import os
import sqlite3
import pandas as pd

RAW_FILE = "data/raw/Superstore.xls"
PROCESSED_CSV = "data/processed/superstore_clean.csv"
DB_FILE = "db/sales_analytics.db"


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def load_excel_sheets(file_path: str):
    orders = pd.read_excel(file_path, sheet_name="Orders")
    returns = pd.read_excel(file_path, sheet_name="Returns")
    people = pd.read_excel(file_path, sheet_name="People")
    return orders, returns, people


def clean_orders(orders: pd.DataFrame) -> pd.DataFrame:
    orders = standardize_column_names(orders)

    # Remove duplicates
    orders = orders.drop_duplicates()

    # Convert dates
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["ship_date"] = pd.to_datetime(orders["ship_date"], errors="coerce")

    # Handle missing postal code if any
    if "postal_code" in orders.columns:
        orders["postal_code"] = orders["postal_code"].fillna(0).astype(int)

    # Create derived columns
    orders["order_year"] = orders["order_date"].dt.year
    orders["order_month"] = orders["order_date"].dt.month
    orders["order_month_name"] = orders["order_date"].dt.strftime("%b")
    orders["ship_delay_days"] = (orders["ship_date"] - orders["order_date"]).dt.days

    # Profit margin
    orders["profit_margin_pct"] = (orders["profit"] / orders["sales"]) * 100
    orders["profit_margin_pct"] = orders["profit_margin_pct"].round(2)

    return orders


def clean_returns(returns: pd.DataFrame) -> pd.DataFrame:
    returns = standardize_column_names(returns)
    return returns


def clean_people(people: pd.DataFrame) -> pd.DataFrame:
    people = standardize_column_names(people)
    return people


def merge_data(orders: pd.DataFrame, returns: pd.DataFrame, people: pd.DataFrame) -> pd.DataFrame:
    # Mark returned orders
    if "order_id" in returns.columns:
        returns["returned_flag"] = 1
        orders = orders.merge(
            returns[["order_id", "returned_flag"]],
            on="order_id",
            how="left"
        )
    else:
        orders["returned_flag"] = 0

    orders["returned_flag"] = orders["returned_flag"].fillna(0).astype(int)

    # Add regional manager from People sheet
    if "region" in people.columns:
        orders = orders.merge(
            people,
            on="region",
            how="left"
        )

    return orders


def load_to_sqlite(df: pd.DataFrame, db_path: str):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)

    df.to_sql("sales", conn, if_exists="replace", index=False)

    # Helpful indexes
    conn.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON sales(order_date);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_region ON sales(region);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_category ON sales(category);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_sub_category ON sales(sub_category);")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_product_name ON sales(product_name);")

    conn.commit()
    conn.close()


def main():
    os.makedirs("data/processed", exist_ok=True)

    orders, returns, people = load_excel_sheets(RAW_FILE)

    orders = clean_orders(orders)
    returns = clean_returns(returns)
    people = clean_people(people)

    final_df = merge_data(orders, returns, people)

    final_df.to_csv(PROCESSED_CSV, index=False)
    load_to_sqlite(final_df, DB_FILE)

    print("ETL complete.")
    print(f"Processed CSV saved to: {PROCESSED_CSV}")
    print(f"SQLite DB saved to: {DB_FILE}")
    print(f"Rows loaded: {len(final_df)}")


if __name__ == "__main__":
    main()