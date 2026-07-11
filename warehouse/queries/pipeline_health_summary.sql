SELECT
    execution_id,
    status,
    rows_read,
    rows_valid,
    rows_invalid,
    rows_processed,
    CASE
        WHEN rows_read = 0 THEN 0
        ELSE ROUND((rows_valid::DOUBLE / rows_read::DOUBLE) * 100, 2)
    END AS valid_row_rate_pct,
    CASE
        WHEN rows_read = 0 THEN 0
        ELSE ROUND((rows_invalid::DOUBLE / rows_read::DOUBLE) * 100, 2)
    END AS invalid_row_rate_pct,
    duration_seconds
FROM fact_pipeline_executions
ORDER BY started_at DESC;
