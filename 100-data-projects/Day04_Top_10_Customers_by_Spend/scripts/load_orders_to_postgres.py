import pandas as pd
import psycopg2

# ✅ Load the correct CSV file
df = pd.read_csv(
    "C:/Users/sjdin/OneDrive/Documents/100-data-projects/Day04_Top_10_Customers_by_Spend/data/spend.csv",
    encoding='ISO-8859-1'
)

# ✅ Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="monthly_revenue_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ✅ Insert into the matching table
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO customer_spending (
            sl_no, customer, month, type, amount
        ) VALUES (%s, %s, %s, %s, %s)
    """, (
        row['Sl No:'],
        row['Customer'],
        row['Month'],
        row['Type'],
        float(row['Amount'])
    ))

conn.commit()
cursor.close()
conn.close()
print("✅ Data from spend.csv loaded successfully into customer_spending table!")

