import sys
import os
import streamlit as st

# Ensure project root is in PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.mlpipeline.predict import RatePrediction, PredictionConfig


# Cache the model so it loads only once
@st.cache_resource
def load_model():
    return RatePrediction(PredictionConfig())


# -----------------------------
#       PAGE LAYOUT
# -----------------------------
st.set_page_config(
    page_title="Hotel Rate Predictor",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Hotel Rate Predictor")
st.caption("AI‑powered pricing recommendation engine for hotel revenue teams")


# -----------------------------
#       INPUT FORM
# -----------------------------
with st.form("rate_form"):

    st.subheader("Booking Details")

    col1, col2 = st.columns(2)

    with col1:
        property_id = st.selectbox(
            "Property ID", ["19559", "17559", "18563", "19558", "18561"]
        )
        check_in_day = st.date_input("Check‑in Date").strftime("%Y-%m-%d")
        number_of_guest = st.number_input("Number of Guests", min_value=1, max_value=10)
        number_of_night = st.number_input("Number of Nights", min_value=1, max_value=30)

    with col2:
        guest_rating_score = st.slider("Guest Rating Score", 1, 5)
        city = st.selectbox("City", ["Bangalore", "Delhi", "Hyderabad", "Mumbai"])
        category = st.selectbox("Category", ["Economy", "Luxury"])
        season = st.selectbox(
            "Season", ["High Season", "Low Season", "Peak", "Shoulder"]
        )

    st.subheader("Room & Channel Details")

    col3, col4 = st.columns(2)

    with col3:
        room_class = st.selectbox(
            "Room Class", ["Standard", "Elite", "Premium", "Presidential"]
        )
        room_type = st.selectbox("Room Type", ["RT1", "RT2", "RT3", "RT4"])

    with col4:
        booking_channel = st.selectbox(
            "Booking Channel",
            [
                "makeyourtrip",
                "direct offline",
                "others",
                "journey",
                "direct online",
                "logtrip",
                "tripster",
            ],
        )
        day_type = st.selectbox("Day Type", ["weekday", "weekend"])

    hurdle_rate = st.number_input("Hurdle Rate (INR)", min_value=0.0, step=0.01)

    confirmed = st.checkbox("I confirm the above details are correct")

    submitted = st.form_submit_button("Predict Rate")


# -----------------------------
#       PREDICTION OUTPUT
# -----------------------------
if submitted:

    predictor = load_model()

    input_data = {
        "check_in_date": check_in_day,
        "room_type": room_type,
        "booking_channel": booking_channel,
        "city": city,
        "room_class": room_class,
        "property_id": property_id,
        "day_type": day_type,
        "number_of_guests": number_of_guest,
        "guest_rating_score": guest_rating_score,
        "hurdle_rate": hurdle_rate,
        "number_of_nights": number_of_night,
        "season": season,
        "category": category,
    }

    result = predictor.get_rate(input_data)

    st.success("Prediction Completed")

    st.subheader("📊 Recommended Pricing")

    colA, colB = st.columns(2)

    with colA:
        st.metric("Predicted Rate", f"INR {result['predicted_rate']}")

    with colB:
        st.metric(
            "Strategic Range",
            f"INR {result['range_min']} – INR {result['range_max']}",
        )

    st.caption(
        "This range reflects the model’s confidence interval based on historical MAE."
    )
