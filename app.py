import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# ----------------------------
# PAGE CONFIG
# ----------------------------
st.set_page_config(
    page_title="DrivenG - Car Predictor",
    page_icon="🚗",
    layout="centered"
)

# ----------------------------
# LOAD MODEL
# ----------------------------
model = joblib.load("car_model (1).joblib")

# ----------------------------
# FIXED BASE YEAR (same as training)
# ----------------------------
BASE_YEAR = 2026

# ----------------------------
# DATA
# ----------------------------
car_brands = {
    "Toyota": ["Camry", "Corolla", "Highlander", "RAV4", "Avalon", "Venza"],
    "Honda": ["Accord", "Civic", "Pilot", "CR-V"],
    "Lexus": ["ES350", "RX350", "GX460", "LX570"],
    "Mercedes-Benz": ["C300", "E350", "GLK350", "ML350"],
    "BMW": ["X5", "3 Series", "5 Series"],
    "Hyundai": ["Elantra", "Sonata", "Tucson"],
    "Acura": ["ILX", "MDX", "RDX", "RL", "TL", "TSX", "ZDX"],
    "Audi": ["A4", "A6", "A7", "Q5", "Q7"],
    "Ford": ["E-350", "Ecosport", "Edge", "Escape", "Explorer", "F-150", "Fusion", "Mustang"]
}

all_models = sorted(set([m for models in car_brands.values() for m in models]))

luxury_brands = ["Lexus", "Mercedes-Benz", "BMW"]

brand_score_map = {
    "Toyota": 5,
    "Honda": 5,
    "Lexus": 5,
    "BMW": 3,
    "Mercedes-Benz": 3,
    "Hyundai": 4,
    "Audi": 3,
    "Acura": 4,
    "Ford": 4
}

# ----------------------------
# UI
# ----------------------------
st.title("🚘 DriveValuenG")
st.write("Smart Nigerian Car Price Prediction System")

with st.form("form"):

    make = st.selectbox("Car Make", list(car_brands.keys()))
    model_name = st.selectbox("Car Model", all_models)

    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid"])
    gear_type = st.selectbox("Gear Type", ["Automatic", "Manual"])
    condition = st.selectbox("Condition", ["Foreign Used", "Nigerian Used"])

    year = st.slider("Car Year", 1990, BASE_YEAR, 2021)

    mileage = st.number_input("Mileage", 0, value=50000, step=1000)
    engine_size = st.number_input("Engine Size", 0.8, 8.0, value=2.0, step=0.1)

    submit = st.form_submit_button("🚀 Predict Price")

# ----------------------------
# PREDICTION
# ----------------------------
if submit:

    # ONLY FEATURE USED FOR AGE
    car_age = BASE_YEAR - year
    car_age = max(car_age, 1)

    input_data = pd.DataFrame({
        "Make": [make],
        "Model": [model_name],
        "fuel type": [fuel_type],
        "gear type": [gear_type],
        "Condition": [condition],
        "Mileage": [mileage],
        "Engine Size": [engine_size],
        "Car Age": [car_age],
        "Is_Luxury": [1 if make in luxury_brands else 0],
        "Brand_Score": [brand_score_map.get(make, 3)]
    })

    try:
        prediction = model.predict(input_data)[0]

        st.success(f"Estimated Price: ₦{prediction:,.0f}")

    except Exception as e:
        st.error(f"Error: {e}")
