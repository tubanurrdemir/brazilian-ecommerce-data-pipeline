/* E-Commerce Cohort & Retention Analysis
  Grouping customers by their first purchase month (Cohort) and 
  measuring their repeat purchase behavior (Retention) in the following months.
*/

-- STEP 1: Find the FIRST purchase month for each customer
WITH customer_first_purchase AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', MIN(o.order_purchase_timestamp)) AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
),

-- STEP 2: Map all customer orders to their respective first purchase month (cohort)
activity AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        fp.cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN customer_first_purchase fp ON c.customer_unique_id = fp.customer_unique_id
)

-- STEP 3: Calculate the number of months passed since the first purchase and count active customers
SELECT 
    cohort_month,
    -- Mathematical formula to calculate the exact MONTH difference between two dates
    (EXTRACT(YEAR FROM order_month) - EXTRACT(YEAR FROM cohort_month)) * 12 + 
    (EXTRACT(MONTH FROM order_month) - EXTRACT(MONTH FROM cohort_month)) AS month_index,
    COUNT(DISTINCT customer_unique_id) AS active_customers
FROM activity
GROUP BY cohort_month, month_index
ORDER BY cohort_month, month_index;
