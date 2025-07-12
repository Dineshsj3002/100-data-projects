import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="basket_size_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
    SELECT order_id, COUNT(product_id) AS basket_size
    FROM order_items
    GROUP BY order_id
    ORDER BY basket_size DESC
    LIMIT 10;
"""

df = pd.read_sql_query(query, conn)
conn.close()

print("✅ Top 10 Orders by Basket Size:")
print(df.to_string(index=False))
