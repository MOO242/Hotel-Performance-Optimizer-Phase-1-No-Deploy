"""
whatiftool.py
─────────────
Streamlit page — Room Rate Predictor.
Calls FastAPI /predict_rate and shows:
  - Predicted rate + strategic range
  - History table of past predictions
  - Bar chart of rates over time
"""

import os
import requests
import pandas as pd
import streamlit as st

# ─── Config ──────────────────────────────────────────────────


API_URL = os.getenv("API_URL", "http://127.0.0.1:8000") + "/predict_rate"
HISTORY_KEY = "rate_history"
MAE = 500  # your model's mean absolute error in INR


# ─── Page setup ──────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Rate Predictor",
    page_icon="📈",
    layout="centered",
)

st.title("📈 Hotel Rate Predictor")
st.caption("AI-powered pricing recommendation for hotel revenue teams")

# initialise history on first run
if HISTORY_KEY not in st.session_state:
    st.session_state[HISTORY_KEY] = []


# ─── Input form ──────────────────────────────────────────────
with st.form("rate_form"):

    st.subheader("Booking Details")
    col1, col2 = st.columns(2)

    with col1:
        property_id = st.selectbox(
            "Property ID", ["19559", "17559", "18563", "19558", "18561"]
        )
        number_of_guests = st.number_input("Number of Guests", min_value=1, max_value=6)
        number_of_nights = st.number_input(
            "Number of Nights", min_value=1, max_value=30
        )
        guest_rating_score = st.slider("Guest Rating Score", 1.0, 5.0, step=0.1)

    with col2:
        city = st.selectbox("City", ["Bangalore", "Delhi", "Hyderabad", "Mumbai"])
        category = st.selectbox("Category", ["Economy", "Luxury"])
        season = st.selectbox(
            "Season", ["High Season", "Low Season", "Peak", "Shoulder"]
        )
        day_type = st.selectbox("Day Type", ["weekday", "weekend"])

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
        hurdle_rate = st.number_input("Hurdle Rate (INR)", min_value=0.0, step=100.0)

    submitted = st.form_submit_button("🔮 Predict Rate", width="stretch")


# ─── Prediction ──────────────────────────────────────────────
if submitted:

    payload = {
        "hurdle_rate": hurdle_rate,
        "number_of_guests": int(number_of_guests),
        "number_of_nights": int(number_of_nights),
        "guest_rating_score": float(guest_rating_score),
        "property_id": property_id,
        "city": city,
        "booking_channel": booking_channel,
        "day_type": day_type,
        "room_type": room_type,
        "season": season,
        "room_class": room_class,
        "category": category,
    }

    with st.spinner("Calling prediction API..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot reach API. Is uvicorn running?")
            st.stop()

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API error: {response.json().get('detail', str(e))}")
            st.stop()

    predicted = result["prediction"]
    range_min = round(predicted - MAE)
    range_max = round(predicted + MAE)

    # ── Result cards ─────────────────────────────────────────
    st.success("✅ Prediction complete")

    colA, colB, colC = st.columns(3)
    colA.metric("Predicted Rate", f"₹{predicted:,.0f}")
    colB.metric("Range Low", f"₹{range_min:,.0f}")
    colC.metric("Range High", f"₹{range_max:,.0f}")

    st.caption("Range = predicted rate ± model MAE (₹500)")

    # ── Save to history ──────────────────────────────────────
    st.session_state[HISTORY_KEY].insert(
        0,
        {
            "Property": property_id,
            "City": city,
            "Season": season,
            "Room Class": room_class,
            "Room Type": room_type,
            "Day Type": day_type,
            "Predicted Rate (₹)": round(predicted),
        },
    )


# ─── History + Chart ─────────────────────────────────────────
if st.session_state[HISTORY_KEY]:

    st.divider()
    st.subheader("📋 Prediction History")

    df = pd.DataFrame(st.session_state[HISTORY_KEY])
    st.dataframe(df, width="stretch")

    st.subheader("📊 Rate Trend")
    st.bar_chart(
        df.set_index(df.index.map(lambda i: f"#{len(df)-i}"))["Predicted Rate (₹)"]
    )

    if st.button("🗑️ Clear History"):
        st.session_state[HISTORY_KEY] = []
        st.rerun()
