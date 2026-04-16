"""
Verification module to validate data integrity post-load.
"""
import sqlite3
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def verify_database(db_filename: str):
    """
    Executes analytical queries against the analytics database to verify ETL completion.
    
    Args:
        db_filename (str): Target SQLite database file path.
    """
    logging.info("Establishing database connection for validation checks...")
    conn = sqlite3.connect(db_filename)
    
    query = """
    SELECT 
        customer_name, 
        product_category, 
        total_revenue 
    FROM sales 
    ORDER BY total_revenue DESC 
    LIMIT 5;
    """
    
    logging.info("--- Top 5 Transactions by Revenue ---")
    df = pd.read_sql(query, conn)
    logging.info(f"\n{df}")
    
    query_sum = "SELECT SUM(total_revenue) AS grand_total FROM sales;"
    df_sum = pd.read_sql(query_sum, conn)
    logging.info(f"Aggregated Gross Revenue: ${df_sum['grand_total'][0]:,.2f}")
    
    conn.close()

if __name__ == "__main__":
    verify_database("ecommerce.db")
