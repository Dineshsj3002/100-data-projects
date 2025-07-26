SELECT 
    COUNT(*) AS total_transactions,
    SUM(fraud_indicator) AS fraud_count,
    COUNT(*) - SUM(fraud_indicator) AS non_fraud,
    ROUND(SUM(fraud_indicator)::numeric / COUNT(*) * 100, 2) AS fraud_percentage
FROM fraud_transactions;
