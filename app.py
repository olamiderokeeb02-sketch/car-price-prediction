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
# SESSION STATE FIX (IMPORTANT)
# ----------------------------
if "last_make" not in st.session_state:
    st.session_state.last_make = "Toyota"

if "model_index" not in st.session_state:
    st.session_state.model_index = 0

# ----------------------------
# STYLE
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

    h1 {
        text-align: center;
        font-size: 62px;
        font-weight: 900;
        background: linear-gradient(to right, #ffffff, #dbeafe, #93c5fd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    h3 {
        text-align: center;
        font-size: 18px;
        color: #cbd5e1;
    }

    label {
        color: white !important;
        font-weight: 600 !important;
    }

    .stSelectbox > div > div,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.08) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
    }

    .stButton > button {
        width: 100%;
        background: rgba(255,255,255,0.08);
        color: white;
        border-radius: 14px;
        height: 58px;
        font-size: 19px;
        font-weight: bold;
        border: 1px solid rgba(255,255,255,0.18);
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

    # MAKE
    make = st.selectbox(
        "Car Make",
        list(car_brands.keys())
    )

    # RESET MODEL IF MAKE CHANGES
    if st.session_state.last_make != make:
        st.session_state.model_index = 0
        st.session_state.last_make = make

    # MODEL (ALWAYS REFRESHED)
    model_name = st.selectbox(
        "Car Model",
        car_brands[make],
        index=st.session_state.model_index
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

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# ----------------------------
# FOOTER
# ----------------------------
st.markdown(
    """
    <div style='text-align:center;color:rgba(255,255,255,0.7);padding-top:25px;font-size:14px;'>
        🚘 DrivenG • AI Powered Nigerian Car Valuation
    </div>
    """,
    unsafe_allow_html=True
)
