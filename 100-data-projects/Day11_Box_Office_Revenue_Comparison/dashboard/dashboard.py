import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

st.set_page_config(page_title="Box Office Revenue Comparison", layout="wide")

@st.cache_data
def fetch_data():
    conn = psycopg2.connect(
        dbname="box_office_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
    SELECT 
        genre, 
        release_year, 
        ROUND(AVG(revenue)::numeric, 2) AS avg_revenue
    FROM box_office_revenue
    GROUP BY genre, release_year
    ORDER BY avg_revenue DESC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = fetch_data()

st.title("🎬 Box Office Revenue Comparison")

fig = px.bar(
    data,
    x="genre",
    y="avg_revenue",
    color="release_year",
    title="Average Box Office Revenue by Genre & Year"
)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(data)
