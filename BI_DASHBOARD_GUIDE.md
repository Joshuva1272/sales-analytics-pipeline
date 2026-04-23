# Superstore Dashboard Build Guide

This guide provides instructions to replicate the analytics suite in **Power BI** or **Tableau** using the cleaned data from our pipeline.

## 1. Data Connection
### Option A: Cleaned CSV (Recommended for Quick Setup)
*   **Source**: `data/processed/superstore_clean.csv`
*   In Power BI: `Get Data` -> `Text/CSV`.
*   In Tableau: `Connect` -> `To a File` -> `Text File`.

### Option B: SQLite Database (Live Connection)
*   **Source**: `db/sales_analytics.db`
*   **Power BI**: Requires "ODBC" connection. Install the SQLite ODBC Driver, then `Get Data` -> `ODBC`.
*   **Tableau**: `Connect` -> `To a Server` -> `Other Databases (ODBC)`.

---

## 2. Dashboard Structure

### A. Overview Page
*   **KPI Cards**:
    *   `Total Sales`: `SUM(sales)`
    *   `Total Profit`: `SUM(profit)`
    *   `Order Count`: `DISTINCTCOUNT(order_id)`
    *   `Profit Margin %`: `SUM(profit) / SUM(sales)` (Format as %)
*   **Visuals**:
    *   **Donut Chart**: Sales by Category.
    *   **Bar Chart**: Sales by Segment.
    *   **Tree Map**: Sales by Sub-Category.

### B. Product Performance Page
*   **Bar Chart (Horizontal)**: Top 10 Products by Sales.
*   **Bar Chart (Horizontal)**: Top 10 Products by Profit.
*   **Bar Chart (Horizontal)**: Bottom 10 Products by Profit (Identifying losses).
*   **Scatter Plot**: Sales vs. Profit by Sub-Category.

### C. Regional Analysis Page
*   **Map**: State map with `Profit` as the color saturation.
*   **Bar Chart**: Sales vs. Profit by Region.
*   **Table**: Return Rate by Region.
    *   *Formula*: `SUM(returned_flag) / COUNT(order_id)`

### D. Trend Analysis Page
*   **Line Chart**: Monthly Sales and Profit Trend.
    *   Axis: `order_date` (Year-Month hierarchy).
    *   Values: `SUM(sales)`, `SUM(profit)`.
*   **YoY Growth Chart**:
    *   *Power BI DAX*: 
        ```dax
        YoY Sales Growth = 
        VAR CurrentYearSales = SUM(sales)
        VAR PreviousYearSales = CALCULATE(SUM(sales), SAMEPERIODLASTYEAR(order_date))
        RETURN DIVIDE(CurrentYearSales - PreviousYearSales, PreviousYearSales)
        ```
*   **Scatter Plot**: Discount vs. Profit Margin to see correlation.

---

## 3. Global Slicers (Filters)
Add a sidebar or top header with the following slicers applied to **all pages**:
1.  **Year** (`order_year`)
2.  **Region** (`region`)
3.  **Category** (`category`)
4.  **Segment** (`segment`)
5.  **Ship Mode** (`ship_mode`)

---

## 4. Key Metrics Calculation Reference
| Metric | Logic |
| :--- | :--- |
| **Profit Margin** | `[Total Profit] / [Total Sales]` |
| **Return Rate** | `[Returned Count] / [Total Orders]` |
| **Avg Ship Delay** | `AVERAGE(ship_delay_days)` |
| **Sales per Order** | `[Total Sales] / [Total Orders]` |
