import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

required_vars = [DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]

if any(value is None for value in required_vars):
    raise ValueError("Missing database environment variables. Please check your .env file.")

database_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(database_url)

print("Database connection established successfully.")


# ---------------------------------------------------------
# 1. ORDERS TABLE CLEANING
# ---------------------------------------------------------

df_orders = pd.read_csv("olist_orders_dataset.csv")

# Convert order date columns from text to datetime format
df_orders["order_purchase_timestamp"] = pd.to_datetime(
    df_orders["order_purchase_timestamp"],
    errors="coerce"
)

df_orders["order_delivered_customer_date"] = pd.to_datetime(
    df_orders["order_delivered_customer_date"],
    errors="coerce"
)

df_orders["order_estimated_delivery_date"] = pd.to_datetime(
    df_orders["order_estimated_delivery_date"],
    errors="coerce"
)

# Keep only delivered orders with valid delivery dates.
# This cleaned table is used for delivery-based analytics.
df_orders = df_orders[
    (df_orders["order_status"] == "delivered") &
    (df_orders["order_delivered_customer_date"].notna()) &
    (df_orders["order_delivered_customer_date"] >= df_orders["order_purchase_timestamp"])
]

df_orders.to_sql("orders", engine, if_exists="replace", index=False)
print("orders table cleaned and loaded successfully.")


# ---------------------------------------------------------
# 2. ORDER PAYMENTS TABLE CLEANING
# ---------------------------------------------------------

df_payments = pd.read_csv("olist_order_payments_dataset.csv")

# Remove undefined payment records
df_payments = df_payments[df_payments["payment_type"] != "not_defined"]

df_payments.to_sql("order_payments", engine, if_exists="replace", index=False)
print("order_payments table cleaned and loaded successfully.")


# ---------------------------------------------------------
# 3. CUSTOMERS TABLE LOAD
# ---------------------------------------------------------

df_customers = pd.read_csv("olist_customers_dataset.csv")

df_customers.to_sql("customers", engine, if_exists="replace", index=False)
print("customers table loaded successfully.")


# ---------------------------------------------------------
# 4. ORDER ITEMS TABLE LOAD
# ---------------------------------------------------------

df_order_items = pd.read_csv("olist_order_items_dataset.csv")

df_order_items.to_sql("order_items", engine, if_exists="replace", index=False)
print("order_items table loaded successfully.")


# ---------------------------------------------------------
# 5. PRODUCTS TABLE LOAD
# ---------------------------------------------------------

df_products = pd.read_csv("olist_products_dataset.csv")

df_products.to_sql("products", engine, if_exists="replace", index=False)
print("products table loaded successfully.")


# ---------------------------------------------------------
# 6. ORDER REVIEWS TABLE LOAD
# ---------------------------------------------------------

df_reviews = pd.read_csv("olist_order_reviews_dataset.csv")

df_reviews.to_sql("order_reviews", engine, if_exists="replace", index=False)
print("order_reviews table loaded successfully.")


print("ETL process completed successfully.")
