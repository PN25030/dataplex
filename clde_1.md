I'll create a comprehensive example of a DAG using the DataplexCreateOrUpdateScanOperator for data quality checks. I'll use an artifact to provide a complete, working example that demonstrates best practices for CloudDQ and Airflow integration.

```python
import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataplex import DataplexCreateOrUpdateScanOperator
from airflow.providers.google.cloud.operators.dataplex import DataplexDeleteScanOperator
from airflow.utils.dates import days_ago

# Configuration for the Dataplex Data Quality Scan
DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# YAML Configuration for Data Quality Rules
DQ_YAML_CONFIG = """
dataQualitySpec:
  rules:
    - column: customer_id
      type: uniquenessRule
      threshold: 0.99
    
    - column: purchase_amount
      type: rangeRule
      minValue: 0
      maxValue: 10000
    
    - column: email
      type: regexRule
      regex: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
"""

with DAG(
    'dataplex_data_quality_scan',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily',
    catchup=False,
    tags=['dataplex', 'data-quality']
) as dag:
    
    # Task to create or update Dataplex data quality scan
    create_or_update_scan = DataplexCreateOrUpdateScanOperator(
        task_id='create_or_update_dataplex_scan',
        project_id='your-gcp-project-id',  # Replace with your GCP project ID
        region='us-central1',  # Replace with your preferred region
        lake_id='your-lake-id',  # Replace with your Dataplex lake ID
        dataplex_scan_id='customers-data-quality-scan',
        body={
            'type': 'CUSTOM_SCAN',
            'spec': {
                'assets': [
                    {
                        'resourceSpec': {
                            'name': 'projects/your-gcp-project-id/datasets/your-dataset/tables/customers'
                        }
                    }
                ],
                'dataQualitySpec': {
                    'rules': [
                        {
                            'column': 'customer_id',
                            'type': 'uniquenessRule',
                            'threshold': 0.99
                        },
                        {
                            'column': 'purchase_amount',
                            'type': 'rangeRule',
                            'minValue': 0,
                            'maxValue': 10000
                        },
                        {
                            'column': 'email',
                            'type': 'regexRule',
                            'regex': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
                        }
                    ]
                }
            }
        }
    )

    # Optional: Task to delete the scan if needed
    delete_scan = DataplexDeleteScanOperator(
        task_id='delete_dataplex_scan',
        project_id='your-gcp-project-id',
        region='us-central1',
        lake_id='your-lake-id',
        dataplex_scan_id='customers-data-quality-scan',
        trigger_rule='all_done'  # Ensures this runs after create/update, even if it fails
    )

    # Set task dependencies
    create_or_update_scan >> delete_scan

# Note: This is a sample DAG and should be customized to your specific use case

```

Let me break down the key components of this Dataplex Data Quality DAG:

1. **Import Required Libraries**:
   - Uses Airflow's Google Cloud Dataplex operators
   - Imports necessary datetime and DAG utilities

2. **Configuration**:
   - Sets up default Airflow arguments
   - Defines a sample YAML-like configuration for data quality rules
   - Demonstrates rules for:
     - Uniqueness check on customer_id
     - Range validation for purchase_amount
     - Regex validation for email format

3. **DAG Structure**:
   - Uses `DataplexCreateOrUpdateScanOperator` to define and run data quality scans
   - Includes an optional `DataplexDeleteScanOperator` for cleanup

4. **Data Quality Rules**:
   - Uniqueness Rule: Ensures customer_id has at least 99% unique values
   - Range Rule: Checks purchase_amount is between 0 and 10,000
   - Regex Rule: Validates email format

**Important Customization Notes**:
- Replace placeholders like `your-gcp-project-id`, `your-lake-id`, and dataset/table names
- Adjust region, scan ID, and data quality rules to match your specific requirements
- Ensure you have the necessary Google Cloud and Airflow provider packages installed

**Prerequisites**:
- Google Cloud Dataplex service enabled
- Airflow with Google Cloud providers installed
- Proper GCP service account permissions

Would you like me to elaborate on any part of the DAG or explain the CloudDQ and Airflow integration in more detail?

import json
from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.google.cloud.operators.dataplex import DataplexCreateOrUpdateScanOperator
from airflow.providers.google.cloud.operators.dataplex import DataplexDeleteScanOperator
from airflow.utils.dates import days_ago

# Configuration for the Dataplex Data Quality Scan
DEFAULT_ARGS = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# YAML Configuration for Data Quality Rules
DQ_YAML_CONFIG = """
dataQualitySpec:
  rules:
    - column: customer_id
      type: uniquenessRule
      threshold: 0.99
    
    - column: purchase_amount
      type: rangeRule
      minValue: 0
      maxValue: 10000
    
    - column: email
      type: regexRule
      regex: '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
"""

with DAG(
    'dataplex_data_quality_scan',
    default_args=DEFAULT_ARGS,
    schedule_interval='@daily',
    catchup=False,
    tags=['dataplex', 'data-quality']
) as dag:
    
    # Task to create or update Dataplex data quality scan
    create_or_update_scan = DataplexCreateOrUpdateScanOperator(
        task_id='create_or_update_dataplex_scan',
        project_id='your-gcp-project-id',  # Replace with your GCP project ID
        region='us-central1',  # Replace with your preferred region
        lake_id='your-lake-id',  # Replace with your Dataplex lake ID
        dataplex_scan_id='customers-data-quality-scan',
        body={
            'type': 'CUSTOM_SCAN',
            'spec': {
                'assets': [
                    {
                        'resourceSpec': {
                            'name': 'projects/your-gcp-project-id/datasets/your-dataset/tables/customers'
                        }
                    }
                ],
                'dataQualitySpec': {
                    'rules': [
                        {
                            'column': 'customer_id',
                            'type': 'uniquenessRule',
                            'threshold': 0.99
                        },
                        {
                            'column': 'purchase_amount',
                            'type': 'rangeRule',
                            'minValue': 0,
                            'maxValue': 10000
                        },
                        {
                            'column': 'email',
                            'type': 'regexRule',
                            'regex': '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
                        }
                    ]
                }
            }
        }
    )

    # Optional: Task to delete the scan if needed
    delete_scan = DataplexDeleteScanOperator(
        task_id='delete_dataplex_scan',
        project_id='your-gcp-project-id',
        region='us-central1',
        lake_id='your-lake-id',
        dataplex_scan_id='customers-data-quality-scan',
        trigger_rule='all_done'  # Ensures this runs after create/update, even if it fails
    )

    # Set task dependencies
    create_or_update_scan >> delete_scan

# Note: This is a sample DAG and should be customized to your specific use case
