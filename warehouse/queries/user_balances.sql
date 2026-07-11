SELECT
    user_id,
    SUM(signed_amount) AS calculated_balance
FROM fact_transactions
GROUP BY user_id
ORDER BY user_id;
