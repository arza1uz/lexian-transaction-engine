WITH sql_balances AS (
    SELECT
        execution_id,
        user_id,
        SUM(signed_amount) AS sql_calculated_balance
    FROM fact_transactions
    GROUP BY
        execution_id,
        user_id
)

SELECT
    b.execution_id,
    b.user_id,
    b.balance AS stored_balance,
    s.sql_calculated_balance,
    b.balance - s.sql_calculated_balance AS balance_difference,
    CASE
        WHEN b.balance = s.sql_calculated_balance THEN 'matched'
        ELSE 'mismatch'
    END AS validation_status
FROM fact_user_balances AS b
LEFT JOIN sql_balances AS s
    ON b.execution_id = s.execution_id
    AND b.user_id = s.user_id
ORDER BY
    b.execution_id,
    b.user_id;
