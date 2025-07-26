import pandas as pd
import psycopg2

# Load the CSV
df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day19_Real_Estate_Fraud_Detector\data\fraud_indicators.csv")

# Rename columns to lowercase and snake_case
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="fraud_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Create the table
cursor.execute("DROP TABLE IF EXISTS fraud_transactions;")
cursor.execute("""
    CREATE TABLE fraud_transactions (
        transaction_id TEXT PRIMARY KEY,
        fraud_indicator INTEGER
    );
""")

# Insert data row by row
# Insert data row by row with proper casting
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO fraud_transactions (transaction_id, fraud_indicator)
        VALUES (%s, %s)
        ON CONFLICT (transaction_id) DO NOTHING;
    """, (
        str(row['transactionid']),
        int(row['fraudindicator'])
    ))

# Finalize
conn.commit()
cursor.close()
conn.close()
print("✅ Data loaded into PostgreSQL successfully!")
