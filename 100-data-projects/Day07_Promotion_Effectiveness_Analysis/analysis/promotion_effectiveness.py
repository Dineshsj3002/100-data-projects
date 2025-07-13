import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="promotion_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
    SELECT
        item_type,
        ROUND(AVG(retail_sales)::numeric, 2) AS avg_retail_sales,
        ROUND(AVG(warehouse_sales)::numeric, 2) AS avg_warehouse_sales
    FROM promotion_effectiveness
    GROUP BY item_type
    ORDER BY avg_retail_sales DESC;
"""

df = pd.read_sql_query(query, conn)
conn.close()

print(df)
