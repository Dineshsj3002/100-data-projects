# dashboard/dashboard.py
import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

# Connect to PostgreSQL
def load_data():
    conn = psycopg2.connect(
        dbname="product_category_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
        SELECT product_category, 
               SUM(order_quantity) AS total_quantity,
               SUM(total) AS total_revenue,
               AVG(discount_percent) AS avg_discount
        FROM products
        GROUP BY product_category
        ORDER BY total_revenue DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Streamlit UI
st.title("📦 Top 10 Product Categories by Revenue")
data = load_data()

fig = px.bar(
    data, 
    x='product_category', 
    y='total_revenue', 
    title="Top Product Categories by Revenue",
    color='avg_discount',
    hover_data=['total_quantity']
)

st.plotly_chart(fig)
st.dataframe(data)

if st.checkbox("Show Raw SQL"):
    st.code("""
        SELECT product_category, 
               SUM(order_quantity) AS total_quantity,
               SUM(total) AS total_revenue,
               AVG(discount_percent) AS avg_discount
        FROM products
        GROUP BY product_category
        ORDER BY total_revenue DESC
        LIMIT 10;
    """)
