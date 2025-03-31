import mysql.connector
import pandas as pd
from dbconnection_project3 import dbread

query = "SELECT * FROM crop_data;"
df = dbread(query)
print(df.head())  # Now it's a DataFrame!shdfsl

# Drop rows with missing values
df = df.dropna()

# Select independent (X) and dependent (y) variables
X = df[['area_harvested', 'yield', 'stocks', 'year']]  # Features
y = df['production']  # Target variable

# Display sample of processed data
print(X.head(), y.head())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Split data (80% training, 20% testing)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate model
print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
print("R² Score:", r2_score(y_test, y_pred))

import matplotlib.pyplot as plt

plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
plt.xlabel("Actual Production (tons)")
plt.ylabel("Predicted Production (tons)")
plt.title("Actual vs Predicted Crop Production")
plt.show()
