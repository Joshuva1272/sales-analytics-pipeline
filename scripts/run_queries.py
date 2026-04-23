import sqlite3
import pandas as pd

DB_FILE = "db/sales_analytics.db"
SQL_FILE = "analysis.sql"

def main():
    conn = sqlite3.connect(DB_FILE)
    
    with open(SQL_FILE, 'r') as f:
        sql_content = f.read()
    
    # Split by semicolon to get individual queries
    queries = sql_content.split(';')
    
    for i, query in enumerate(queries):
        query = query.strip()
        if not query:
            continue
            
        print(f"\n--- Query {i+1} ---")
        try:
            df = pd.read_sql_query(query, conn)
            print(df)
        except Exception as e:
            print(f"Error executing query: {e}")
            
    conn.close()

if __name__ == "__main__":
    main()
