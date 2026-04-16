import os
import pandas as pd
import pytest
from quality_check import check_data_quality
from transform_data import clean_sales_data

@pytest.fixture
def setup_files():
    """Provides temporary filenames for testing and automatically cleans them up."""
    input_file = "test_raw_data.csv"
    valid_out = "test_valid_data.csv"
    quar_out = "test_quar_data.csv"
    clean_out = "test_clean_data.csv"
    
    yield input_file, valid_out, quar_out, clean_out
    
    # Teardown logic
    for f in [input_file, valid_out, quar_out, clean_out]:
        if os.path.exists(f):
            os.remove(f)

def test_check_data_quality(setup_files):
    """Verifies that good data is kept and bad data (negative price, missing ID) is quarantined."""
    input_file, valid_out, quar_out, _ = setup_files
    data = [
        {"transaction_id": "id_1", "price": 100, "quantity": 1},
        {"transaction_id": "id_2", "price": -50, "quantity": 1}, # Negative price -> quarantine
        {"transaction_id": None, "price": 150, "quantity": 1},  # Missing ID -> quarantine
    ]
    pd.DataFrame(data).to_csv(input_file, index=False)
    
    check_data_quality(input_file, valid_out, quar_out)
    
    valid_df = pd.read_csv(valid_out)
    quar_df = pd.read_csv(quar_out)
    
    # 1 valid record should pass through
    assert len(valid_df) == 1
    assert valid_df.iloc[0]["transaction_id"] == "id_1"
    
    # 2 invalid records should be quarantined
    assert len(quar_df) == 2

def test_clean_sales_data(setup_files):
    """Verifies that total_revenue is correctly calculated from price and quantity."""
    _, valid_out, _, clean_out = setup_files
    data = [
        {"transaction_id": "id_1", "price": 100, "quantity": 2, "transaction_date": "2023-01-01"},
    ]
    pd.DataFrame(data).to_csv(valid_out, index=False)
    
    clean_sales_data(valid_out, clean_out)
    
    clean_df = pd.read_csv(clean_out)
    
    assert len(clean_df) == 1
    assert "total_revenue" in clean_df.columns
    # 100 * 2 = 200
    assert clean_df.iloc[0]["total_revenue"] == 200.0
