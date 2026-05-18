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
# CUSTOM STYLING
# ----------------------------
st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(to bottom right, #0f172a, #111827);
    }

    h1 {
        color: white;
        text-align: center;
        font-size: 52px;
        font-weight: bold;
    }

    h3 {
        color: #cbd5e1;
        text-align: center;
    }

    .block-container {
        padding-top: 2rem;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #2563eb, #3b82f6);
        color: white;
        border-radius: 12px;
        height: 55px;
        font-size: 18px;
        border: none;
        font-weight: bold;
    }

    .prediction-box {
        padding: 25px;
        background: #1e293b;
        border-radius: 15px;
        text-align: center;
        color: white;
        font-size: 32px;
        margin-top: 25px;
        border: 1px solid #334155;
    }

    label {
        color: white !important;
        font-weight: 500;
    }

    .stSelectbox, .stNumberInput, .stTextInput {
        background-color: #111827;
        border-radius: 10px;
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
    "Toyota": [
        "Camry", "Corolla", "Highlander",
        "RAV4", "Avalon", "Venza"
    ],
    "Honda": [
        "Accord", "Civic", "Pilot",
        "CR-V"
    ],
    "Lexus": [
        "ES350", "RX350", "GX460",
        "LX570"
    ],
    "Mercedes-Benz": [
        "C300", "E350", "GLK350",
        "ML350"
    ],
    "BMW": [
        "X5", "3 Series", "5 Series"
    ],
    "Hyundai": [
        "Elantra", "Sonata", "Tucson"
    ]
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

    # YEAR DROPDOWN FEATURE
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

    submit_button = st.form_submit_button(
        "🚀 Predict Car Price"
    )

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

        st.markdown(
            f"""
            <div class="prediction-box">
                🚗 Estimated Car Price <br><br>
                ₦{prediction:,.0f}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.balloons()

    except Exception as e:
        st.error(f"Prediction Error: {e}")

# ----------------------------
# FOOTER
# ----------------------------
st.write("")
st.caption("DrivenG • AI Powered Nigerian Car Valuation")
