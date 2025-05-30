import streamlit as st
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from dbconnection_project3 import dbread

st.set_page_config(page_title="Crop Production Prediction", page_icon="🌾", layout="wide")


st.sidebar.title("🌍 Navigation")
page = st.sidebar.radio("Go to", ["📊 Display Data", "📈 Graphs", "🔮 Prediction Model"])

query = "SELECT * FROM crop_data;"
df = dbread(query)
print(df.head())

if page == "📊 Display Data":
    st.title("📊 Crop Data Table")
    st.write("### PIVOTED TABLE WITH NECCESARY INFORMATION")
    st.dataframe(df)

elif page == "📈 Graphs":
    st.title("📈 Crop Data Visualizations")

    st.subheader("🌾 Crop Production Over the Years")
    plt.figure(figsize=(10, 5))
    plt.plot(df["year"], df["production"], marker="o", linestyle="-", color="b")
    plt.xlabel("Year")
    plt.ylabel("Production (tons)")
    plt.title("Crop Production Over the Years")
    plt.grid()
    st.pyplot(plt)

    st.subheader("🏆 Top 5 Years with Highest Production")
    df_sorted = df.sort_values(by="production", ascending=False).head(5)
    plt.figure(figsize=(10, 5))
    plt.bar(df_sorted["year"], df_sorted["production"], color="green")
    plt.xlabel("Year")
    plt.ylabel("Production (tons)")
    plt.title("Top 5 Years with Highest Production")
    st.pyplot(plt)

    st.subheader("📉 Relationship Between Area Harvested and Production")
    plt.figure(figsize=(8, 5))
    plt.scatter(df["area_harvested"], df["production"], color="red", alpha=0.5)
    plt.xlabel("Area Harvested (ha)")
    plt.ylabel("Production (tons)")
    plt.title("Area Harvested vs. Production")
    st.pyplot(plt)

elif page == "🔮 Prediction Model":
    st.title("🔮 Crop Production Prediction")

    df = df.dropna()
    X = df[['area_harvested', 'yield', 'stocks', 'year']]
    y = df['production']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)

    st.subheader("🔢 Enter Input Values for Prediction")
    area_harvested = st.number_input("Area Harvested (ha)", min_value=1.0, value=10000.0)
    yield_value = st.number_input("Yield (kg/ha)", min_value=1.0, value=5000.0)
    stocks = st.number_input("Stocks (tons)", min_value=1.0, value=50000.0)
    year = st.number_input("Year", min_value=2000, max_value=2100, value=2025)

    if st.button("🔮 Predict Crop Production"):
        input_data = pd.DataFrame([[area_harvested, yield_value, stocks, year]], columns=X.columns)
        prediction = model.predict(input_data)[0]
        st.success(f"🌾 Predicted Crop Production: {prediction:.2f} tons")
        
    st.subheader("📈 Model Performance")
    y_pred = model.predict(X_test)

    plt.figure(figsize=(8,5))
    plt.scatter(y_test, y_pred, color='blue', alpha=0.5)
    plt.xlabel("Actual Production (tons)")
    plt.ylabel("Predicted Production (tons)")
    plt.title("Actual vs Predicted Crop Production")
    st.pyplot(plt)



