-- 1. Top 10 products by sales
SELECT product_name, SUM(sales) as total_sales
FROM sales
GROUP BY product_name
ORDER BY total_sales DESC
LIMIT 10;

-- 2. Profitability by region
SELECT region, SUM(profit) as total_profit
FROM sales
GROUP BY region
ORDER BY total_profit DESC;

-- 3. Year-over-Year (YoY) growth
WITH annual_sales AS (
    SELECT order_year, SUM(sales) as total_sales
    FROM sales
    GROUP BY order_year
)
SELECT 
    order_year, 
    total_sales,
    LAG(total_sales) OVER (ORDER BY order_year) as prev_year_sales,
    ((total_sales - LAG(total_sales) OVER (ORDER BY order_year)) / LAG(total_sales) OVER (ORDER BY order_year)) * 100 as yoy_growth_pct
FROM annual_sales;

-- 4. Sales/Profit by Category
SELECT category, SUM(sales) as total_sales, SUM(profit) as total_profit
FROM sales
GROUP BY category
ORDER BY total_sales DESC;

-- 5. Top 5 most profitable States
SELECT state, SUM(profit) as total_profit
FROM sales
GROUP BY state
ORDER BY total_profit DESC
LIMIT 5;

-- 6. Sales by Segment
SELECT segment, SUM(sales) as total_sales
FROM sales
GROUP BY segment
ORDER BY total_sales DESC;

-- 7. Average Discount per Region
SELECT region, AVG(discount) as avg_discount
FROM sales
GROUP BY region
ORDER BY avg_discount DESC;

-- 8. Monthly sales seasonality
SELECT order_month, order_month_name, SUM(sales) as total_sales
FROM sales
GROUP BY order_month, order_month_name
ORDER BY order_month;

-- 9. Shipping mode efficiency (Avg ship delay and profit)
SELECT ship_mode, AVG(ship_delay_days) as avg_delay, AVG(profit) as avg_profit
FROM sales
GROUP BY ship_mode
ORDER BY avg_profit DESC;

-- 10. Bottom 5 sub-categories by profit
SELECT sub_category, SUM(profit) as total_profit
FROM sales
GROUP BY sub_category
ORDER BY total_profit ASC
LIMIT 5;
