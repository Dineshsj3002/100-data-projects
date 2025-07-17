# dashboard/dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import psycopg2

# App Config
st.set_page_config(
    page_title="Netflix Language & Country Trends",
    page_icon="🌍",
    layout="wide"
)

# --- Database Connection ---
@st.cache_resource
def init_connection():
    return psycopg2.connect(**st.secrets["postgres"])

try:
    conn = init_connection()
except psycopg2.OperationalError as e:
    st.error("❌ Database connection failed. Please check your secrets.toml and PostgreSQL service.")
    st.stop()

# --- Query Function ---
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return pd.DataFrame(cur.fetchall(), columns=[desc[0] for desc in cur.description])

# --- SQL Queries ---
query_country = """
    WITH unnested_countries AS (
        SELECT UNNEST(STRING_TO_ARRAY(country, ', ')) AS single_country
        FROM netflix_titles
        WHERE country IS NOT NULL
    )
    SELECT single_country, COUNT(*) AS count
    FROM unnested_countries
    WHERE single_country != ''
    GROUP BY single_country
    ORDER BY count DESC
    LIMIT 10;
"""

query_year = """
    SELECT EXTRACT(YEAR FROM date_added) AS year, COUNT(*) AS count
    FROM netflix_titles
    WHERE date_added IS NOT NULL
    GROUP BY year
    ORDER BY year;
"""

# --- Fetch Data ---
with st.spinner("📊 Fetching country data..."):
    df_country = run_query(query_country)

with st.spinner("📈 Fetching year trend data..."):
    df_year = run_query(query_year)

# --- Main Dashboard Layout ---
st.title("🌍 Netflix Content: A Look at Country & Language Trends")
st.markdown("Analyzing content trends by country of production as a proxy for language.")

col1, col2 = st.columns([2, 3])

with col1:
    st.subheader("Top Content Producing Countries (Proxy for Language)")
    fig_country = px.bar(
        df_country,
        x="count",
        y="single_country",
        orientation='h',
        title="Top 10 Countries by Title Count",
        labels={'count': 'Number of Titles', 'single_country': 'Country'},
        text='count'
    )
    fig_country.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig_country, use_container_width=True)

with col2:
    st.subheader("Titles Added to Netflix by Year")
    fig_year = px.line(
        df_year,
        x="year",
        y="count",
        title="Annual Number of Titles Added",
        labels={'year': 'Year', 'count': 'Number of Titles'}
    )
    fig_year.update_traces(mode='lines+markers')
    st.plotly_chart(fig_year, use_container_width=True)
