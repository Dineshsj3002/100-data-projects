import streamlit as st
import pandas as pd
import plotly.express as px

# Load cleaned data
df = pd.read_csv('data/country_wise_latest.csv', skiprows=2)
df.columns = df.iloc[0]
df = df[1:]
df.reset_index(drop=True, inplace=True)
print(df.columns)
df.rename(columns={str(df.columns[0]): 'Region'}, inplace=True)

# Convert numeric columns properly (remove commas, percentages)
for col in df.columns[1:]:
    df[col] = df[col].replace({',': '', '%': ''}, regex=True)
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Sidebar Filters
st.sidebar.title("🩺 Filter by Region")
selected_region = st.sidebar.selectbox("Choose a Region", df["Region"].unique())

# Main
st.title("🏥 Hospital Bed Availability Stats")
st.markdown("Data: Hospital Region-wise Bed & ICU Availability (Projected vs Capacity)")

filtered = df[df['Region'] == selected_region]

st.subheader(f"📍 Stats for: {selected_region}")
st.dataframe(filtered.T.rename(columns={filtered.index[0]: "Value"}))

# Plot: Projected ICU Needs vs Capacity
icu_cols = [
    'Total ICU Beds',
    'Available ICU Beds',
    'ICU Beds Needed, Six Months',
    'ICU Beds Needed, Twelve Months',
    'ICU Beds Needed, Eighteen Months'
]

icu_df = filtered[icu_cols].T.reset_index()
icu_df.columns = ['Category', 'Count']

fig = px.bar(icu_df, x='Category', y='Count', text='Count',
             title="🧠 ICU Capacity vs Projected Demand", color='Category')
st.plotly_chart(fig)
