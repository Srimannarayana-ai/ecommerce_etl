"""
Data Quality module to enforce data contracts and isolate invalid records.
"""
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def check_data_quality(input_filename: str, valid_output: str, quarantine_output: str):
    """
    Validates incoming raw data against strict business rules.
    Partitions the dataset into clean output for ingestion and a quarantined dataset for investigation.
    """
    logging.info(f"Initializing Data Quality Check on: {input_filename}")
    
    try:
        df = pd.read_csv(input_filename)
        logging.info(f"Loaded {len(df)} records for validation.")
    except FileNotFoundError:
        logging.error(f"Raw data source '{input_filename}' not found.")
        return

    # Data Quality Rules Definition
    bad_price_mask = df['price'] <= 0
    missing_id_mask = df['transaction_id'].isnull()
    
    all_bad_data_mask = bad_price_mask | missing_id_mask

    # Partition the dataset logic
    clean_data_df = df[~all_bad_data_mask]
    quarantined_data_df = df[all_bad_data_mask]

    clean_data_df.to_csv(valid_output, index=False)
    
    if not quarantined_data_df.empty:
        quarantined_data_df.to_csv(quarantine_output, index=False)
        logging.warning(f"Data quality breach detected.")
        logging.warning(f"Quarantined {len(quarantined_data_df)} records to: '{quarantine_output}'.")
    else:
        logging.info("Data Quality validation passed successfully.")
        
    logging.info(f"Validated {len(clean_data_df)} records successfully serialized to: '{valid_output}'.")

if __name__ == "__main__":
    check_data_quality("raw_sales_data.csv", "validated_data.csv", "quarantined_data.csv")
