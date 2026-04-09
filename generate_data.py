"""
Module to simulate and generate raw e-commerce transaction data.
"""
import pandas as pd
from faker import Faker
import random

# Initialize Faker for synthetic data generation
fake = Faker()
NUM_RECORDS = 100

def generate_ecommerce_data(num_records: int):
    """
    Generates synthetic e-commerce transaction records and persists them to a CSV file.
    
    Args:
        num_records (int): The number of transaction records to simulate.
    """
    print(f"Generating {num_records} transaction records...")
    
    data = []
    
    for _ in range(num_records):
        record = {
            "transaction_id": fake.uuid4(),
            "customer_name": fake.name(),
            "product_category": random.choice(["Electronics", "Clothing", "Home & Garden", "Sports", "Toys"]),
            "price": round(random.uniform(10.0, 500.0), 2),
            "quantity": random.randint(1, 5),
            "transaction_date": fake.date_between(start_date='-1y', end_date='today')
        }
        data.append(record)
        
    df = pd.DataFrame(data)
    
    output_filename = "raw_sales_data.csv"
    df.to_csv(output_filename, index=False)
    
    print(f"Successfully generated and serialized raw data to: {output_filename}")

if __name__ == "__main__":
    generate_ecommerce_data(NUM_RECORDS)
