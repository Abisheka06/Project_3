import pandas as pd
import mysql.connector
from dbconnection_project3 import dbwrite

# Load and inspect the dataset
df = pd.read_excel("FAOSTAT_data.xlsx")
print("Raw Data Preview:")
print(df.head())

# Pivot the dataset to reshape it
df_cleaned = df.pivot_table(
    index=["Area", "Year"], 
    columns="Element", 
    values="Value",
    aggfunc='first'  # Prevents issues with duplicate entries
).reset_index()

# Rename columns for clarity
df_cleaned.rename(columns={
    "Area": "country",
    "Year": "year",
    "Area harvested": "area_harvested",
    "Yield": "yield",
    "Production": "production",
    "Stocks": "stocks"
}, inplace=True)

# Display cleaned dataset
print("Cleaned Data Preview:")
print(df_cleaned.head())

# 🔴 Ensure Column Names Match Before Inserting
print("Columns in df_cleaned:", df_cleaned.columns)

# ✅ Use the already cleaned data (DO NOT reload the Excel file again!)
# Insert query
insert_query = """
INSERT INTO crop_data (country, year, area_harvested, yield, production, stocks)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    area_harvested = VALUES(area_harvested),
    yield = VALUES(yield),
    production = VALUES(production),
    stocks = VALUES(stocks);
"""

# Convert DataFrame to list of tuples
data_to_insert = df_cleaned[['country', 'year', 'area_harvested', 'yield', 'production', 'stocks']].values.tolist()

# 🔴 Check Before Inserting into MySQL
print("Sample Data for MySQL Insertion:")
print(data_to_insert[:5])  # Show first 5 records

dbwrite(insert_query,data_to_insert)

print("Data inserted successfully!")
