import mysql.connector
import pandas as pd
from dbconnection_project3 import dbread
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

query = "SELECT * FROM crop_data;"
df = dbread(query)
print(df.head()) 

df = df.dropna()

X = df[['area_harvested', 'yield', 'stocks', 'year']]  
y = df['production'] 

print(X.head(), y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.xlabel("Actual Production (tons)")
plt.ylabel("Predicted Production (tons)")
plt.title("Actual vs Predicted Crop Production")
plt.show()
