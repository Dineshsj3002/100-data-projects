
# analysis/analyze_products.py
import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="product_category_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
SELECT product_category, 
       SUM(order_quantity) AS total_quantity,
       SUM(total) AS total_revenue,
       AVG(discount_percent) AS avg_discount
FROM products
GROUP BY product_category
ORDER BY total_revenue DESC
LIMIT 10;
"""

# Load into DataFrame
df = pd.read_sql_query(query, conn)
print(df)
conn.close()
