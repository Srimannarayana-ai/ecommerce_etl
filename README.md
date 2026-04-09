# E-Commerce ETL Pipeline 

This repository contains a fully functional, local Extract, Transform, Load (ETL) data pipeline built with Python and SQLite.

## Architecture

This project simulates a real-world data engineering workflow consisting of four distinct phases:

1. **Extract (`generate_data.py`)**: Generates synthetic e-commerce transaction records using the `Faker` library and serializes them to a raw CSV file.
2. **Transform (`transform_data.py`)**: Ingests the raw CSV via `pandas`, drops null values to ensure data integrity, standardizes datetime formats, and calculates derived business metrics (e.g., `total_revenue`).
3. **Load (`load_data.py`)**: Establishes a connection to a local SQLite database and idempotently loads the pristine dataset into a `sales` table.
4. **Analysis (`verify_data.py`)**: Executes analytical SQL queries against the resulting database to validate data integrity and extract top-level business insights.

## Tech Stack

- **Language:** Python 3.x
- **Data Manipulation:** `pandas`
- **Data Generation:** `faker`
- **Database:** SQLite3

## Local Execution

To run this pipeline on your local machine:

1. Create a virtual environment: `python -m venv venv`
2. Activate the environment and install dependencies: `pip install pandas faker`
3. Execute the pipeline scripts sequentially:
   ```bash
   python generate_data.py
   python transform_data.py
   python load_data.py
   python verify_data.py
   ```
