import streamlit as st
import pandas as pd
import psycopg2
import plotly.express as px

st.set_page_config(page_title="Netflix Originals Tracker", layout="wide")
st.title("🎬 Netflix Originals Tracker Dashboard")

@st.cache_data
def fetch_data():
    conn = psycopg2.connect(
        dbname="netflix_db",
        user="postgres",
        password="root123",
        host="localhost",
        port="5432"
    )
    query = """
        SELECT
            country,
            COUNT(*) AS total_titles
        FROM netflix_titles
        WHERE country IS NOT NULL
        GROUP BY country
        ORDER BY total_titles DESC
        LIMIT 15;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

data = fetch_data()

fig = px.bar(data, x='country', y='total_titles',
             title="Top Countries by Netflix Originals", color='total_titles', text_auto=True)

st.plotly_chart(fig, use_container_width=True)

st.dataframe(data)
