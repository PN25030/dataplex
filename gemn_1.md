```python
from __future__ import annotations

import datetime

import yaml

from airflow.models.dag import DAG
from airflow.providers.google.cloud.operators.dataplex import DataplexCreateOrUpdateTaskOperator

with DAG(
    dag_id="dataplex_dq_scan_dag",
    schedule=None,
    start_date=datetime.datetime(2023, 1, 1),
    catchup=False,
    tags=["dataplex", "dq"],
) as dag:
    dq_rules_yaml = """
    dataQualitySpec:
      rules:
        - column: "id"
          nonNullExpectation: {}
        - column: "value"
          rangeExpectation:
            minValue: 0
            maxValue: 100
    """

    create_dq_scan = DataplexCreateOrUpdateTaskOperator(
        task_id="create_dq_scan",
        project_id="YOUR_PROJECT_ID",  # Replace with your project ID
        location="YOUR_LOCATION",  # Replace with your location (e.g., "us-central1")
        lake_id="YOUR_LAKE_ID",  # Replace with your lake ID
        task_id_name="dq-scan-task",
        body={
            "description": "Data Quality Scan Task",
            "triggerSpec": {"schedule": "0 0 * * *"},  # Daily at midnight
            "executionSpec": {"serviceAccount": "YOUR_SERVICE_ACCOUNT"}, # Replace with your service account
            "spark": {"config": {}},
            "dataQualitySpec": yaml.safe_load(dq_rules_yaml)["dataQualitySpec"],
            "dataQualityResultTable": "projects/YOUR_PROJECT_ID/datasets/YOUR_DATASET_ID/tables/dq_results", #Replace with your result table path
            "inputData": {
                "entity": "projects/YOUR_PROJECT_ID/locations/YOUR_LOCATION/lakes/YOUR_LAKE_ID/zones/YOUR_ZONE_ID/entities/YOUR_ENTITY_ID" #Replace with your entity ID
            }
        },
    )

    create_dq_scan
```

**Key improvements and explanations:**

1.  **YAML Input:**
    * The DQ rules are now defined in a YAML string (`dq_rules_yaml`), which is then loaded using `yaml.safe_load()`. This makes the rules much more readable and maintainable.
    * The `dataQualitySpec` is directly passed into the `body` of the operator.
2.  **DataplexCreateOrUpdateTaskOperator:**
    * Uses the `DataplexCreateOrUpdateTaskOperator`, which is the correct operator for creating or updating Dataplex tasks.
3.  **Required Parameters:**
    * Includes all the essential parameters:
        * `project_id`: Your Google Cloud project ID.
        * `location`: The Dataplex location (e.g., "us-central1").
        * `lake_id`: The Dataplex lake ID.
        * `task_id_name`: The unique ID for the Dataplex task.
        * `body`: The task configuration, including the DQ rules, schedule, and input data.
4.  **Body Configuration:**
    * The `body` dictionary now includes:
        * `description`: A descriptive string for the task.
        * `triggerSpec`: A cron schedule for running the DQ scan (e.g., daily at midnight).
        * `executionSpec`: the service account to be used for the task.
        * `spark`: An empty Spark configuration (you can add Spark-specific settings here if needed).
        * `dataQualitySpec`: The loaded DQ rules from the YAML.
        * `dataQualityResultTable`: The full resource name of the BigQuery table to store the DQ results.
        * `inputData`: The full resource name of the Dataplex entity to scan.
5.  **Placeholders:**
    * I've used placeholders like `YOUR_PROJECT_ID`, `YOUR_LOCATION`, `YOUR_LAKE_ID`, `YOUR_SERVICE_ACCOUNT`, `YOUR_DATASET_ID`, and `YOUR_ENTITY_ID`. **You must replace these with your actual values.**
6.  **Error Handling and Validation:**
    * In a production environment, you should add error handling and validation to ensure the YAML is valid and the Dataplex task is created successfully.
7.  **Service Account:**
    * The service account that is used needs to have the Dataplex admin role, and Bigquery write permissions.

**Before Running:**

1.  **Install Providers:** Ensure you have the Google Cloud provider installed:
    ```bash
    pip install apache-airflow-providers-google
    ```
2.  **Replace Placeholders:** Replace all the `YOUR_*` placeholders with your actual Google Cloud resource IDs.
3.  **Service Account Setup:** Make sure the service account that Airflow uses has the necessary permissions to create Dataplex tasks and write to BigQuery.
4.  **Dataplex Resources:** Ensure the Dataplex lake, zone, and entity you're referencing exist.
5.  **BigQuery Dataset and Table:** Create the BigQuery dataset and table specified in `dataQualityResultTable`.

This improved code provides a more robust and practical example of using the `DataplexCreateOrUpdateTaskOperator` for DQ scans in Dataplex.
