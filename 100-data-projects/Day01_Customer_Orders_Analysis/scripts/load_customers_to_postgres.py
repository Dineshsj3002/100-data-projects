import pandas as pd
import psycopg2

# Load CSV data
df = pd.read_csv(r'C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day01_Customer_Orders_Analysis\data\olist_customers_dataset.csv')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="customer_orders_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Insert each row
for _, row in df.iterrows():
    cur.execute("""
        INSERT INTO customers (customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        row['customer_id'],
        row['customer_unique_id'],
        int(row['customer_zip_code_prefix']),
        row['customer_city'],
        row['customer_state']
    ))

conn.commit()
cur.close()
conn.close()

print("✅ Data inserted successfully!")
