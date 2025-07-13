import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Promotion Effectiveness", layout="wide")
st.title("📊 Promotion Effectiveness Dashboard")

@st.cache_data
def fetch_data():
    conn = psycopg2.connect(
        dbname="promotion_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
        SELECT
            item_type,
            ROUND(AVG(retail_sales)::numeric, 2) AS avg_retail_sales,
            ROUND(AVG(warehouse_sales)::numeric, 2) AS avg_warehouse_sales
        FROM promotion_effectiveness
        GROUP BY item_type
        ORDER BY avg_retail_sales DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = fetch_data()

col1, col2 = st.columns(2)

with col1:
    fig1 = px.bar(data, x='item_type', y='avg_retail_sales',
                  title="Average Retail Sales by Item Type",
                  color='avg_retail_sales', text_auto=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.bar(data, x='item_type', y='avg_warehouse_sales',
                  title="Average Warehouse Sales by Item Type",
                  color='avg_warehouse_sales', text_auto=True)
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("📄 Raw Data")
st.dataframe(data)
