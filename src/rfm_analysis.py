"""
RFM Analysis - End-to-End Pipeline
This script connects to PostgreSQL, extracts customer order data, 
calculates RFM metrics, assigns scores, segments customers using Regex, 
and generates an executive summary report for business intelligence.
"""

import os
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine
from dotenv import load_dotenv
# -------------------------------------------------------------------
# 1. DATABASE CONNECTION
# -------------------------------------------------------------------
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DB_URL)
print("Database connection successful. Ready for RFM analysis!")
# -------------------------------------------------------------------
# 2. SQL QUERY (Data Processing)
# -------------------------------------------------------------------
sql_query = """
SELECT 
    c.customer_unique_id,
    o.order_id,
    o.order_purchase_timestamp,
    p.payment_value
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_payments p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered';
"""

# -------------------------------------------------------------------
# 3. DATA EXTRACTION
# -------------------------------------------------------------------
print("Fetching data from the database... This might take a few seconds.")
df = pd.read_sql(sql_query, engine)

# -------------------------------------------------------------------
# 4. RFM CALCULATION (Data Transformation)
# -------------------------------------------------------------------
df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
analysis_date = df['order_purchase_timestamp'].max() + dt.timedelta(days=1)

rfm = df.groupby('customer_unique_id').agg({
    'order_purchase_timestamp': lambda x: (analysis_date - x.max()).days, # Recency
    'order_id': 'nunique',                                                # Frequency
    'payment_value': 'sum'                                                # Monetary
}).reset_index()

rfm.columns = ['customer_unique_id', 'Recency', 'Frequency', 'Monetary']

# -------------------------------------------------------------------
# 5. RFM SCORING (Assigning 1-5 Scores)
# -------------------------------------------------------------------
# Recency: Lower days = Higher score (5 to 1)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency: Using 'rank' to handle tied values
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Monetary: Standard logic (1 to 5)
rfm['M_Score'] = pd.qcut(rfm['Monetary'], 5, labels=[1, 2, 3, 4, 5])

rfm['RFM_Segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)

# -------------------------------------------------------------------
# 6. CUSTOMER SEGMENTATION (Naming the Segments via Regex)
# -------------------------------------------------------------------
seg_map = {
    r'[1-2][1-2]': 'Hibernating',
    r'[1-2][3-4]': 'At_Risk',
    r'[1-2]5': 'Cant_Lose',
    r'3[1-2]': 'About_to_Sleep',
    r'33': 'Need_Attention',
    r'[3-4][4-5]': 'Loyal_Customers',
    r'41': 'Promising',
    r'51': 'New_Customers',
    r'[4-5][2-3]': 'Potential_Loyalists',
    r'5[4-5]': 'Champions'
}

rfm['segment'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str)
rfm['segment'] = rfm['segment'].replace(seg_map, regex=True)

# -------------------------------------------------------------------
# 7. FINAL SUMMARY REPORT (Business Intelligence)
# -------------------------------------------------------------------
rfm_summary = rfm.groupby('segment').agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': ['mean', 'count']
}).round(2)

rfm_summary.columns = ['Avg_Recency', 'Avg_Frequency', 'Avg_Monetary', 'Customer_Count']
rfm_summary = rfm_summary.sort_values(by='Customer_Count', ascending=False)

print("\n--- FINAL RFM SEGMENTATION REPORT ---")
print(rfm_summary)

# Export the final summary to a CSV file for management
os.makedirs("reports", exist_ok=True)
rfm_summary.to_csv('reports/rfm_summary_report.csv')

print("\nSUCCESS: The final report has been saved as 'reports/rfm_summary_report.csv' in your project folder!")
