import os
import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Try Plotly first; fall back to matplotlib if unavailable
try:
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False

# ─── Config ──────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000") + "/predict_rate"
HISTORY_KEY = "rate_history"

# Model metrics (from test set evaluation)
MAE = 1780  # ← Updated to match your Rate Forecaster test MAE
MODEL_VERSION = "RF-v1.0"
MODEL_R2 = 0.80

# ─── Page setup ──────────────────────────────────────────────
st.set_page_config(
    page_title="Hotel Rate Predictor",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Hotel Rate Predictor")
st.caption(
    f"AI-powered pricing recommendation for revenue teams "
    f"| Model: {MODEL_VERSION} | R²: {MODEL_R2} | MAE: ±₹{MAE:,}"
)

if HISTORY_KEY not in st.session_state:
    st.session_state[HISTORY_KEY] = []


# ─── Helper: Call rate API ───────────────────────────────────
def predict_rate(payload):
    """Call the rate API and return the prediction (or None on failure)."""
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()["prediction"]
    except Exception as e:
        st.error(f"❌ API Error: {str(e)}")
        return None


# ─── Input form ──────────────────────────────────────────────

ROOM_MAPPING = {
    "Standard": {"type": "RT1", "label": "Deluxe", "hurdle": 1500.0},
    "Elite": {"type": "RT2", "label": "Elite", "hurdle": 2500.0},
    "Premium": {"type": "RT3", "label": "Premium", "hurdle": 4000.0},
    "Presidential": {"type": "RT4", "label": "Suite", "hurdle": 7500.0},
}
with st.form("rate_form"):
    st.subheader("Booking Details")
    col1, col2, col3 = st.columns(3)

    with col1:
        property_id = st.selectbox(
            "Property ID", ["16558", "16559", "17558", "17559", "18558", "19558"]
        )
        city = st.selectbox("City", ["Mumbai", "Delhi", "Bangalore", "Hyderabad"])
        category = st.selectbox("Hotel Category", ["Economy", "Luxury"])

    with col2:
        number_of_guests = st.number_input("Guests", min_value=1, max_value=6, value=2)
        number_of_nights = st.number_input("Nights", min_value=1, max_value=30, value=1)
        guest_rating_score = st.slider(
            "Guest Rating Score", 1.0, 5.0, value=3.5, step=0.1
        )

    with col3:
        season = st.selectbox(
            "Season", ["Low Season", "Shoulder", "High Season", "Peak"]
        )
        day_type = st.selectbox("Day Type", ["weekday", "weekend"])

    st.subheader("Room Rate Hurdle & Channel Configuration")
    col4, col5 = st.columns(2)

    with col4:
        room_class = st.selectbox(
            "Room Class",
            list(ROOM_MAPPING.keys()),
            key="room_class_select",
        )

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

    with col5:
        # 1. Put Room Type here first to match the line with Room Class
        linked_data = ROOM_MAPPING[room_class]
        type_options = ["RT1", "RT2", "RT3", "RT4"]
        target_index = type_options.index(linked_data["type"])
        room_type = st.selectbox(
            f"Room Type ({linked_data['label']})", type_options, index=target_index
        )

    hurdle_rate = st.number_input(
        "Hurdle Rate (Min Price ₹)",
        min_value=1000.0,
        value=linked_data["hurdle"],
        step=100.0,
        help=f"Minimum floor for {room_class} ({linked_data['label']}).",
    )

    # Outside columns
    submitted = st.form_submit_button(
        "🔮 Predict Recommended Rate", use_container_width=True
    )


# ─── Prediction Logic ────────────────────────────────────────
if submitted:
    payload = {
        "hurdle_rate": float(hurdle_rate),
        "number_of_guests": int(number_of_guests),
        "number_of_nights": int(number_of_nights),
        "guest_rating_score": float(guest_rating_score),
        "property_id": str(property_id),
        "city": city,
        "booking_channel": booking_channel,
        "day_type": day_type,
        "room_type": room_type,
        "season": season,
        "room_class": room_class,
        "category": category,
    }

    with st.spinner("Analyzing market dynamics..."):
        predicted = predict_rate(payload)

        if predicted is not None:
            # Guardrail: never recommend below hurdle rate
            raw_prediction = predicted
            final_rate = max(predicted, hurdle_rate)

            # Confidence band based on real model MAE
            range_min = round(final_rate - MAE)
            range_max = round(final_rate + MAE)

            # ── Result cards ─────────────────────────────────
            st.success("✅ Rate Strategy Generated")
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Recommended Rate", f"₹{final_rate:,.0f}")
            res_col2.metric("Floor (−MAE)", f"₹{range_min:,.0f}")
            res_col3.metric("Ceiling (+MAE)", f"₹{range_max:,.0f}")

            # ── Hurdle guardrail disclosure ──────────────────
            if raw_prediction < hurdle_rate:
                st.warning(
                    f"⚠️ **Hurdle guardrail fired:** Model suggested "
                    f"₹{raw_prediction:,.0f}, below your hurdle rate. "
                    f"Recommendation raised to floor (₹{hurdle_rate:,.0f})."
                )

            st.info(
                f"💡 **Strategy:** Recommended rate **₹{final_rate:,.0f}** "
                f"for **{category}** {room_class} ({room_type}) in **{city}** "
                f"during **{season}** ({day_type}). "
                f"Confidence band reflects model's test-set MAE of ±₹{MAE:,}."
            )

            # ── Save to history ──────────────────────────────
            st.session_state[HISTORY_KEY].insert(
                0,
                {
                    "Property": property_id,
                    "City": city,
                    "Room": f"{room_class} ({room_type})",
                    "Season": season,
                    "Day": day_type,
                    "Recommended (₹)": round(final_rate),
                    "Floor (₹)": range_min,
                    "Ceiling (₹)": range_max,
                    "Hurdle (₹)": hurdle_rate,
                },
            )


# ─── History & Charts ────────────────────────────────────────
if st.session_state[HISTORY_KEY]:
    st.divider()
    df = pd.DataFrame(st.session_state[HISTORY_KEY])

    tab1, tab2 = st.tabs(["📋 Pricing History", "📊 Rate Strategy Trend"])

    # ──────────────────────────────────────────────────────────
    with tab1:
        st.dataframe(df, width="stretch")
        if st.button("🗑️ Reset History"):
            st.session_state[HISTORY_KEY] = []
            st.rerun()

    # ──────────────────────────────────────────────────────────
    with tab2:
        # Reverse for chronological order
        chart_df = df.iloc[::-1].reset_index(drop=True)
        chart_df["Sequence"] = chart_df.index + 1

        if PLOTLY_AVAILABLE:
            # ─── Plotly version ───
            fig = go.Figure()

            # Confidence band (filled area between floor and ceiling)
            fig.add_trace(
                go.Scatter(
                    x=chart_df["Sequence"],
                    y=chart_df["Ceiling (₹)"],
                    name="Ceiling",
                    line=dict(color="rgba(232, 123, 76, 0)"),
                    showlegend=False,
                    hoverinfo="skip",
                )
            )
            fig.add_trace(
                go.Scatter(
                    x=chart_df["Sequence"],
                    y=chart_df["Floor (₹)"],
                    name="Confidence Band (±MAE)",
                    fill="tonexty",
                    fillcolor="rgba(232, 123, 76, 0.2)",
                    line=dict(color="rgba(232, 123, 76, 0)"),
                    hovertemplate="<b>Floor:</b> ₹%{y:,.0f}<extra></extra>",
                )
            )

            # Recommended rate line
            fig.add_trace(
                go.Scatter(
                    x=chart_df["Sequence"],
                    y=chart_df["Recommended (₹)"],
                    name="Recommended Rate",
                    line=dict(color="#E87B4C", width=3),
                    marker=dict(size=10),
                    mode="lines+markers",
                    hovertemplate=(
                        "<b>Sequence:</b> %{x}<br>"
                        "<b>Rate:</b> ₹%{y:,.0f}<extra></extra>"
                    ),
                )
            )

            # Hurdle rate step
            fig.add_trace(
                go.Scatter(
                    x=chart_df["Sequence"],
                    y=chart_df["Hurdle (₹)"],
                    name="Hurdle Rate (Floor)",
                    line=dict(color="#e74c3c", width=2, dash="dash"),
                    line_shape="hv",
                    hovertemplate="<b>Hurdle:</b> ₹%{y:,.0f}<extra></extra>",
                )
            )

            fig.update_layout(
                title=dict(
                    text="📈 Rate Strategy Over Time",
                    font=dict(size=20),
                ),
                xaxis_title="Prediction Sequence",
                yaxis=dict(title="Rate (INR)", tickformat=","),
                hovermode="x unified",
                template="plotly_dark",
                height=500,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1,
                ),
            )

            st.plotly_chart(fig, width="stretch")

        else:
            # ─── Matplotlib fallback ───
            fig, ax = plt.subplots(figsize=(12, 5))
            fig.patch.set_facecolor("#0e1117")
            ax.set_facecolor("#0e1117")

            ax.plot(
                chart_df["Sequence"],
                chart_df["Recommended (₹)"],
                marker="o",
                color="#E87B4C",
                linewidth=3,
                markersize=10,
                label="Recommended Rate",
            )
            ax.fill_between(
                chart_df["Sequence"],
                chart_df["Floor (₹)"],
                chart_df["Ceiling (₹)"],
                color="#E87B4C",
                alpha=0.2,
                label=f"Confidence Band (±₹{MAE:,})",
            )
            ax.step(
                chart_df["Sequence"],
                chart_df["Hurdle (₹)"],
                where="post",
                color="#e74c3c",
                linestyle="--",
                linewidth=2,
                alpha=0.8,
                label="Hurdle Rate (Floor)",
            )

            ax.set_xlabel("Prediction Sequence", color="white", fontsize=12)
            ax.set_ylabel("Rate (INR)", color="white", fontsize=12)
            ax.tick_params(axis="x", colors="white")
            ax.tick_params(axis="y", colors="white")
            ax.grid(True, alpha=0.2)

            for spine in ax.spines.values():
                spine.set_color("white")

            plt.title(
                "📈 Rate Strategy Over Time",
                color="white",
                fontsize=16,
                pad=15,
            )
            ax.legend(
                loc="upper center",
                bbox_to_anchor=(0.5, -0.15),
                ncol=3,
                facecolor="#0e1117",
                edgecolor="white",
                labelcolor="white",
            )
            fig.tight_layout()
            st.pyplot(fig)
            plt.close(fig)
