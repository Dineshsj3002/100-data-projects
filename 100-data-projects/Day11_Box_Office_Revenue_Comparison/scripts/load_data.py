import pandas as pd
import psycopg2

# Load CSV
file_path = r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day11_Box_Office_Revenue_Comparison\data\MovieFranchises.csv"
df = pd.read_csv(file_path)
print(df.columns)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="box_office_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create Table with NUMERIC for large values
cursor.execute("""
    CREATE TABLE IF NOT EXISTS box_office_data (
        movie_id TEXT,
        title TEXT,
        lifetime_gross NUMERIC,
        year INT,
        studio TEXT,
        rating TEXT,
        runtime TEXT,
        budget NUMERIC,
        release_date TEXT,
        vote_avg FLOAT,
        vote_count INT,
        franchise_id TEXT
    );
""")
conn.commit()

# Clean and Prepare DataFrame
df['Lifetime Gross'] = df['Lifetime Gross'].astype(str).str.replace(",", "").replace("nan", "0")
df['Budget'] = df['Budget'].astype(str).str.replace(",", "").replace("nan", "0")
# Filter only rows where Year column is numeric
df = df[pd.to_numeric(df['Year'], errors='coerce').notnull()]

# Insert with validation
for _, row in df.iterrows():
    try:
        lifetime_gross = float(row['Lifetime Gross']) if row['Lifetime Gross'].isnumeric() else 0
        budget = float(row['Budget']) if row['Budget'].isnumeric() else 0

        cursor.execute("""
            INSERT INTO box_office_data (
                movie_id, title, lifetime_gross, year, studio, rating,
                runtime, budget, release_date, vote_avg, vote_count, franchise_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row['MovieID'],
            row['Title'],
            lifetime_gross,
            int(row['Year']) if pd.notnull(row['Year']) else None,
            row['Studio'],
            row['Rating'],
            row['Runtime'],
            budget,
            row['ReleaseDate'],
            float(row['VoteAvg']) if pd.notnull(row['VoteAvg']) else None,
            int(row['VoteCount']) if pd.notnull(row['VoteCount']) else None,
            row['FranchiseID']
        ))
    except Exception as e:
        print(f"Skipping row {row['MovieID']} due to error: {e}")

conn.commit()
cursor.close()
conn.close()

print("✅ Box Office Revenue Data Loaded!")
