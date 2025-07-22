import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df = pd.read_csv(r'C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day16_Revenue_vs_Expenses_EDA\data\Superstore.csv', encoding='latin1')

# Ensure 'Order Date' is in datetime format
df['Order Date'] = pd.to_datetime(df['Order Date'], dayfirst=True)
# Create month column
df['Month'] = df['Order Date'].dt.to_period('M').astype(str)

# Calculate Expenses
df['Expenses'] = df['Sales'] - df['Profit']

# Group by Month
monthly = df.groupby('Month')[['Sales', 'Profit', 'Expenses']].sum().reset_index()
monthly.rename(columns={'Sales': 'Revenue'}, inplace=True)

# Plot trends
sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly, x='Month', y='Revenue', label='Revenue')
sns.lineplot(data=monthly, x='Month', y='Expenses', label='Expenses')
sns.lineplot(data=monthly, x='Month', y='Profit', label='Profit', linestyle='--')
plt.title('Monthly Revenue vs Expenses (Superstore)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
