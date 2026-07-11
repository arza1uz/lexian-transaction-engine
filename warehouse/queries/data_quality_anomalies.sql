SELECT
    'negative_or_zero_amount' AS anomaly_type,
    execution_id,
    transaction_id,
    user_id,
    transaction_type,
    amount
FROM fact_transactions
WHERE amount <= 0

UNION ALL

SELECT
    'missing_user_id' AS anomaly_type,
    execution_id,
    transaction_id,
    user_id,
    transaction_type,
    amount
FROM fact_transactions
WHERE user_id IS NULL OR TRIM(user_id) = ''

UNION ALL

SELECT
    'unsupported_transaction_type' AS anomaly_type,
    execution_id,
    transaction_id,
    user_id,
    transaction_type,
    amount
FROM fact_transactions
WHERE transaction_type NOT IN ('deposit', 'withdrawal');
