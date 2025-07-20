import pandas as pd

file_path = r'C:\Users\sjdin\OneDrive\Documents\100-data-projects\Day14_Hospital_Bed_Availability_Stats\data\data.csv'  # Adjust to your actual path

# Read the CSV correctly
df = pd.read_csv(file_path, header=2)
df.rename(columns={df.columns[0]: 'Region'}, inplace=True)

print("✅ Data loaded successfully!")
print("📊 Available columns:", df.columns.tolist())
