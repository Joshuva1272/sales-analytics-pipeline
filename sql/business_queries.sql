-- 1. Total sales, profit, and orders
SELECT
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM sales;

-- 2. Sales by region
SELECT
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- 3. Top 10 products by sales
SELECT
    product_name,
    ROUND(SUM(sales), 2) AS total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- 4. Top 10 products by profit
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name
ORDER BY total_profit DESC
LIMIT 10;

-- 5. Bottom 10 products by profit
SELECT
    product_name,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY product_name
ORDER BY total_profit ASC
LIMIT 10;

-- 6. Sales and profit by category and sub-category
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM sales
GROUP BY category, sub_category
ORDER BY total_sales DESC;

-- 7. Year-over-year sales growth
WITH yearly_sales AS (
    SELECT
        order_year,
        SUM(sales) AS total_sales
    FROM sales
    GROUP BY order_year
)
SELECT
    order_year,
    ROUND(total_sales, 2) AS total_sales,
    ROUND(
        ((total_sales - LAG(total_sales) OVER (ORDER BY order_year)) * 100.0)
        / LAG(total_sales) OVER (ORDER BY order_year),
        2
    ) AS yoy_growth_pct
FROM yearly_sales
ORDER BY order_year;

-- 8. Monthly sales trend
SELECT
    order_year,
    order_month,
    ROUND(SUM(sales), 2) AS monthly_sales,
    ROUND(SUM(profit), 2) AS monthly_profit
FROM sales
GROUP BY order_year, order_month
ORDER BY order_year, order_month;

-- 9. Return rate by region
SELECT
    region,
    COUNT(*) AS total_rows,
    SUM(returned_flag) AS returned_rows,
    ROUND(SUM(returned_flag) * 100.0 / COUNT(*), 2) AS return_rate_pct
FROM sales
GROUP BY region
ORDER BY return_rate_pct DESC;

-- 10. Average shipping delay by ship mode
SELECT
    ship_mode,
    ROUND(AVG(ship_delay_days), 2) AS avg_ship_delay_days
FROM sales
GROUP BY ship_mode
ORDER BY avg_ship_delay_days DESC;