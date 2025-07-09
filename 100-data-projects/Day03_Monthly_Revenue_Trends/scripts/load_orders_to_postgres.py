import pandas as pd
import psycopg2

# Load CSV
df = pd.read_csv("data\superstore_final_dataset.csv", encoding='ISO-8859-1')

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="monthly_revenue_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Clean + insert rows
for _, row in df.iterrows():
    cursor.execute('''
        INSERT INTO orders (
            order_id, order_date, ship_date, ship_mode, customer_id, 
            customer_name, segment, country, city, state, postal_code, 
            region, product_id, category, sub_category, product_name, sales
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        row['Order_ID'],
        pd.to_datetime(row['Order_Date']).date(),
        pd.to_datetime(row['Ship_Date']).date(),
        row['Ship_Mode'], row['Customer_ID'], row['Customer_Name'], row['Segment'],
        row['Country'], row['City'], row['State'], str(row['Postal_Code']),
        row['Region'], row['Product_ID'], row['Category'], row['Sub_Category'],
        row['Product_Name'], float(row['Sales'])
    ))

conn.commit()
cursor.close()
conn.close()
print("✅ Orders loaded into PostgreSQL.")
