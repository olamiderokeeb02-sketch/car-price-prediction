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
model = joblib.load("car_model.joblib")

# ----------------------------
# CAR DATA
# ----------------------------
car_brands = {
    "Toyota": ["Camry", "Corolla", "Highlander", "RAV4", "Avalon", "Venza"],
    "Honda": ["Accord", "Civic", "Pilot", "CR-V"],
    "Lexus": ["ES350", "RX350", "GX460", "LX570"],
    "Mercedes-Benz": ["C300", "E350", "GLK350", "ML350"],
    "BMW": ["X5", "3 Series", "5 Series"],
    "Hyundai": ["Elantra", "Sonata", "Tucson"]
}

# ----------------------------
# CUSTOM STYLING
# ----------------------------
st.markdown(
    """
    <style>

    .stApp {
        background:
            linear-gradient(rgba(0,0,0,0.65), rgba(0,0,0,0.65)),
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

    header, footer {
        visibility: hidden;
    }

    /* TITLE */
    h1 {
        text-align: center;
        font-size: 62px;
        font-weight: 900;

        background: linear-gradient(to right, #ffffff, #dbeafe, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow: 0px 0px 20px rgba(147,197,253,0.35);
    }

    /* SUBTITLE */
    h3 {
        text-align: center;
        font-size: 18px;
        font-weight: 400;

        background: linear-gradient(to right, #e2e8f0, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    label {
        color: white !important;
        font-weight: 600 !important;
    }

    /* INPUTS */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background: rgba(255,255,255,0.08);
        color: white;
        border-radius: 14px;
        height: 58px;
        font-size: 19px;
        border: 1px solid rgba(255,255,255,0.18);
        font-weight: bold;
        backdrop-filter: blur(10px);
    }

    .stButton > button:hover {
        background: rgba(255,255,255,0.15);
        transform: scale(1.02);
    }

    /* RESULT BOX */
    .prediction-box {
        padding: 30px;
        background: rgba(15, 23, 42, 0.75);
        border-radius: 20px;
        text-align: center;
        color: white;
        font-size: 34px;
        margin-top: 30px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1>🚘 DriveValuenG</h1>", unsafe_allow_html=True)
st.markdown("<h3>Smart Nigerian Car Price Prediction System</h3>", unsafe_allow_html=True)

# ----------------------------
# FORM
# ----------------------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    # ✅ FIXED DEPENDENCY (THIS IS THE IMPORTANT PART)
    with col1:
        make = st.selectbox(
            "Car Make",
            list(car_brands.keys())
        )

    with col2:
        model_name = st.selectbox(
            "Car Model",
            car_brands[make]   # 👈 THIS FIXES THE ISSUE
        )

    col3, col4 = st.columns(2)

    with col3:
        fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Hybrid"])

    with col4:
        gear_type = st.selectbox("Gear Type", ["Automatic", "Manual"])

    current_year = datetime.now().year

    year = st.select_slider(
        "Select Car Year",
        options=list(range(1990, current_year + 1)),
        value=2015
    )

    col5, col6 = st.columns(2)

    with col5:
        mileage = st.number_input("Mileage", 0, value=50000, step=1000)

    with col6:
        engine_size = st.number_input("Engine Size", 0.8, 8.0, value=2.0, step=0.1)

    condition = st.selectbox("Condition", ["Foreign Used", "Nigerian Used", "Brand New"])
    selling_condition = st.selectbox("Selling Condition", ["Clean", "Accidented", "Refurbished"])
    bought_condition = st.selectbox("Bought Condition", ["New", "Used"])

    submit_button = st.form_submit_button("🚀 Predict Car Price")

# ----------------------------
# PREDICTION
# ----------------------------
if submit_button:

    car_age = current_year - year

    input_data = pd.DataFrame({
        "Make": [make],
        "Model": [model_name],
        "fuel type": [fuel_type],
        "gear type": [gear_type],
        "Condition": [condition],
        "Mileage": [mileage],
        "Engine Size": [engine_size],
        "Selling Condition": [selling_condition],
        "Bought Condition": [bought_condition],
        "Car Age": [car_age]
    })

    try:
        prediction = model.predict(input_data)[0]

        st.markdown(f"""
        <div class="prediction-box">
            🚗 Estimated Car Price <br><br>
            ₦{prediction:,.0f}
        </div>
        """, unsafe_allow_html=True)

        st.balloons()

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown(
    """
    <div style='
        text-align: center;
        color: rgba(255,255,255,0.7);
        padding-top: 25px;
        font-size: 14px;
        letter-spacing: 0.5px;
    '>
        🚘 DrivenG • AI Powered Nigerian Car Valuation
    </div>
    """,
    unsafe_allow_html=True
)
