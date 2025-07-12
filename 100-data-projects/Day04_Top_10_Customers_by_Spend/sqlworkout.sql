CREATE TABLE customer_spending (
    id SERIAL PRIMARY KEY,
    sl_no TEXT,
    customer TEXT,
    month TEXT,
    type TEXT,
    amount NUMERIC
);

SELECT * FROM customer_spending LIMIT 5;
SELECT COUNT(*) FROM customer_spending;
SELECT * FROM customer_spending;
SELECT * FROM customer_spending LIMIT 10;
SELECT customer, SUM(amount) FROM customer_spending GROUP BY customer;

SELECT COUNT(*) FROM customer_spending;
SELECT DISTINCT customer FROM customer_spending LIMIT 10;


