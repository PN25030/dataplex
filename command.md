rules:
  - name: not_null_rule
    rule_type: NOT_NULL
    dimension: COMPLETENESS
  - name: range_rule
    rule_type: RANGE
    dimension: VALIDITY
    params:
      min_value: 0
      max_value: 1000

rule_bindings:
  - name: customers_check
    entity_URI: bigquery://projects/your-project-id/datasets/your-dataset/tables/customers
    column: "customer_id"
    row_filter: NONE
    rules:
      - not_null_rule
  - name: orders_check
    entity_URI: bigquery://projects/your-project-id/datasets/your-dataset/tables/orders
    column: "order_amount"
    row_filter: NONE
    rules:
      - range_rule
