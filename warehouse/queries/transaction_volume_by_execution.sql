SELECT
    execution_id,
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_absolute_amount,
    SUM(signed_amount) AS net_amount
FROM fact_transactions
GROUP BY
    execution_id,
    transaction_type
ORDER BY
    execution_id,
    transaction_type;
