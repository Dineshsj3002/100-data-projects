import pandas as pd
import psycopg2

df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day07_Promotion_Effectiveness_Analysis\Data\Retail and wherehouse Sale.csv")
print(df.columns)

conn = psycopg2.connect(
    dbname="promotion_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO promotion_effectiveness (
            year, month, supplier, item_code, item_description, 
            item_type, retail_sales, retail_transfers, warehouse_sales
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        int(row['YEAR']),
        int(row['MONTH']),
        row['SUPPLIER'],
        row['ITEM CODE'],
        row['ITEM DESCRIPTION'],
        row['ITEM TYPE'],
        float(row['RETAIL SALES']),
        float(row['RETAIL TRANSFERS']),
        float(row['WAREHOUSE SALES'])
    ))

conn.commit()
cursor.close()
conn.close()
print("✅ Data loaded successfully!")
