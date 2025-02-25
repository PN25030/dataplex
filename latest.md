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
