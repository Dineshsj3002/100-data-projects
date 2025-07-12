import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.title("🛒 Top 10 Orders by Basket Size")

@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname="basket_size_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
        SELECT order_id, COUNT(product_id) AS basket_size
        FROM order_items
        GROUP BY order_id
        ORDER BY basket_size DESC
        LIMIT 10;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = load_data()

fig = px.bar(
    data,
    x='basket_size',
    y='order_id',
    orientation='h',
    title='Top 10 Orders by Basket Size',
    color='basket_size',
    labels={'basket_size': 'Number of Products', 'order_id': 'Order ID'},
    height=500
)

fig.update_layout(yaxis=dict(autorange="reversed"))  # Largest basket on top

st.plotly_chart(fig)
st.dataframe(data)
