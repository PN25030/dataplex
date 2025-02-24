# dataplex

gcloud dataplex tasks create dq-by-table-task \
  --location=us-central1 \
  --lake=your-lake \
  --trigger-type=ON_DEMAND \
  --execution-spec.service-account=your-service-account@your-project-id.iam.gserviceaccount.com \
  --data-quality-spec.config=gs://your-bucket/dq_by_table.yaml \
  --data-quality-spec.result.bigquery-table=projects/your-project-id/datasets/dq_results/tables/by_table_results


gcloud dataplex datascans create data-quality dq-job \
  --location=your-region \
  --data-quality-spec-file=dq_config.yaml \
  --project=your-project-id
