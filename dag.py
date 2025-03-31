from airflow import DAG
from airflow.providers.google.cloud.operators.dataplex import DataplexStartDataScanOperator
from airflow.utils.dates import days_ago

# Define constants
PROJECT_ID = 'your-project-id'
LOCATION = 'your-region'
SCAN_ID = 'your-dataplex-scan-id'

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define DAG
with DAG(
    'execute_existing_dataplex_scan',
    default_args=default_args,
    description='Execute an existing Dataplex scan using Airflow',
    schedule_interval=None,
    start_date=days_ago(1),
    catchup=False,
) as dag:

    execute_scan = DataplexStartDataScanOperator(
        task_id='execute_dataplex_scan',
        project_id=PROJECT_ID,
        location=LOCATION,
        data_scan_id=SCAN_ID,
        deferrable=True,
    )

    execute_scan