import pandas as pd
import psycopg2

# Load the CSV file
df = pd.read_csv(r"C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day20_Shopping_Basket_Insights\data\customer_shopping_data.csv")

# Clean up column names
df.columns = df.columns.str.strip().str.lower()

# Rename columns to match table format
df = df.rename(columns={
    'invoice_no': 'invoice_id',
    'price': 'price_per_unit',
    'invoice_date': 'shopping_date'
})

# Add total_amount column
df['total_amount'] = df['quantity'] * df['price_per_unit']

# Convert date
df['shopping_date'] = pd.to_datetime(df['shopping_date'], dayfirst=True)


# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="shopping_db",    
    user="postgres",
    password="root123",      
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Drop table if exists
cursor.execute("DROP TABLE IF EXISTS shopping_data;")

# Create new table
cursor.execute("""
    CREATE TABLE shopping_data (
        invoice_id TEXT,
        customer_id TEXT,
        gender TEXT,
        age INT,
        category TEXT,
        quantity INT,
        price_per_unit FLOAT,
        total_amount FLOAT,
        shopping_date DATE,
        payment_method TEXT,
        shopping_mall TEXT
    );
""")

# Insert each row
for _, row in df.iterrows():
    cursor.execute("""
        INSERT INTO shopping_data (
            invoice_id, customer_id, gender, age, category, quantity,
            price_per_unit, total_amount, shopping_date, payment_method, shopping_mall
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        row['invoice_id'],
        row['customer_id'],
        row['gender'],
        int(row['age']),
        row['category'],
        int(row['quantity']),
        float(row['price_per_unit']),
        float(row['total_amount']),
        row['shopping_date'].date(),
        row['payment_method'],
        row['shopping_mall']
    ))

# Commit changes and close
conn.commit()
cursor.close()
conn.close()

print("✅ Data loaded into PostgreSQL successfully.")
