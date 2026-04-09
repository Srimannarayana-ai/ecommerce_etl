"""
Module to handle the loading phase of the ETL pipeline.
"""
import pandas as pd
import sqlite3

def load_data_to_database(csv_filename: str, db_filename: str, table_name: str):
    """
    Extracts cleansed data from a CSV source and loads it into a target SQLite database.
    
    Args:
        csv_filename (str): Path to the cleansed CSV file.
        db_filename (str): Target SQLite database file path.
        table_name (str): Target table name within the database.
    """
    print(f"Initiating load process from {csv_filename}...")
    
    df = pd.read_csv(csv_filename)
    
    print(f"Establishing connection to target database: {db_filename}...")
    conn = sqlite3.connect(db_filename)
    
    print(f"Inserting records into table '{table_name}'...")
    # Using 'replace' to ensure idempotency for development runs
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    
    conn.close()
    
    print("Database load operation completed successfully.")

if __name__ == "__main__":
    load_data_to_database("cleaned_sales_data.csv", "ecommerce.db", "sales")
