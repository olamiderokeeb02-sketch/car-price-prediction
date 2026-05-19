# ----------------------------
# SESSION STATE INIT
# ----------------------------
if "make" not in st.session_state:
    st.session_state.make = "Toyota"

if "model_name" not in st.session_state:
    st.session_state.model_name = car_brands["Toyota"][0]

# ----------------------------
# FORM
# ----------------------------
with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        make = st.selectbox(
            "Car Make",
            list(car_brands.keys()),
            key="make"
        )

    with col2:
        model_name = st.selectbox(
            "Car Model",
            car_brands[st.session_state.make],
            key="model_name"
        )
