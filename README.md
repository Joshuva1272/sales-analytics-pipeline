# Superstore Sales Analytics Pipeline

## Business Problem
The Superstore management needs a robust data pipeline to understand regional performance, product profitability, and sales trends. Currently, the data is siloed in Excel files, making it difficult to perform year-over-year analysis and identify loss-making segments.

## Methodology
1.  **ETL Pipeline**: Developed `scripts/etl.py` to:
    *   Load raw data from Excel (`Orders`, `Returns`, `People` sheets).
    *   Clean and standardize column names.
    *   Calculate derived metrics (Ship Delay, Profit Margin).
    *   Load cleaned data into a SQLite database (`db/sales_analytics.db`).
2.  **SQL Analysis**: Executed 10 business-critical queries in `analysis.sql` to extract insights.
3.  **Visualization**: Built a performance dashboard using Matplotlib and Seaborn (`scripts/dashboard.py`).

## Key Findings
*   **Profit Leaders**: **Technology** is the most profitable category ($188k), with **California** and **New York** being the top states.
*   **Regional Disparity**: The **West** region leads in profit ($162k), whereas the **Central** region lags significantly ($20k), primarily due to high average discounts (25%).
*   **Loss-Making Products**: **Tables** (-$23k) and **Bookcases** (-$3.6k) are consistently underperforming and eroding overall margins.
*   **Growth Trends**: The business saw a massive revenue surge in 2021 (+44% YoY).
*   **Seasonality**: Sales peak sharply in **Q4** (Sept, Nov, Dec), indicating strong holiday demand.

## Recommendations
1.  **Review Pricing in Central Region**: Reduce the average discount in the Central region to align with other regions and improve profitability.
2.  **Address Furniture Margins**: Investigate the cost structure or discount strategy for Tables and Bookcases. If profitability cannot be improved, consider phasing out these lines.
3.  **Double Down on Technology**: Allocate more marketing budget to high-margin Technology products (especially Copiers and Phones).
4.  **Incentivize Early Q4 Purchases**: Implement loyalty programs in October to smooth out the transition into the peak holiday season.

