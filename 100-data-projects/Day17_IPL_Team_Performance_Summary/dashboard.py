import pandas as pd
import streamlit as st
import psycopg2
import altair as alt

# 🏏 Dashboard Title
st.title("🏏 IPL Team Performance Dashboard")

# 📡 Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='ipl_db',
    user='postgres',
    password='root123',
    host='localhost',
    port='5432'
)

# 📥 Load Data
df = pd.read_sql("SELECT * FROM ipl_batting_stats", conn)
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]  # Clean column names
conn.close()

# 👁️ View columns (debug)
st.sidebar.subheader("📋 Available Columns")
st.sidebar.write(df.columns.tolist())

# 1️⃣ Most Sixes
six_col = '6s' if '6s' in df.columns else 'sixes' if 'sixes' in df.columns else None
if six_col:
    most_sixes = df.sort_values(by=six_col, ascending=False)[['player', six_col]].head(10)
    st.subheader("💥 Top 10 Players with Most Sixes")
    chart = alt.Chart(most_sixes).mark_bar().encode(
        x=alt.X(six_col, title="Number of Sixes"),
        y=alt.Y('player', sort='-x', title="Player"),
        tooltip=['player', six_col]
    ).properties(height=400)
    st.altair_chart(chart, use_container_width=True)
else:
    st.warning("❌ No column found for sixes (6s/sixes).")

# 2️⃣ Most Matches
if 'mat' in df.columns:
    most_matches = df.sort_values(by='mat', ascending=False)[['player', 'mat']].head(10)
    st.subheader("🎯 Players with Most Matches")
    st.bar_chart(most_matches.set_index('player'))

# 3️⃣ Highest Strike Rate
if 'sr' in df.columns:
    highest_sr = df[df['sr'] > 0].sort_values(by='sr', ascending=False)[['player', 'sr']].head(10)
    st.subheader("⚡ Highest Strike Rate")
    st.bar_chart(highest_sr.set_index('player'))

# 4️⃣ Top Run Scorers
if 'runs' in df.columns:
    top_scorers = df.sort_values(by='runs', ascending=False)[['player', 'runs']].head(10)
    st.subheader("🏆 Top Run Scorers")
    st.bar_chart(top_scorers.set_index('player'))

# 5️⃣ Top Fifties and Hundreds
if '50' in df.columns:
    st.subheader("🔥 Top 50s")
    top_50s = df.sort_values(by='50', ascending=False)[['player', '50']].head(10)
    st.bar_chart(top_50s.set_index('player'))

if '100' in df.columns:
    st.subheader("🔥 Top 100s")
    top_100s = df.sort_values(by='100', ascending=False)[['player', '100']].head(10)
    st.bar_chart(top_100s.set_index('player'))

# 🧠 Footer
st.markdown("---")
st.markdown("✨ *Built by you, powered by PostgreSQL + Streamlit + Pandas*")
