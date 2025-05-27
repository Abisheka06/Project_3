import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from dbconnection_project3 import dbread

query = "SELECT * FROM crop_data;"
df = dbread(query)
print(df.head())  

plt.figure(figsize=(10, 5))
plt.plot(df["year"], df["production"], marker="o", linestyle="-", color="b")
plt.xlabel("Year")
plt.ylabel("Production (tons)")
plt.title("Crop Production Over the Years")
plt.grid()
plt.show()

df_sorted = df.sort_values(by="production", ascending=False).head(5)  
plt.figure(figsize=(10, 5))
plt.bar(df_sorted["year"], df_sorted["production"], color="green")
plt.xlabel("Year")
plt.ylabel("Production (tons)")
plt.title("Top 5 Years with Highest Production")
plt.show()

plt.figure(figsize=(8, 5))
plt.scatter(df["area_harvested"], df["production"], color="red", alpha=0.5)
plt.xlabel("Area Harvested (ha)")
plt.ylabel("Production (tons)")
plt.title("Relationship Between Area Harvested and Production")
plt.show()

