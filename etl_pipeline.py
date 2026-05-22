import pandas as pd
from sqlalchemy import create_engine
import logging

# Configure logging to display professional output in the console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EcommerceETL:
    """
    An ETL (Extract, Transform, Load) pipeline for processing Brazilian E-commerce data
    and loading it into a PostgreSQL database.
    """

    def __init__(self, db_connection_string):
        """Initializes the database connection engine."""
        self.engine = create_engine(db_connection_string)
        logging.info("Database connection established successfully.")

    def extract(self, file_path):
        """Extracts data from a specified CSV file."""
        logging.info(f"Extracting data from: {file_path}...")
        return pd.read_csv(file_path)

    def transform_orders(self, df):
        """
        Transforms the orders dataset.
        - Converts string timestamps to datetime objects.
        - Filters out illogical 'time-traveling' records (delivery before purchase).
        """
        logging.info("Transforming 'orders' dataset...")
        
        # Convert to datetime
        df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
        df['order_delivered_customer_date'] = pd.to_datetime(df['order_delivered_customer_date'])
        
        # Keep valid deliveries OR orders that are not yet delivered (NaT)
        valid_dates = df['order_delivered_customer_date'] >= df['order_purchase_timestamp']
        not_delivered_yet = df['order_delivered_customer_date'].isna()
        
        df_cleaned = df[valid_dates | not_delivered_yet]
        return df_cleaned

    def transform_payments(self, df):
        """
        Transforms the payments dataset.
        - Removes invalid or 'not_defined' payment types.
        """
        logging.info("Transforming 'order_payments' dataset...")
        df_cleaned = df[df['payment_type'] != 'not_defined']
        return df_cleaned

    def load(self, df, table_name):
        """Loads the transformed pandas DataFrame into the PostgreSQL database."""
        logging.info(f"Loading data into PostgreSQL table: '{table_name}'...")
        df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        logging.info(f"Table '{table_name}' loaded successfully.")

    def run_pipeline(self):
        """Executes the complete ETL workflow."""
        try:
            # 1. Process Orders
            df_orders = self.extract('olist_orders_dataset.csv')
            df_orders = self.transform_orders(df_orders)
            self.load(df_orders, 'orders')

            # 2. Process Payments
            df_payments = self.extract('olist_order_payments_dataset.csv')
            df_payments = self.transform_payments(df_payments)
            self.load(df_payments, 'order_payments')

            # 3. Process Customers (Extract & Load directly)
            df_customers = self.extract('olist_customers_dataset.csv')
            self.load(df_customers, 'customers')

            # 4. Process Order Items (Extract & Load directly)
            df_items = self.extract('olist_order_items_dataset.csv')
            self.load(df_items, 'order_items')

            # 5. Process Products (Extract & Load directly)
            df_products = self.extract('olist_products_dataset.csv')
            self.load(df_products, 'products')

            logging.info("🚀 ETL Pipeline completed successfully!")

        except Exception as e:
            logging.error(f"ETL Pipeline failed with error: {e}")

if __name__ == "__main__":
    # Database connection parameters
    # Format: postgresql://username:password@localhost:5432/database_name
    DB_URL = 'postgresql://postgres:<YOUR_PASSWORD_HERE>@localhost:5432/ecommerce_db'
    
    # Instantiate and run the ETL pipeline
    etl_process = EcommerceETL(DB_URL)
    etl_process.run_pipeline()
