SELECT
    execution_id,
    started_at,
    finished_at,
    duration_seconds,
    status,
    rows_read,
    rows_valid,
    rows_invalid,
    rows_processed,
    input_path,
    output_path
FROM fact_pipeline_executions
ORDER BY started_at DESC;
