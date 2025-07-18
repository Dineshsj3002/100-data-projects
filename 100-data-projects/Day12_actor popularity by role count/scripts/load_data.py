import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day12_actor popularity by role count\data\robertdowneyjr.csv")

# Clean up column names
df.columns = df.columns.str.strip()

# Identify the correct actor column
actor_column = [col for col in df.columns if col.lower() == 'actors'][0]
print("✅ Actor column identified as:", actor_column)

# PostgreSQL Connection
conn = psycopg2.connect(
    dbname="actor_roles_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS actor_roles;")
cursor.execute("""
    CREATE TABLE actor_roles (
        title TEXT,
        actor_name TEXT
    );
""")
conn.commit()

for _, row in df.iterrows():
    title = row['Title'].strip() if pd.notnull(row['Title']) else None
    actors_raw = row[actor_column]

    if pd.notnull(actors_raw) and title:
        actors_list = [actor.strip() for actor in actors_raw.split(",") if actor.strip()]

        for actor in actors_list:
            cursor.execute("""
                INSERT INTO actor_roles (title, actor_name)
                VALUES (%s, %s)
            """, (title, actor))

conn.commit()
cursor.close()
conn.close()

print("✅ Actor Roles Data Loaded Successfully!")
