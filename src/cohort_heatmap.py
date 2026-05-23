"""
Cohort Analysis & Retention Heatmap (Percentage Based)
This script connects to the PostgreSQL database, calculates customer retention
using a SQL CTE, converts raw numbers to retention rates (%), and generates a heatmap.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# -------------------------------------------------------------------
# 1. DATABASE CONNECTION (ETL - Extract)
# -------------------------------------------------------------------
# Connects to the local PostgreSQL database using SQLAlchemy
engine = create_engine('postgresql://postgres:190719@localhost:5432/ecommerce_db')

# -------------------------------------------------------------------
# 2. SQL QUERY (Data Processing)
# -------------------------------------------------------------------
# Calculates the first purchase month (cohort) and the month index for subsequent purchases.
sql_query = """
WITH customer_first_purchase AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', MIN(o.order_purchase_timestamp)) AS cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_unique_id
),
activity AS (
    SELECT 
        c.customer_unique_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        fp.cohort_month
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    JOIN customer_first_purchase fp ON c.customer_unique_id = fp.customer_unique_id
)
SELECT 
    cohort_month,
    (EXTRACT(YEAR FROM order_month) - EXTRACT(YEAR FROM cohort_month)) * 12 + 
    (EXTRACT(MONTH FROM order_month) - EXTRACT(MONTH FROM cohort_month)) AS month_index,
    COUNT(DISTINCT customer_unique_id) AS active_customers
FROM activity
GROUP BY cohort_month, month_index
ORDER BY cohort_month, month_index;
"""

# -------------------------------------------------------------------
# 3. DATA EXTRACTION & TRANSFORMATION (Pandas)
# -------------------------------------------------------------------
# Execute the SQL query and store the result in a Pandas DataFrame
df = pd.read_sql(sql_query, engine)
print("Data successfully extracted from PostgreSQL.")

# Format the datetime to 'YYYY-MM' for cleaner heatmap labels
df['cohort_month'] = pd.to_datetime(df['cohort_month']).dt.strftime('%Y-%m')

# Create a pivot table (matrix) for the heatmap
# index: First purchase month, columns: Months passed, values: Number of active customers
cohort_pivot = df.pivot(index='cohort_month', columns='month_index', values='active_customers')
print("Pivot table successfully created.")

# -------------------------------------------------------------------
# 4. PERCENTAGE CONVERSION (Retention Rate)
# -------------------------------------------------------------------
# Divide each cell by the value in the first column (month 0) to get the retention percentage
retention_matrix = cohort_pivot.divide(cohort_pivot[0], axis=0)
print("Converted raw numbers to retention percentages. Generating Heatmap...")

# -------------------------------------------------------------------
# 5. DATA VISUALIZATION (Seaborn Heatmap)
# -------------------------------------------------------------------
# Set the canvas size and title
plt.figure(figsize=(18, 10))
plt.title('Brazilian E-Commerce: Customer Retention Rate (%)', fontsize=18, pad=20)

# Draw the heatmap using Seaborn
# fmt='.1%' formats numbers as percentages (e.g., 4.5%)
# cmap='YlGnBu' applies a Yellow-Green-Blue color palette
# vmin=0.0 and vmax=0.10 narrow the focus to 0-10% to highlight differences in later months
sns.heatmap(retention_matrix, annot=True, fmt='.1%', cmap='YlGnBu', vmin=0.0, vmax=0.10, linewidths=0.5)

# Configure axis labels and ticks
plt.ylabel('Cohort Month (First Purchase)', fontsize=14)
plt.xlabel('Month Index (Months Since First Purchase)', fontsize=14)
plt.yticks(rotation=0)

# Render the visualization
plt.tight_layout()
plt.show()
