CREATE OR REPLACE VIEW mart_data_quality_summary AS
WITH executions AS (
    SELECT execution_id FROM fact_pipeline_executions
    UNION
    SELECT execution_id FROM raw_transactions
    UNION
    SELECT execution_id FROM fact_transactions
    UNION
    SELECT execution_id FROM fact_user_balances
), raw_counts AS (
    SELECT
        execution_id,
        COUNT(*) AS raw_row_count,
        COUNT(*) - COUNT(DISTINCT transaction_id) AS duplicate_raw_transaction_count
    FROM raw_transactions
    GROUP BY execution_id
), fact_counts AS (
    SELECT
        execution_id,
        COUNT(*) AS fact_transaction_count
    FROM fact_transactions
    GROUP BY execution_id
), balance_counts AS (
    SELECT
        execution_id,
        COUNT(*) AS balance_record_count
    FROM fact_user_balances
    GROUP BY execution_id
), execution_counts AS (
    SELECT
        execution_id,
        rows_invalid AS invalid_row_count,
        status
    FROM fact_pipeline_executions
)
SELECT
    executions.execution_id,
    COALESCE(raw_counts.raw_row_count, 0) AS raw_row_count,
    COALESCE(fact_counts.fact_transaction_count, 0) AS fact_transaction_count,
    COALESCE(balance_counts.balance_record_count, 0) AS balance_record_count,
    COALESCE(execution_counts.invalid_row_count, 0) AS invalid_row_count,
    COALESCE(raw_counts.duplicate_raw_transaction_count, 0) AS duplicate_raw_transaction_count,
    CASE
        WHEN execution_counts.status <> 'succeeded' THEN 'failed'
        WHEN COALESCE(execution_counts.invalid_row_count, 0) > 0
            OR COALESCE(raw_counts.duplicate_raw_transaction_count, 0) > 0
            OR COALESCE(raw_counts.raw_row_count, 0) <> COALESCE(fact_counts.fact_transaction_count, 0)
            THEN 'warning'
        ELSE 'passed'
    END AS data_quality_status
FROM executions
LEFT JOIN raw_counts
    ON executions.execution_id = raw_counts.execution_id
LEFT JOIN fact_counts
    ON executions.execution_id = fact_counts.execution_id
LEFT JOIN balance_counts
    ON executions.execution_id = balance_counts.execution_id
LEFT JOIN execution_counts
    ON executions.execution_id = execution_counts.execution_id;
