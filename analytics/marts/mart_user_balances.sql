CREATE OR REPLACE VIEW mart_user_balances AS
WITH calculated_balances AS (
    SELECT
        execution_id,
        user_id,
        SUM(signed_amount) AS sql_calculated_balance,
        COUNT(*) AS transaction_count,
        MAX(transaction_timestamp) AS last_transaction_timestamp
    FROM fact_transactions
    GROUP BY execution_id, user_id
)
SELECT
    balances.execution_id,
    balances.user_id,
    balances.balance AS stored_balance,
    calculated.sql_calculated_balance,
    balances.balance - COALESCE(calculated.sql_calculated_balance, 0) AS balance_difference,
    CASE
        WHEN calculated.sql_calculated_balance IS NULL THEN 'missing_transactions'
        WHEN ABS(balances.balance - calculated.sql_calculated_balance) <= 0.01 THEN 'matched'
        ELSE 'mismatch'
    END AS validation_status,
    COALESCE(calculated.transaction_count, 0) AS transaction_count,
    calculated.last_transaction_timestamp
FROM fact_user_balances AS balances
LEFT JOIN calculated_balances AS calculated
    ON balances.execution_id = calculated.execution_id
    AND balances.user_id = calculated.user_id;
