"""
demand.py
─────────
Streamlit page — Room Demand Predictor.
Calls FastAPI /predict_demand and shows:
  - Predicted rooms sold
  - Occupancy rate (rooms sold / rooms available)
  - History table of past predictions
  - Bar + line charts from matplotlib
"""

import os

import matplotlib.pyplot as plt
import pandas as pd
import requests
import streamlit as st

# ─── Config ──────────────────────────────────────────────────
API_URL     = os.getenv("API_URL", "http://127.0.0.1:8000") + "/predict_demand"
HISTORY_KEY = "demand_history"


# ─── Page setup ──────────────────────────────────────────────
st.set_page_config(
    page_title="Room Demand Predictor",
    page_icon="🏨",
    layout="centered",
)

st.title("🏨 Room Demand Predictor")
st.caption("Forecast rooms sold per night by property and room type")

# initialise history on first run
if HISTORY_KEY not in st.session_state:
    st.session_state[HISTORY_KEY] = []


# ─── Input form ──────────────────────────────────────────────
with st.form("demand_form"):

    st.subheader("Property Details")
    col1, col2 = st.columns(2)

    with col1:
        property_id = st.selectbox(
            "Property ID", ["19559", "17559", "18563", "19558", "18561"]
        )
        rooms_available = st.number_input(
            "Rooms Available", min_value=0, max_value=500, step=1
        )

    with col2:
        room_category = st.selectbox(
            "Room Category", ["RT1", "RT2", "RT3", "RT4"]
        )

    submitted = st.form_submit_button("🔮 Predict Demand", width="stretch")


# ─── Prediction ──────────────────────────────────────────────
if submitted:

    payload = {
        "property_id":    property_id,
        "rooms_available": int(rooms_available),
        "room_category":  room_category,
    }

    with st.spinner("Calling prediction API..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot reach API. Is the server running?")
            st.stop()

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ API error: {response.json().get('detail', str(e))}")
            st.stop()

    # ── Process result ────────────────────────────────────────
    predicted_rooms = result["prediction"]

    # clamp — can't sell more rooms than available
    predicted_rooms = min(predicted_rooms, rooms_available)

    # derived metric — calculated locally, no extra API call
    occupancy_pct = (
        round((predicted_rooms / rooms_available) * 100, 1)
        if rooms_available > 0
        else 0.0
    )

    # ── Result cards ─────────────────────────────────────────
    st.success("✅ Prediction complete")

    colA, colB = st.columns(2)
    colA.metric("Predicted Rooms Sold", f"{predicted_rooms:.2f}")
    colB.metric("Occupancy Rate",       f"{occupancy_pct}%")

    # ── Save to history ──────────────────────────────────────
    st.session_state[HISTORY_KEY].insert(0, {
        "Property":        property_id,
        "Room Category":   room_category,
        "Rooms Available": int(rooms_available),
        "Rooms Sold":      round(predicted_rooms, 2),
        "Occupancy (%)":   occupancy_pct,
    })


# ─── History + Charts ────────────────────────────────────────
if st.session_state[HISTORY_KEY]:

    st.divider()
    st.subheader("📋 Prediction History")

    df = pd.DataFrame(st.session_state[HISTORY_KEY])
    st.dataframe(df, width="stretch")

    # ── Matplotlib charts ─────────────────────────────────────
    st.subheader("📊 Demand Analytics")

    labels = [f"#{len(df)-i}" for i in df.index]

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))

    # Chart 1 — bar: rooms sold per prediction
    axes[0].bar(labels, df["Rooms Sold"], color="#4C9BE8")
    axes[0].set_title("Rooms Sold per Prediction")
    axes[0].set_xlabel("Prediction #")
    axes[0].set_ylabel("Rooms Sold")
    axes[0].tick_params(axis="x", rotation=45)

    # Chart 2 — line: occupancy trend
    axes[1].plot(
        labels,
        df["Occupancy (%)"],
        marker="o",
        color="#E87B4C",
        linewidth=2,
        markersize=6,
    )
    axes[1].set_title("Occupancy Rate Trend")
    axes[1].set_xlabel("Prediction #")
    axes[1].set_ylabel("Occupancy %")
    axes[1].set_ylim(0, 100)
    axes[1].tick_params(axis="x", rotation=45)

    # add a reference line at 80% — healthy occupancy threshold
    axes[1].axhline(y=80, color="green", linestyle="--", linewidth=1, label="80% target")
    axes[1].legend()

    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)          # free memory

    if st.button("🗑️ Clear History"):
        st.session_state[HISTORY_KEY] = []
        st.rerun()