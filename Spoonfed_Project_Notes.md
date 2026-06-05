# E-Commerce ETL Pipeline: Master Explanation Notes

This document provides a **spoon-fed, line-by-line** breakdown of the entire E-Commerce ETL Pipeline project. It is designed to explain the concept and syntax of every single script from scratch to end.

---

## 1. Extract: `generate_data.py`
**Goal:** Create fake e-commerce data to simulate a real business.

```python
import pandas as pd
from faker import Faker
import random
import logging
```
* **Line 1-4:** We import tools we need. `pandas` manages data in table format. `Faker` generates fake names/dates. `random` generates random numbers/choices. `logging` lets us print status messages to the terminal safely.

```python
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
```
* **Line 5:** Sets up the logging tool so every message it prints has a timestamp, the severity level (INFO, WARNING, etc.), and the actual message.

```python
fake = Faker()
NUM_RECORDS = 100
ERROR_RATE = 0.05
```
* **Line 6-8:** We create a `Faker` object called `fake`. We define `NUM_RECORDS` as 100 (so it generates 100 fake transactions) and `ERROR_RATE` as 0.05 (which means a 5% chance of intentionally creating "bad" data to test our pipeline later).

```python
def generate_ecommerce_data(num_records: int):
    logging.info(f"Generating {num_records} transaction records...")
    data = []
```
* **Line 9-11:** Defines the main function. We log a message saying we are starting. We create an empty list called `data` that will eventually hold all our fake transactions.

```python
    for _ in range(num_records):
```
* **Line 12:** A loop that will run 100 times (based on `num_records`). The `_` means we don't care about the loop number itself.

```python
        transaction_id = fake.uuid4() if random.random() > ERROR_RATE else None
```
* **Line 13:** Generates a random unique ID (`fake.uuid4()`). However, `if random.random() > 0.05` means 95% of the time it works, but 5% of the time it assigns `None` (a missing ID) to test our error checking later.

```python
        price = round(random.uniform(10.0, 500.0), 2) if random.random() > ERROR_RATE else round(random.uniform(-50.0, -1.0), 2)
```
* **Line 14:** 95% of the time, it generates a normal price between $10 and $500, rounded to 2 decimal places. 5% of the time, it intentionally generates a **negative** price to act as bad data.

```python
        record = {
            "transaction_id": transaction_id,
            "customer_name": fake.name(),
            "product_category": random.choice(["Electronics", "Clothing", "Home & Garden", "Sports", "Toys"]),
            "price": price,
            "quantity": random.randint(1, 5),
            "transaction_date": fake.date_between(start_date='-1y', end_date='today')
        }
        data.append(record)
```
* **Line 15-23:** We create a "dictionary" (a packet of data) representing a single purchase. It uses fake names, randomly picks a category, uses the price we calculated above, picks a random quantity between 1 and 5, and generates a random date within the last year. Finally, it `appends` (adds) this single record to our master `data` list.

```python
    df = pd.DataFrame(data)
    output_filename = "raw_sales_data.csv"
    df.to_csv(output_filename, index=False)
```
* **Line 24-26:** We take our `data` list and turn it into a Pandas DataFrame (a virtual spreadsheet). We name the output file `raw_sales_data.csv` and use `.to_csv()` to physically save the virtual spreadsheet to your hard drive, ignoring the row numbers (`index=False`).

---

## 2. Validation: `quality_check.py`
**Goal:** Catch the bad data (missing IDs, negative prices) so it doesn't ruin our database.

```python
def check_data_quality(input_filename: str, valid_output: str, quarantine_output: str):
```
* Takes three arguments: the raw file we just made, the name for the clean output file, and the name for the "quarantine" jail file.

```python
    try:
        df = pd.read_csv(input_filename)
```
* Tries to open the `raw_sales_data.csv` file into a Pandas DataFrame.

```python
    bad_price_mask = df['price'] <= 0
    missing_id_mask = df['transaction_id'].isnull()
    all_bad_data_mask = bad_price_mask | missing_id_mask
```
* **The Magic Lines:** `bad_price_mask` scans every row and tags `True` if the price is 0 or less. `missing_id_mask` scans for empty IDs. `all_bad_data_mask` combines them using the `|` (OR) symbol. If either is true, the row is marked as "BAD".

```python
    clean_data_df = df[~all_bad_data_mask]
    quarantined_data_df = df[all_bad_data_mask]
```
* We physically split the rows. `clean_data_df` takes rows where the bad mask is `~` (NOT applied). `quarantined_data_df` takes the rows where the bad mask IS applied.

```python
    clean_data_df.to_csv(valid_output, index=False)
    if not quarantined_data_df.empty:
        quarantined_data_df.to_csv(quarantine_output, index=False)
```
* Saves the good data to `validated_data.csv`. If the quarantine list isn't empty, it saves the bad rows to `quarantined_data.csv` so engineers can inspect them later!

---

## 3. Transform: `transform_data.py`
**Goal:** Calculate the business logic (Total Revenue).

```python
def clean_sales_data(input_filename: str, output_filename: str):
    df = pd.read_csv(input_filename)
```
* Opens the `validated_data.csv` (which is now guaranteed to have no negative prices or missing IDs).

```python
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
```
* Converts the date column from a standard text string into a formal "Datetime" object so databases can understand how to sort by date later.

```python
    df['total_revenue'] = df['price'] * df['quantity']
```
* Creates a brand new column named `total_revenue`, calculated dynamically on the fly by multiplying the price by the quantity. 

```python
    df = df.dropna()
    df.to_csv(output_filename, index=False)
```
* `dropna()` is a final safety net to delete any row with any random blank columns. It saves the final table as `cleaned_sales_data.csv`.

---

## 4. Load: `load_data.py`
**Goal:** Push the clean, transformed data into a real database structure.

```python
import sqlite3
```
* Imports the built-in Python tool used to talk to Local SQLite databases.

```python
def load_data_to_database(csv_filename: str, db_filename: str, table_name: str):
    df = pd.read_csv(csv_filename)
```
* Opens the final, perfect `cleaned_sales_data.csv`.

```python
    conn = sqlite3.connect(db_filename)
```
* Opens a direct cable connection to `ecommerce.db` (creating it if it doesn't already exist).

```python
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()
```
* The single most powerful line: takes the entire Pandas dataframe and rams it into the SQL database connection into a table named `sales`. `if_exists='replace'` means if we run the pipeline multiple times, it wipes the old data instead of stacking it infinitely. Finally, `conn.close()` hangs up the connection.

---

## 5. Verify & Orchestrate
* **`verify_data.py`**: Connects to the database and runs standard SQL `SELECT` commands to prove the data is safely loaded and queryable.
* **`ecommerce_dag.py`**: Apache Airflow's "Script". It physically imports all the functions above and chains them together like dominos: `Extract -> Quality Check -> Transform -> Load -> Verify`. It tells docker when to run them and in what order!
* **Docker**: The config files (`Dockerfile` and `docker-compose.yml`) build an isolated virtual mini-computer that runs Ubuntu and contains Airflow, so this pipeline can run anywhere without crashing.
