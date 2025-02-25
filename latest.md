Let’s break this down into two parts: (1) defining a simple "not null" rule, and (2) applying it to a table column using a DataPlex YAML configuration for a data scan. I’ll keep it straightforward and natural-sounding.

### Part 1: Simple "Not Null" Rule
A "not null" rule simply checks that a column in a table doesn’t contain any null values. For example, if you have a column like `customer_id`, the rule ensures every row has a valid `customer_id` and none are missing (null).

### Part 2: Applying it in a DataPlex YAML Scan
DataPlex uses YAML to define data quality scans, and we can configure a rule to enforce "not null" on a specific column. Below is an example of how you’d set this up in a DataPlex YAML file. Let’s assume we’re working with a table called `customers` and a column called `customer_id`.

Here’s the YAML:

```yaml
dataScanId: not-null-customer-id-scan
data:
  resource: //bigquery.googleapis.com/projects/my-project/datasets/my_dataset/tables/customers
spec:
  type: DATA_QUALITY
  dataQualitySpec:
    rules:
    - ruleType: NOT_NULL
      column: customer_id
      threshold: 1.0
      description: "Ensures customer_id column has no null values"
    samplingPercent: 100
    rowFilter: "TRUE"
trigger:
  onDemand: true
```

### Explanation
- **`dataScanId`**: A unique name for your scan (e.g., `not-null-customer-id-scan`).
- **`data.resource`**: Points to the table in BigQuery (replace `my-project`, `my_dataset`, and `customers` with your actual values).
- **`spec.type`**: Set to `DATA_QUALITY` since this is a quality check.
- **`rules`**: Defines the "not null" rule:
  - `ruleType: NOT_NULL` specifies the rule.
  - `column: customer_id` targets the column to check.
  - `threshold: 1.0` means 100% of rows must pass (no nulls allowed).
  - `description`: A note about what the rule does.
- **`samplingPercent`**: Set to 100 to check every row (you can lower this if you only want a sample).
- **`rowFilter`**: Set to `TRUE` to include all rows (you can modify this if you want to filter rows).
- **`trigger`**: Set to `onDemand: true` for a manual scan (you could also schedule it).

### How to Use It
1. Save this YAML in a file (e.g., `not_null_scan.yaml`).
2. Deploy it in DataPlex using the Google Cloud CLI:
   ```bash
   gcloud dataplex datascans create --location=[REGION] --file=not_null_scan.yaml
   ```
   Replace `[REGION]` with your region (e.g., `us-central1`).
3. Run the scan manually via the DataPlex UI or CLI to check the `customer_id` column for nulls.

This setup ensures the `customer_id` column in the `customers` table is scanned for null values, and you’ll get a report on whether it passes (no nulls) or fails (nulls found). Let me know if you need help tweaking it further!
