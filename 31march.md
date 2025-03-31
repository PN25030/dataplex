If you only want to execute an existing Dataplex scan (not a Dataplex task), you can use the DataplexStartDataScanOperator in Airflow. Here’s how you can set it up:

Example DAG to Execute an Existing Dataplex Scan

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

Explanation
	•	DataplexStartDataScanOperator: Starts an existing data scan in Dataplex.
	•	deferrable=True: Allows asynchronous execution, freeing up Airflow resources.
	•	data_scan_id: The ID of the existing data scan to be executed.

Monitoring
	•	After triggering, you can monitor the progress of the scan in the Google Cloud Console under Dataplex → Data Scans.

Let me know if you’d like further adjustments!