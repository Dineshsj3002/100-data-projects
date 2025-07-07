import pandas as pd
import matplotlib.pyplot as plt
import psycopg2

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="customer_orders_db",
    user="postgres",
    password="root123",
    host="localhost",
    port="5432"
)

# Load the data from the DB
df = pd.read_sql("SELECT * FROM customers", conn)
conn.close()

# Summary
print("📊 Summary:")
print(f"Total customers: {df['customer_unique_id'].nunique()}")
print(f"Top 5 cities:\n{df['customer_city'].value_counts().head()}")
print(f"Top 5 states:\n{df['customer_state'].value_counts().head()}")

# Plot top 10 cities
df['customer_city'].value_counts().head(10).plot(kind='bar', title='Top 10 Cities by Customers', color='skyblue')
plt.ylabel('Number of Customers')
plt.xlabel('City')
plt.tight_layout()
plt.show()
