import pandas as pd
import mysql.connector
from dbconnection_project3 import dbwrite

df = pd.read_excel("FAOSTAT_data.xlsx")
print("Raw Data Preview:")
print(df.head())

df_cleaned = df.pivot_table(
    index=["Area", "Year"], 
    columns="Element", 
    values="Value",
    aggfunc='first'  
).reset_index()

df_cleaned.rename(columns={
    "Area": "country",
    "Year": "year",
    "Area harvested": "area_harvested",
    "Yield": "yield",
    "Production": "production",
    "Stocks": "stocks"
}, inplace=True)


print("Cleaned Data Preview:")
print(df_cleaned.head())

print("Columns in df_cleaned:", df_cleaned.columns)

insert_query = """
INSERT INTO crop_data (country, year, area_harvested, yield, production, stocks)
VALUES (%s, %s, %s, %s, %s, %s)
ON DUPLICATE KEY UPDATE 
    area_harvested = VALUES(area_harvested),
    yield = VALUES(yield),
    production = VALUES(production),
    stocks = VALUES(stocks);
"""

data_to_insert = df_cleaned[['country', 'year', 'area_harvested', 'yield', 'production', 'stocks']].values.tolist()

print("Sample Data for MySQL Insertion:")
print(data_to_insert[:5])

dbwrite(insert_query,data_to_insert)

print("Data inserted successfully!")
