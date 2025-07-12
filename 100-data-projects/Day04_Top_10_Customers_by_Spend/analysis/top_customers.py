import pandas as pd
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="monthly_revenue_db",
    user="postgres",
    password="root123",  # Tip: Use env vars in production
    host="localhost",
    port="5432"
)

# SQL Query: Top 10 customers by total spend
query = """
    SELECT customer, ROUND(SUM(amount), 2) AS total_spend
    FROM customer_spending
    GROUP BY customer
    ORDER BY total_spend DESC
    LIMIT 10;
"""

# Read into DataFrame
try:
    df = pd.read_sql_query(query, conn)
    print(df)
except Exception as e:
    print("❌ Query failed:", e)
finally:
    conn.close()
