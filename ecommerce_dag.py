from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# Importing the functional logic from your exact python scripts!
from generate_data import generate_ecommerce_data, NUM_RECORDS
from quality_check import check_data_quality
from transform_data import clean_sales_data
from load_data import load_data_to_database
from verify_data import verify_database

# ---------------------------------------------------------
# Define the Default Arguments for your DAG
# ---------------------------------------------------------
default_args = {
    'owner': 'data_engineer_portfolio',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False, # In a real environment, you'd put an email here
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

# ---------------------------------------------------------
# Instantiate the DAG (The Robot Manager)
# ---------------------------------------------------------
dag = DAG(
    'ecommerce_etl_pipeline',
    default_args=default_args,
    description='An automated e-commerce ETL pipeline running daily.',
    schedule_interval='@daily', # Run once a day at midnight
    catchup=False,
)

# ---------------------------------------------------------
# Define the Tasks
# ---------------------------------------------------------
# Task 1: Extract (Generate fake data)
extract_task = PythonOperator(
    task_id='extract_raw_data',
    python_callable=generate_ecommerce_data,
    op_kwargs={'num_records': NUM_RECORDS}, # Passing the argument needed by the function
    dag=dag,
)

# Task 2: Data Quality Check
quality_check_task = PythonOperator(
    task_id='validate_data_quality',
    python_callable=check_data_quality,
    op_kwargs={
        'input_filename': 'raw_sales_data.csv',
        'valid_output': 'validated_data.csv',
        'quarantine_output': 'quarantined_data.csv'
    },
    dag=dag,
)

# Task 3: Transform (Clean data & calculate revenue)
transform_task = PythonOperator(
    task_id='transform_and_clean_data',
    python_callable=clean_sales_data,
    op_kwargs={
        'input_filename': 'validated_data.csv',
        'output_filename': 'cleaned_sales_data.csv'
    },
    dag=dag,
)

# Task 4: Load (Insert into SQLite database)
load_task = PythonOperator(
    task_id='load_to_database',
    python_callable=load_data_to_database,
    op_kwargs={
        'csv_filename': 'cleaned_sales_data.csv',
        'db_filename': 'ecommerce.db',
        'table_name': 'sales'
    },
    dag=dag,
)

# Task 5: Verify (Run analytics to prove it worked)
verify_task = PythonOperator(
    task_id='verify_pipeline_results',
    python_callable=verify_database,
    op_kwargs={'db_filename': 'ecommerce.db'},
    dag=dag,
)

# ---------------------------------------------------------
# Set the Execution Order (The Magic!)
# ---------------------------------------------------------
extract_task >> quality_check_task >> transform_task >> load_task >> verify_task
