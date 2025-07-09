import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="monthly_revenue_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
SELECT 
    TO_CHAR(order_date, 'YYYY-MM') AS month,
    ROUND(SUM(sales), 2) AS total_revenue
FROM orders
GROUP BY month
ORDER BY month;
"""

df = pd.read_sql_query(query, conn)
print(df)
conn.close()
