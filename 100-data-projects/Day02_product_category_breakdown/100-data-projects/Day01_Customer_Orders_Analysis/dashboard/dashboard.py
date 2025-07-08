import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt

# Title
st.title("📊 Customer Orders Summary Dashboard")

# DB connection
@st.cache_resource
def connect_db():
    return psycopg2.connect(
        dbname="customer_orders_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )

conn = connect_db()

# Load data
@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM customers", conn)

df = load_data()

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("👥 Unique Customers", df['customer_unique_id'].nunique())
col2.metric("🏙️ Total Cities", df['customer_city'].nunique())
col3.metric("🗺️ Total States", df['customer_state'].nunique())

st.markdown("---")

# Top cities
st.subheader("🏙️ Top 10 Cities by Customer Count")
top_cities = df['customer_city'].value_counts().head(10)
st.bar_chart(top_cities)

# Top states
st.subheader("🗺️ Top 10 States by Customer Count")
top_states = df['customer_state'].value_counts().head(10)
st.bar_chart(top_states)

# Raw Data toggle
with st.expander("📄 Show Raw Data"):
    st.dataframe(df)
