import pandas as pd
import psycopg2

conn = psycopg2.connect(
    dbname="netflix_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
    SELECT
        country,
        COUNT(*) AS total_titles,
        AVG(release_year) AS avg_release_year
    FROM netflix_titles
    WHERE country IS NOT NULL
    GROUP BY country
    ORDER BY total_titles DESC
    LIMIT 10;
"""

df = pd.read_sql_query(query, conn)
print(df)
conn.close()
