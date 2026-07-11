SELECT
    execution_id,
    user_id,
    SUM(signed_amount) AS sql_calculated_balance,
    COUNT(*) AS transaction_count
FROM fact_transactions
GROUP BY
    execution_id,
    user_id
ORDER BY
    execution_id,
    user_id;
