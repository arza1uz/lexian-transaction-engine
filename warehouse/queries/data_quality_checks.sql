SELECT
    'raw_rows_by_execution' AS check_name,
    execution_id,
    COUNT(*) AS check_value
FROM raw_transactions
GROUP BY execution_id

UNION ALL

SELECT
    'valid_transactions_by_execution' AS check_name,
    execution_id,
    COUNT(*) AS check_value
FROM fact_transactions
GROUP BY execution_id

UNION ALL

SELECT
    'balances_by_execution' AS check_name,
    execution_id,
    COUNT(*) AS check_value
FROM fact_user_balances
GROUP BY execution_id;
