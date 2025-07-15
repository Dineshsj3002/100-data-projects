import pandas as pd
import psycopg2

# Load CSV
file_path = r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day09_Netflix_Originals_Tracker\data\netflix_titles.csv"
df = pd.read_csv(file_path)
print(df.columns)

# Database connection
conn = psycopg2.connect(
    dbname="netflix_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table with "cast" in double quotes
cursor.execute("""
CREATE TABLE IF NOT EXISTS netflix_titles (
    show_id TEXT PRIMARY KEY,
    type TEXT,
    title TEXT,
    director TEXT,
    "cast" TEXT,
    country TEXT,
    date_added TEXT,
    release_year INT,
    rating TEXT,
    duration TEXT,
    listed_in TEXT,
    description TEXT
);
""")
conn.commit()

for _, row in df.iterrows():
    date_added = pd.to_datetime(row['date_added'], errors='coerce')
    date_added = None if pd.isna(date_added) else date_added

    cursor.execute("""
        INSERT INTO netflix_titles (
            show_id, type, title, director, "cast", country, date_added,
            release_year, rating, duration, listed_in, description
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (show_id) DO NOTHING
    """, (
        row['show_id'],
        row['type'],
        row['title'],
        row['director'],
        row['cast'],
        row['country'],
        date_added,
        int(row['release_year']),
        row['rating'],
        row['duration'],
        row['listed_in'],
        row['description']
    ))


conn.commit()
cursor.close()
conn.close()
print("✅ Netflix titles loaded successfully!")
