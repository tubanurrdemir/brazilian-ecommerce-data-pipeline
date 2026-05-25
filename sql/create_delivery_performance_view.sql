/*
  Delivery Performance View for Tableau

  This view prepares delivery-related metrics for Tableau visualization.
  It combines order delivery dates with customer review scores and creates
  calculated fields for delivery status and delivery duration.
*/

CREATE OR REPLACE VIEW vw_delivery_performance AS
SELECT
    o.order_id,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    r.review_score,
    CASE
        WHEN o.order_delivered_customer_date::timestamp > o.order_estimated_delivery_date::timestamp
        THEN 'Late'
        ELSE 'On Time'
    END AS delivery_status,
    (o.order_delivered_customer_date::date - o.order_purchase_timestamp::date) AS delivery_days
FROM orders o
JOIN order_reviews r
    ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  AND r.review_score IS NOT NULL;
