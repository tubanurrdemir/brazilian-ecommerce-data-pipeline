/*
  E-Commerce Master Table Creation
  This query joins the cleaned tables (orders, payments, customers) 
  to create a single, optimized Master View for the Tableau Dashboard.
*/

CREATE OR REPLACE VIEW master_satis_tablosu AS
SELECT 
    o.order_id,
    o.order_purchase_timestamp AS siparis_tarihi,
    p.payment_type AS odeme_turu,
    p.payment_value AS odenen_tutar,
    c.customer_state AS musteri_eyaleti
FROM orders o
JOIN order_payments p ON o.order_id = p.order_id
JOIN customers c ON o.customer_id = c.customer_id;
