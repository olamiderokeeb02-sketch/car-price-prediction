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
# CUSTOM STYLING (LUXURY UPGRADE)
# ----------------------------
st.markdown(
    """
    <style>

    /* LUXURY CAR BACKGROUND */
    .stApp {
        background:
            linear-gradient(rgba(0,0,0,0.70), rgba(0,0,0,0.80)),
            url("https://images.unsplash.com/photo-1503376780353-7e6692767b70?q=80&w=2070&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* GLASS CONTAINER */
    .main .block-container {
        padding: 35px;
        background: rgba(15, 23, 42, 0.45);
        border-radius: 25px;
        backdrop-filter: blur(14px);
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* REMOVE STREAMLIT DEFAULT UI */
    header, footer {
        visibility: hidden;
    }

    /* TITLE */
    h1 {
        text-align: center;
        font-size: 58px;
        font-weight: 900;

        background: linear-gradient(to right, #ffffff, #dbeafe, #60a5fa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        text-shadow: 0px 0px 25px rgba(96,165,250,0.4);
    }

    /* SUBTITLE */
    h3 {
        text-align: center;
        color: #cbd5e1;
        font-size: 18px;
        font-weight: 400;
    }

    /* LABELS */
    label {
        color: white !important;
        font-weight: 600 !important;
    }

    /* INPUT FIELDS */
    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.12) !important;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background: linear-gradient(to right, #2563eb, #3b82f6);
        color: white;
        border-radius: 14px;
        height: 58px;
        font-size: 18px;
        border: none;
        font-weight: bold;
        box-shadow: 0px 10px 25px rgba(37,99,235,0.3);
    }

    .stButton > button:hover {
        transform: scale(1.02);
        transition: 0.2s ease-in-out;
    }

    /* RESULT BOX */
    .prediction-box {
        padding: 25px;
        background: rgba(15, 23, 42, 0.75);
        border-radius: 18px;
        text-align: center;
        color: white;
        font-size: 32px;
        margin-top: 25px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# HEADER
# ----------------------------
st.markdown("<h1>🚘 DriveValuenG</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3>Smart Nigerian Car Price Prediction System</h3>",
    unsafe_allow_html=True
)

st.write("")

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

    # YEAR DROPDOWN
    current_year = datetime.now().year

    year = st.select_slider(
        "Select Car Year",
        options=list(range(1990, current_year + 1)),
        value=2015
    )

    col5, col6 = st.columns(2)

    with col5:
        mileage = st.number_input(
            "Mileage",
            min_value=0,
            value=50000,
            step=1000
        )

    with col6:
        engine_size = st.number_input(
            "Engine Size",
            min_value=0.8,
            max_value=8.0,
            value=2.0,
            step=0.1
        )

    condition = st.selectbox(
        "Condition",
        ["Foreign Used", "Nigerian Used", "Brand New"]
    )

    selling_condition = st.selectbox(
        "Selling Condition",
        ["Clean", "Accidented", "Refurbished"]
    )

    bought_condition = st.selectbox(
        "Bought Condition",
        ["New", "Used"]
    )

    st.write("")

    submit_button = st.form_submit_button("🚀 Predict Car Price")
