import pandas as pd
import psycopg2

# Load the dataset
df = pd.read_csv("C:/Users/sjdin/OneDrive/Documents/100-data-projects/Day14_Hospital_Bed_Availability_Stats/data/country_wise_latest.csv")

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="covid_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS covid_stats (
        country TEXT,
        confirmed INT,
        deaths INT,
        recovered INT,
        active INT,
        new_cases INT,
        new_deaths INT,
        new_recovered INT,
        death_rate FLOAT,
        recovery_rate FLOAT,
        death_per_recovery FLOAT,
        last_week_confirmed INT,
        week_change INT,
        week_percent_increase FLOAT,
        who_region TEXT
    );
""")

# Insert data
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO covid_stats VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        row["Country/Region"], row["Confirmed"], row["Deaths"], row["Recovered"],
        row["Active"], row["New cases"], row["New deaths"], row["New recovered"],
        row["Deaths / 100 Cases"], row["Recovered / 100 Cases"], row["Deaths / 100 Recovered"],
        row["Confirmed last week"], row["1 week change"], row["1 week % increase"], row["WHO Region"]
    ))

conn.commit()
cursor.close()
conn.close()

print("✅ COVID data loaded successfully.")
