CREATE OR REPLACE VIEW mart_balance_validation AS
WITH calculated_balances AS (
    SELECT
        execution_id,
        user_id,
        SUM(signed_amount) AS sql_calculated_balance
    FROM fact_transactions
    GROUP BY execution_id, user_id
), validation AS (
    SELECT
        balances.execution_id,
        balances.user_id,
        balances.balance AS stored_balance,
        calculated.sql_calculated_balance,
        ABS(balances.balance - COALESCE(calculated.sql_calculated_balance, 0)) AS absolute_difference,
        CASE
            WHEN calculated.sql_calculated_balance IS NULL THEN 'missing_transactions'
            WHEN ABS(balances.balance - calculated.sql_calculated_balance) <= 0.01 THEN 'matched'
            ELSE 'mismatch'
        END AS validation_status
    FROM fact_user_balances AS balances
    LEFT JOIN calculated_balances AS calculated
        ON balances.execution_id = calculated.execution_id
        AND balances.user_id = calculated.user_id
)
SELECT
    execution_id,
    user_id,
    stored_balance,
    sql_calculated_balance,
    absolute_difference,
    validation_status,
    CASE
        WHEN validation_status = 'matched' THEN 'info'
        WHEN sql_calculated_balance IS NULL THEN 'critical'
        WHEN absolute_difference > 10 THEN 'critical'
        WHEN absolute_difference > 0.01 THEN 'warning'
        ELSE 'info'
    END AS validation_severity
FROM validation;
