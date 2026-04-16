# Use the official Apache Airflow image as our base (includes Python 3.10 and Airflow pre-installed)
FROM apache/airflow:2.8.2-python3.10

# Copy our requirements file into the container
COPY requirements.txt /requirements.txt

# Install the Python packages we need (pandas, faker)
RUN pip install --no-cache-dir -r /requirements.txt
