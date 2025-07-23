import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv(r'C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day17_IPL_Team_Performance_Summary\data\dataa.csv')

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

print("✅ Cleaned columns:", df.columns.tolist())

# Create DB connection
conn = psycopg2.connect(
    dbname='ipl_db',
    user='postgres',
    password='root123',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Create Table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS ipl_batting_stats (
        id SERIAL PRIMARY KEY,
        player TEXT,
        matches INT,
        innings INT,
        not_outs INT,
        runs INT,
        highest_score TEXT,
        average FLOAT,
        balls_faced INT,
        strike_rate FLOAT,
        hundreds INT,
        fifties INT,
        fours INT,
        sixes INT
    );
""")
conn.commit()

# Insert Data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO ipl_batting_stats (
            player, matches, innings, not_outs, runs,
            highest_score, average, balls_faced, strike_rate,
            hundreds, fifties, fours, sixes
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row['player'],
        int(row['mat']),
        int(row['inns']),
        int(row['no']),
        int(row['runs']),
        row['hs'],
        float(row['avg']) if row['avg'] != '-' else None,
        int(row['bf']),
        float(row['sr']),
        int(row['100']),
        int(row['50']),
        int(row['4s']),
        int(row['6s'])
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ Player stats loaded into PostgreSQL successfully.")
