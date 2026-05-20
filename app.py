import streamlit as st
import pandas as pd
import joblib
import numpy as np

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
model = joblib.load("car_model.joblib")

# ----------------------------
# FIXED CURRENT YEAR
# ----------------------------
current_year = 2025

# ----------------------------
# CAR DATA
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
    "Ford": ["E-350", "Ecosport", "Edge", "Escape", "Expedition",
             "Explorer", "F-150", "Flex", "Focus", "Fusion",
             "Galaxy", "Mustang", "Ranger", "Sport Trac", "Taurus"]
}

# ----------------------------
# FEATURE MAPS
# ----------------------------
luxury_brands = ["Lexus", "Mercedes-Benz", "BMW", "Audi"]

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
# STYLING
# ----------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
    url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2070&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

.main .block-container {
    padding: 35px;
    background: rgba(15, 23, 42, 0.45);
    border-radius: 25px;
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.1);
}

h1 {
    text-align: center;
    font-size: 62px;
    font-weight: 900;
    background: linear-gradient(to right, #ffffff, #dbeafe, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.subtitle {
    text-align: center;
    font-size: 28px;
    font-weight: 800;
    margin-top: -10px;
    background: linear-gradient(to right, #ffffff, #dbeafe, #93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

label {
    color: white !important;
    font-weight: 600 !important;
}

.prediction-box {
    padding: 30px;
    background: rgba(15, 23, 42, 0.75);
    border-radius: 20px;
    text-align: center;
    color: white;
    font-size: 34px;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1>🚘 DriveValuenG</h1>", unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Smart Nigerian Car Price Prediction System</div>',
    unsafe_allow_html=True
)

# ----------------------------
# FORM
# ----------------------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        make = st.selectbox(
            "Car Make",
            list(car_brands.keys())
        )

    with col2:
        model_name = st.selectbox(
            "Car Model",
            car_brands[make]
        )

    col3, col4 = st.columns(2)

    with col3:
        fuel_type = st.selectbox(
            "Fuel Type",
            ["Petrol", "Diesel", "Hybrid"]
        )

    with col4:
        gear_type = st.selectbox(
            "Gear Type",
            ["Automatic", "Manual"]
        )

    year = st.select_slider(
        "Select Car Year",
        options=list(range(1990, current_year + 1)),
        value=2021
    )

    col5, col6 = st.columns(2)

    with col5:
        mileage = st.number_input(
            "Mileage",
            0,
            value=50000,
            step=1000
        )

    with col6:
        engine_size = st.number_input(
            "Engine Size",
            0.8,
            8.0,
            value=2.0,
            step=0.1
        )

    condition = st.selectbox(
        "Condition",
        ["Foreign Used", "Nigerian Used"]
    )

    submit_button = st.form_submit_button(
        "🚀 Predict Car Price"
    )

# ----------------------------
# PREDICTION
# ----------------------------
if submit_button:

    try:

        # FEATURE ENGINEERING
        car_age = current_year - year
        car_age = max(car_age, 0)

        mileage_per_year = mileage / (car_age + 1)

        log_mileage = np.log1p(mileage)

        is_luxury = 1 if make in luxury_brands else 0

        brand_score = brand_score_map.get(make, 3)

        # INPUT DATAFRAME
        input_data = pd.DataFrame({
            "Make": [make],
            "Model": [model_name],
            "fuel type": [fuel_type],
            "gear type": [gear_type],
            "Condition": [condition],
            "Mileage": [mileage],
            "Engine Size": [engine_size],
            "Car Age": [car_age],
            "Mileage_per_year": [mileage_per_year],
            "Log_Mileage": [log_mileage],
            "Is_Luxury": [is_luxury],
            "Brand_Score": [brand_score]
        })

        # MODEL PREDICTION (LOG SCALE)
        prediction_log = model.predict(input_data)[0]

        # CONVERT BACK TO REAL PRICE
        prediction = np.expm1(prediction_log)

        # SAFETY FLOOR
        prediction = max(prediction, 500000)

        # DISPLAY RESULT
        st.markdown(f"""
        <div class="prediction-box">
            Estimated Car Price <br><br>
            ₦{prediction:,.0f}
        </div>
        """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("""
<div style='text-align:center;
color:rgba(255,255,255,0.6);
padding-top:20px;'>

🚘 DrivenG • AI Powered Nigerian Car Valuation

</div>
""", unsafe_allow_html=True)
