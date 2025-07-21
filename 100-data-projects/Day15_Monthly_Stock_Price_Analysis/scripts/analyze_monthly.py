import pandas as pd
from pathlib import Path

# Define base path to make the script more portable
# This assumes the script is in the 'scripts' directory and data is in 'data'
BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_CSV = BASE_DIR / "data" / "BAJAJFINSV.csv"
OUTPUT_CSV = BASE_DIR / "data" / "monthly_stock_summary.csv"

# Load the data
df = pd.read_csv(INPUT_CSV, parse_dates=["Date"])

# Extract Year and Month
df["YearMonth"] = df["Date"].dt.to_period("M")

# Group by Month and calculate Open (first), Close (last), High (max), Low (min), and Volume (sum)
monthly_summary = df.groupby("YearMonth").agg({
    "Open": "first",
    "Close": "last",
    "High": "max",
    "Low": "min",
    "Volume": "sum"
}).reset_index()

# Convert period to datetime for plotting
monthly_summary["YearMonth"] = monthly_summary["YearMonth"].dt.to_timestamp()

# Save processed data
monthly_summary.to_csv(OUTPUT_CSV, index=False)
print("✅ Monthly summary saved.")
