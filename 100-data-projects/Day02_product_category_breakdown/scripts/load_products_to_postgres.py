import pandas as pd
import psycopg2

# Load the CSV file
file_path = "C:/Users/sjdin/OneDrive/Documents/100-data-projects/Day02_product_category_breakdown/data/data.csv"  # Adjust if needed
df = pd.read_csv(file_path)

# 🧽 Clean monetary columns
df['Sub Total'] = df['Sub Total'].replace('[\$,]', '', regex=True).astype(float)
df['Total'] = df['Total'].replace('[\$,]', '', regex=True).astype(float)
df['Discount %'] = df['Discount %'].str.replace('%', '').astype(float)
# 🧽 Clean date column
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)


# PostgreSQL DB connection
try:
    conn = psycopg2.connect(
        dbname="product_category_db",   # change to your DB name
        user="postgres",                # change to your username
        password="root123",       # 👈 your actual password
        host="localhost",
        port="5432"
    )
    cursor = conn.cursor()
    print("✅ Connected to PostgreSQL database.")
# Handle missing values
    df.fillna({
        'Order Quantity': 0,
        'Discount %': 0,
        'Sub Total': 0,
        'Total': 0
    }, inplace=True)

    # Insert data row-by-row
    for _, row in df.iterrows():
        cursor.execute('''
            INSERT INTO products (
                product_name,
                product_category,
                order_quantity,
                subtotal,
                discount_percent,
                total,
                city,
                state,
                order_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            row['Product Name'],
            row['Product Category'],
            int(row['Order Quantity']),
            row['Sub Total'],
            float(row['Discount %']),
            row['Total'],
            row['City'],
            row['State'],
            row['Order Date'].date()
        ))

    conn.commit()
    print("✅ Data loaded successfully into PostgreSQL.")

except Exception as e:
    print("❌ Error:", e)

finally:
    cursor.close()
    conn.close()
