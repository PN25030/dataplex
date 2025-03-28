try:
    from airflow import DAG
    from airflow.providers.google.cloud.operators.dataplex import DataplexCreateOrUpdateScanOperator
    from airflow.utils.dates import days_ago
    from datetime import timedelta
except ModuleNotFoundError as e:
    raise ImportError("Airflow or its required components are not installed. Ensure you have Apache Airflow with Google provider installed using `pip install apache-airflow-providers-google`.\nOriginal Error: " + str(e))

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG with cron expression for schedule
def create_dataplex_scan_dag(cron_expression: str = '0 0 * * *'):
    with DAG(
        'dataplex_create_or_update_scan',
        default_args=default_args,
        description='DAG to create or update a Dataplex Scan',
        schedule_interval=cron_expression,
        start_date=days_ago(1),
        catchup=False,
    ) as dag:

        create_or_update_scan = DataplexCreateOrUpdateScanOperator(
            task_id='create_or_update_scan',
            project_id='your-gcp-project-id',
            region='your-region',
            scan_id='your-scan-id',
            scan={
                'name': 'projects/your-gcp-project-id/locations/your-region/scans/your-scan-id',
                'description': 'Dataplex scan for data quality checks',
                'data': {
                    'resourceSpec': {
                        'name': 'your-bigquery-dataset',
                        'type': 'BIGQUERY_DATASET'
                    }
                },
                'executionSpec': {
                    'trigger': 'SCHEDULE',
                    'schedule': {
                        'cron': cron_expression
                    }
                }
            },
        )

        create_or_update_scan

    return dag

# Example with cron expression for every hour
globals()['dataplex_scan_hourly'] = create_dataplex_scan_dag('0 * * * *')
