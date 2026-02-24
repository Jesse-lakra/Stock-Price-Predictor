import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# -----------------------
# Helper Functions
# -----------------------

def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

# -----------------------
# Sidebar Login Option
# -----------------------

st.sidebar.title("Login Panel")
option = st.sidebar.selectbox("Select Role", ["Admin", "User"])

# -----------------------
# ADMIN SECTION
# -----------------------

if option == "Admin":

    username = st.text_input("Admin Username")
    password = st.text_input("Admin Password", type="password")

    if st.button("Login as Admin"):
        if username == "admin" and password == "admin123":
            st.success("Admin Login Successful")

            uploaded_file = st.file_uploader("Upload Stock CSV", type=["csv"])

            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                st.write(df.head())

                df["Day"] = np.arange(len(df))

                X = df[["Day"]]
                y = df["Close"]

                model = LinearRegression()
                model.fit(X, y)

                joblib.dump(model, "model.pkl")
                st.success("Model Trained & Saved Successfully")

        else:
            st.error("Invalid Admin Credentials")

# -----------------------
# USER SECTION
# -----------------------

if option == "User":

    users = load_users()

    action = st.radio("Select Option", ["New User", "Existing User"])

    if action == "New User":
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            users[new_user] = new_pass
            save_users(users)
            st.success("User Registered! Please Login.")

    if action == "Existing User":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.success("Login Successful")

                model = joblib.load("model.pkl")

                future_days = np.arange(200, 205).reshape(-1, 1)
                prediction = model.predict(future_days)

                st.subheader("5 Day Stock Prediction")
                st.write(prediction)

            else:
                st.error("Invalid Credentials")