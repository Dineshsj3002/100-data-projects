import pandas as pd
import psycopg2

# Load CSV file — adjust path if needed
df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day06_Refund_Returns_Ratio\data\ecommerce_returns_synthetic_data.csv")
print("Columns:", df.columns)

# PostgreSQL connection
conn = psycopg2.connect(
    dbname="returns_ratio_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert rows into returns table using actual column names
for _, row in df.iterrows():
    cur.execute(
        "INSERT INTO returns (order_id, is_returned) VALUES (%s, %s)",
        (row['Order_ID'], row['Return_Status'] == 'Returned')
    )

conn.commit()
cur.close()
conn.close()
print("✅ Returns data loaded into returns table.")
