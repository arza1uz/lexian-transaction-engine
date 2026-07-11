SELECT
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_absolute_amount,
    SUM(signed_amount) AS net_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY transaction_type;
