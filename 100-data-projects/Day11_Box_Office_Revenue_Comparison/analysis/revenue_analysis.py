import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="box_office_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
SELECT 
    genre, 
    release_year, 
    ROUND(AVG(revenue)::numeric, 2) AS avg_revenue
FROM box_office_revenue
GROUP BY genre, release_year
ORDER BY avg_revenue DESC;
"""

df = pd.read_sql_query(query, conn)
print(df.head())

conn.close()
