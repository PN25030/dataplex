rules:
  - name: not_null_rule
    rule_type: NOT_NULL
    dimension: COMPLETENESS

rule_bindings:
  - name: customers_check
    entity_URI: bigquery://projects/your-project-id/datasets/your-dataset/tables/customers
    column: "customer_id"
    row_filter: NONE
    rules:
      - not_null_rule
