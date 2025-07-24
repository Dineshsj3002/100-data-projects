import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

# Load the CSV
df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day18_Attendance_Heatmap\data\2018-2019_Daily_Attendance_20240429.csv")

# Clean column names
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Convert 'date' column to datetime
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d', errors='coerce')

# Drop rows with invalid/missing date
df = df.dropna(subset=['date'])

# PostgreSQL connection setup
conn = psycopg2.connect(
    dbname="school_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Drop and recreate table
cursor.execute("DROP TABLE IF EXISTS attendance;")
cursor.execute("""
    CREATE TABLE attendance (
        school_dbn TEXT,
        date DATE,
        enrolled INTEGER,
        absent INTEGER,
        present INTEGER,
        released INTEGER
    );
""")

# Prepare data as list of tuples
records = df[['school_dbn', 'date', 'enrolled', 'absent', 'present', 'released']].values.tolist()

# Use execute_values for bulk insert
execute_values(cursor, """
    INSERT INTO attendance (school_dbn, date, enrolled, absent, present, released)
    VALUES %s
""", records)

# Done!
conn.commit()
cursor.close()
conn.close()

print("✅ Data loaded into PostgreSQL successfully (fast mode).")
