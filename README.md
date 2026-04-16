# E-Commerce ETL Pipeline

This repository contains a fully functional, local Extract, Transform, Load (ETL) data pipeline built with Python and SQLite, featuring robust Data Quality checks.

## Architecture

This project simulates a real-world data engineering workflow consisting of five distinct phases:

1. **Extract (`generate_data.py`)**: Generates synthetic e-commerce transaction records using the `faker` library, occasionally injecting intentional data anomalies, and serializes them to a raw CSV file.
2. **Data Quality & Quarantine (`quality_check.py`)**: Intercepts the raw data and applies boolean mask checks to enforce strict data contracts. Clean records pass through for transformation, while anomalies (e.g., negative prices, missing IDs) are isolated into a quarantine file.
3. **Transform (`transform_data.py`)**: Ingests the validated CSV via `pandas`, standardizes datetime formats, handles edge cases, and calculates derived business metrics (e.g., `total_revenue`).
4. **Load (`load_data.py`)**: Establishes a connection to a local SQLite database and idempotently loads the pristine dataset into a `sales` database table.
5. **Analysis (`verify_data.py`)**: Executes analytical SQL queries against the resulting database to validate data integrity and extract downstream business insights.
6. **Orchestration (`ecommerce_dag.py`)**: An Apache Airflow DAG that schedules and automatically executes the above tasks sequentially, managing dependencies and failures.

## Tech Stack

- **Language:** Python 3.x
- **Data Manipulation:** `pandas`
- **Data Generation:** `faker`
- **Database:** SQLite3
- **Orchestration:** Apache Airflow
- **Containerization:** Docker & Docker Compose

## Local Execution

To run this pipeline on your local machine:

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

2. **Activate the environment:**
   - On **Windows**: `.\venv\Scripts\activate`
   - On **Mac/Linux**: `source venv/bin/activate`

3. **Install dependencies:**
   ```bash
   pip install pandas faker
   ```

4. **Execute the pipeline scripts sequentially:**
   ```bash
   python generate_data.py
   python quality_check.py
   python transform_data.py
   python load_data.py
   python verify_data.py
   ```

## Automated Testing

To ensure the integrity of the data transformations and quality checks, a `pytest` suite is included.
To run the automated tests:

```bash
python -m pytest test_pipeline.py -v
```

## Running with Docker & Airflow (Production Simulation)

To run the fully automated, orchestrated pipeline in an isolated environment:

1. **Ensure Docker Desktop is running.**
2. **Start the pipeline in Detached Mode using Docker Compose:**
   ```bash
   docker-compose up -d
   ```
3. **Access the Airflow Web UI:**
   - Open your browser and navigate to `http://localhost:8080/`
   - **Username:** `admin`
   - *Check your terminal logs or `standalone_admin_password.txt` in the container for the dynamically generated password.*
4. **Trigger the Pipeline:**
   Inside the UI, locate the `ecommerce_etl_pipeline` DAG, unpause it, and watch the visual execution of your ETL tasks!
5. **Teardown:**
   When finished, cleanly shut down the container using:
   ```bash
   docker-compose down
   ```
