/*
  Delivery Performance Analysis

  This analysis measures delivery speed, late delivery rate,
  and the relationship between delivery delays and customer review scores.
*/

-- 1. Average delivery time in days
SELECT
    ROUND(
        AVG(order_delivered_customer_date::date - order_purchase_timestamp::date)::numeric,
        2
    ) AS avg_delivery_days
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL;


-- 2. Late delivery rate
SELECT
    ROUND(
        100.0 * SUM(
            CASE
                WHEN order_delivered_customer_date::timestamp > order_estimated_delivery_date::timestamp
                THEN 1 ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS late_delivery_rate_percentage
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;


-- 3. Average review score by delivery status
SELECT
    CASE
        WHEN o.order_delivered_customer_date::timestamp > o.order_estimated_delivery_date::timestamp
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,
    ROUND(AVG(r.review_score)::numeric, 2) AS avg_review_score,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
JOIN order_reviews r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  AND r.review_score IS NOT NULL
GROUP BY delivery_status
ORDER BY avg_review_score;
