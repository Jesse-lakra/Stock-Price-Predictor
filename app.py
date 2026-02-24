import streamlit as st
import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.linear_model import LinearRegression

# -----------------------
# Session State Setup
# -----------------------

if "admin_logged_in" not in st.session_state:
    st.session_state.admin_logged_in = False

if "user_logged_in" not in st.session_state:
    st.session_state.user_logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

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
# Sidebar
# -----------------------

st.sidebar.title("Login Panel")
option = st.sidebar.selectbox("Select Role", ["Admin", "User"])

# =====================================================
# ================= ADMIN SECTION =====================
# =====================================================

if option == "Admin":

    if not st.session_state.admin_logged_in:

        username = st.text_input("Admin Username")
        password = st.text_input("Admin Password", type="password")

        if st.button("Login as Admin"):
            if username == "admin" and password == "admin123":
                st.session_state.admin_logged_in = True
                st.rerun()
            else:
                st.error("Invalid Admin Credentials")

    else:
        st.success("Admin Logged In Successfully ✅")

        uploaded_file = st.file_uploader("Upload Stock CSV", type=["csv"])

        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())

            if "Close" not in df.columns:
                st.error("CSV must contain 'Close' column")
            else:
                df["Day"] = np.arange(len(df))

                X = df[["Day"]]
                y = df["Close"]

                model = LinearRegression()
                model.fit(X, y)

                joblib.dump(model, "model.pkl")
                st.success("Model Trained & Saved Successfully ✅")

        if st.button("Logout Admin"):
            st.session_state.admin_logged_in = False
            st.rerun()

# =====================================================
# ================= USER SECTION ======================
# =====================================================

if option == "User":

    users = load_users()

    action = st.radio("Select Option", ["New User", "Existing User"])

    # ---------------- Register ----------------

    if action == "New User":
        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Register"):
            if new_user in users:
                st.warning("User already exists!")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("User Registered Successfully ✅")

    # ---------------- Login ----------------

    if action == "Existing User":

        if not st.session_state.user_logged_in:

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if username in users and users[username] == password:
                    st.session_state.user_logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid Credentials")

        else:
            st.success(f"Welcome {st.session_state.username} 🎉")

            if not os.path.exists("model.pkl"):
                st.error("Model not trained yet. Please ask Admin to upload data.")
            else:
                model = joblib.load("model.pkl")

                future_days = np.arange(200, 205).reshape(-1, 1)
                prediction = model.predict(future_days)

                st.subheader("5 Day Stock Prediction 📈")
                st.write(prediction)

            if st.button("Logout User"):
                st.session_state.user_logged_in = False
                st.session_state.username = ""
                st.rerun()