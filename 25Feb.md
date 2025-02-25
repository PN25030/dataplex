Let’s dive into how you can use Dataplex with YAML to define a reference rule list and bind specific rules to a table. Dataplex leverages YAML files to specify data quality rules and bindings, typically in conjunction with tools like CloudDQ or its native data quality tasks. I’ll walk you through creating a YAML configuration that defines a set of reusable rules and then binds specific ones to a table. Since you mentioned a "reference YAML rule list," I’ll assume you want a modular setup where rules are defined separately and selectively applied to a table.

Below, I’ll provide a practical example tailored to a BigQuery table, as Dataplex commonly integrates with BigQuery for data quality tasks. The structure will include a rule list, a table entity, and rule bindings. I’ll keep it clear and concise, focusing on the code details you asked for.

### Example Scenario
Let’s say you have a BigQuery table called `sales_orders` in the dataset `my_dataset` under project `my-project-id`. You want to define a reusable list of data quality rules (e.g., checking for nulls, duplicates, and valid ranges) and then bind only specific rules to this table.

### YAML Code Example
Here’s the YAML configuration:

```yaml
# Metadata defaults for Dataplex entity URIs (optional convenience)
metadata_registry_defaults:
  bigquery:
    projects: my-project-id
    datasets: my_dataset

# Define reusable rules (your reference rule list)
rules:
  NOT_NULL_SIMPLE:
    type: NOT_NULL
    description: "Ensures the column has no null values"
  NO_DUPLICATES:
    type: NO_DUPLICATES_IN_COLUMN_GROUPS
    parameters:
      column_names: 
        - $column
    description: "Checks for duplicate values in the specified column"
  POSITIVE_VALUE:
    type: RANGE
    parameters:
      min: "0"
      max: "1000000"
    description: "Ensures values are positive and within a reasonable range"
  VALID_EMAIL:
    type: REGEX
    parameters:
      pattern: "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
    description: "Validates email format"

# Define row filters (optional, for selective rule application)
row_filters:
  NONE:
    filter_sql_expr: "TRUE"

# Bind specific rules to the table
rule_bindings:
  SALES_ORDER_ID_CHECK:
    entity_uri: bigquery://tables/sales_orders
    column_id: order_id
    row_filter_id: NONE
    rule_ids:
      - NOT_NULL_SIMPLE
      - NO_DUPLICATES
    metadata:
      team: sales_team
  SALES_AMOUNT_CHECK:
    entity_uri: bigquery://tables/sales_orders
    column_id: amount
    row_filter_id: NONE
    rule_ids:
      - NOT_NULL_SIMPLE
      - POSITIVE_VALUE
    metadata:
      team: finance_team
```

### Breakdown of the Code

1. **Metadata Registry Defaults**:
   - This section simplifies the `entity_uri` by setting default values for the project and dataset. Instead of writing the full URI (`bigquery://projects/my-project-id/datasets/my_dataset/tables/sales_orders`) for every binding, you can just use `bigquery://tables/sales_orders`.
   - Optional but handy for cleaner YAML.

2. **Rules Section**:
   - This is your "reference YAML rule list." It defines reusable data quality rules:
     - `NOT_NULL_SIMPLE`: Checks that a column has no null values.
     - `NO_DUPLICATES`: Ensures no duplicate values in a column (uses `$column` as a placeholder for the column specified in the binding).
     - `POSITIVE_VALUE`: Ensures values are between 0 and 1,000,000 (adjustable range).
     - `VALID_EMAIL`: Validates a column against an email regex pattern.
   - These rules are generic and can be applied to any table/column via bindings.

3. **Row Filters**:
   - Defines filters to apply before running rules. Here, `NONE` means no filtering (all rows are checked). You could add filters like `filter_sql_expr: "amount > 100"` to target specific rows.

4. **Rule Bindings**:
   - This is where you bind specific rules from the reference list to your table:
     - `SALES_ORDER_ID_CHECK`: Applies `NOT_NULL_SIMPLE` and `NO_DUPLICATES` to the `order_id` column of `sales_orders`.
     - `SALES_AMOUNT_CHECK`: Applies `NOT_NULL_SIMPLE` and `POSITIVE_VALUE` to the `amount` column.
   - Each binding specifies:
     - `entity_uri`: The table (shortened thanks to defaults).
     - `column_id`: The column to validate.
     - `row_filter_id`: References a filter (here, `NONE`).
     - `rule_ids`: The specific rules to apply from the `rules` list.
     - `metadata`: Optional tags (e.g., team ownership).

### How to Use This in Dataplex
1. **Store the YAML**:
   - Save this as, say, `data_quality_rules.yaml` and upload it to a Google Cloud Storage bucket (e.g., `gs://my-bucket/dq-rules/`).

2. **Create a Dataplex Data Quality Task**:
   - In the Google Cloud Console, go to Dataplex > Process > Create Task.
   - Select "Check Data Quality."
   - Configure:
     - YAML file location: `gs://my-bucket/dq-rules/data_quality_rules.yaml`.
     - Target BigQuery dataset: Where results will be stored (e.g., `my_project_id.my_dq_results_dataset`).
     - Schedule: On-demand or recurring.
   - Submit the task to run the validation.

3. **Review Results**:
   - Results will appear in the specified BigQuery dataset as tables or views, showing pass/fail details for each rule binding.

### Customization Tips
- **Add More Rules**: Expand the `rules` section with custom SQL rules if needed (e.g., `type: CUSTOM_SQL_EXPR` with a `sql_expr` field).
- **Multiple Tables**: Add more `rule_bindings` entries with different `entity_uri` values to apply rules to other tables.
- **Incremental Validation**: Add `incremental_time_filter_column_id` in a binding to validate only new data based on a timestamp column.

This setup gives you a modular, reusable rule list and the flexibility to bind specific rules to your table as needed. Let me know if you’d like to tweak this further or adapt it to a different table structure!
