"""
Module for data transformation and cleansing operations.
"""
import pandas as pd

def clean_sales_data(input_filename: str, output_filename: str):
    """
    Reads validated sales data, applies business logic transformations, handles 
    missing values, and outputs the cleansed dataset.
    """
    print(f"Reading source data from: {input_filename}...")
    
    df = pd.read_csv(input_filename)
    
    # Standardize datetime format for database compatibility
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    
    # Calculate derived metric: total revenue per transaction
    df['total_revenue'] = df['price'] * df['quantity']
    
    # Drop records containing null values to ensure structural integrity
    df = df.dropna()
    
    df.to_csv(output_filename, index=False)
    
    print(f"Transformed dataset successfully written to: {output_filename}")

if __name__ == "__main__":
    clean_sales_data("validated_data.csv", "cleaned_sales_data.csv")
