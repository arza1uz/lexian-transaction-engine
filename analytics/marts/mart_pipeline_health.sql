CREATE OR REPLACE VIEW mart_pipeline_health AS
SELECT
    execution_id,
    status,
    started_at,
    finished_at,
    duration_seconds,
    rows_read,
    rows_valid,
    rows_invalid,
    rows_processed,
    CASE
        WHEN rows_read = 0 THEN 0.0
        ELSE ROUND(rows_valid * 100.0 / rows_read, 2)
    END AS valid_row_rate_pct,
    CASE
        WHEN rows_read = 0 THEN 0.0
        ELSE ROUND(rows_invalid * 100.0 / rows_read, 2)
    END AS invalid_row_rate_pct,
    CASE
        WHEN rows_valid = 0 THEN 0.0
        ELSE ROUND(rows_processed * 100.0 / rows_valid, 2)
    END AS processing_efficiency_pct,
    CASE
        WHEN status <> 'succeeded' THEN 'failed'
        WHEN rows_invalid > 0 OR rows_processed <> rows_valid THEN 'warning'
        ELSE 'healthy'
    END AS health_status
FROM fact_pipeline_executions;
