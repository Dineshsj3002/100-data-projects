import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.title("📅 Monthly Revenue Trends")

@st.cache_data
def load_data():
    conn = psycopg2.connect(
        dbname="monthly_revenue_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
        SELECT TO_CHAR(order_date, 'YYYY-MM') AS month,
               ROUND(SUM(sales), 2) AS total_revenue
        FROM orders
        GROUP BY month
        ORDER BY month;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Load + plot
data = load_data()
fig = px.line(data, x='month', y='total_revenue', title='Monthly Revenue Trend', markers=True)
fig.update_layout(xaxis_title='Month', yaxis_title='Revenue ($)', hovermode='x')

st.plotly_chart(fig)
st.dataframe(data)
