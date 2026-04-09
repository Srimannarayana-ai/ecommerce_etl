"""
Module to simulate and generate raw e-commerce transaction data.
"""
import pandas as pd
from faker import Faker
import random

fake = Faker()
NUM_RECORDS = 100
ERROR_RATE = 0.05

def generate_ecommerce_data(num_records: int):
    """
    Generates synthetic e-commerce transaction records and persists them to a CSV file.
    Includes intentional data anomalies to test downstream validation logic.
    """
    print(f"Generating {num_records} transaction records...")
    
    data = []
    
    for _ in range(num_records):
        # Simulate missing constraints or faulty upstream processes
        transaction_id = fake.uuid4() if random.random() > ERROR_RATE else None
        
        # Simulate anomalous negative values
        price = round(random.uniform(10.0, 500.0), 2) if random.random() > ERROR_RATE else round(random.uniform(-50.0, -1.0), 2)

        record = {
            "transaction_id": transaction_id,
            "customer_name": fake.name(),
            "product_category": random.choice(["Electronics", "Clothing", "Home & Garden", "Sports", "Toys"]),
            "price": price,
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
