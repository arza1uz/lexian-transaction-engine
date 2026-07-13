CREATE OR REPLACE VIEW mart_transaction_activity AS
SELECT
    execution_id,
    user_id,
    transaction_type,
    COUNT(*) AS transaction_count,
    SUM(amount) AS gross_amount,
    SUM(signed_amount) AS net_amount,
    MIN(transaction_timestamp) AS first_transaction_timestamp,
    MAX(transaction_timestamp) AS last_transaction_timestamp
FROM fact_transactions
GROUP BY execution_id, user_id, transaction_type;
