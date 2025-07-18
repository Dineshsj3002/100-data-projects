import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

conn = psycopg2.connect(
    dbname="actor_roles_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

query = """
    SELECT actor_name, SUM(role_count) AS total_roles
    FROM actor_role_counts
    GROUP BY actor_name
    ORDER BY total_roles DESC
    LIMIT 20;
"""
df = pd.read_sql_query(query, conn)
print(df.head())

plt.figure(figsize=(12, 8))
plt.barh(df['actor_name'], df['total_roles'], color='skyblue')
plt.gca().invert_yaxis()
plt.title("Top 20 Actors by Role Count")
plt.xlabel("Total Roles")
plt.tight_layout()
plt.show()

conn.close()
