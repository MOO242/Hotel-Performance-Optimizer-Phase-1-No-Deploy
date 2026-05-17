import os
import numpy as np
import pandas as pd
import requests
import streamlit as st
from datetime import date

# ─── Try Plotly first, fall back to matplotlib ─────────────
try:
    import plotly.graph_objects as go

    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    import matplotlib.pyplot as plt

# ─── Config ──────────────────────────────────────────────────
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000") + "/predict_demand"
HISTORY_KEY = "demand_history"
CURVE_KEY = "demand_curve"

# ─── Page setup ──────────────────────────────────────────────
st.set_page_config(
    page_title="Room Demand Predictor",
    page_icon="🏨",
    layout="wide",
)

st.title("🏨 Room Demand Predictor")
st.caption("Forecast rooms sold per night and explore pricing scenarios")

if HISTORY_KEY not in st.session_state:
    st.session_state[HISTORY_KEY] = []
if CURVE_KEY not in st.session_state:
    st.session_state[CURVE_KEY] = None


# ─── Helper: Call API for one ADR value ──────────────────────
def predict_at_adr(adr_value, base_payload, rooms_available):
    """Call the demand API with a specific ADR; apply guardrails."""
    payload = base_payload.copy()
    payload["adr"] = float(adr_value)
    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        response.raise_for_status()
        raw = response.json()["prediction"]
        return max(0, min(raw, rooms_available))
    except Exception as e:
        st.error(f"API error at ADR={adr_value}: {e}")
        return None


# ─── Helper: Generate demand curve ──────────────────────────
def generate_demand_curve(base_payload, user_adr, rooms_available, num_points=9):
    """Predict across a range of ADR values to build the demand curve."""
    adr_range = np.linspace(user_adr * 0.6, user_adr * 1.4, num_points)
    results = []
    for a in adr_range:
        rooms = predict_at_adr(a, base_payload, rooms_available)
        if rooms is None:
            continue
        results.append(
            {
                "ADR": round(a, 0),
                "Rooms Sold": round(rooms, 1),
                "Projected Revenue": round(rooms * a, 0),
            }
        )
    return pd.DataFrame(results)


# ─── Input form ──────────────────────────────────────────────
with st.form("demand_form"):
    st.subheader("Booking & Property Details")

    col1, col2, col3 = st.columns(3)
    with col1:
        property_id = st.selectbox(
            "Property ID", ["16558", "16559", "17558", "17559", "18558", "19558"]
        )
        rooms_available = st.number_input(
            "Rooms Available", min_value=1, max_value=500, value=50
        )
    with col2:
        room_category = st.selectbox("Room Type", ["RT1", "RT2", "RT3", "RT4"])
        check_in_date = st.date_input(
            "Check-in Date", value=date.today(), min_value=date.today()
        )
    with col3:
        booking_channel = st.selectbox(
            "Booking Channel", ["Direct Online", "Direct Offline", "Journey", "Logtrip"]
        )
        adr = st.number_input(
            "Average Daily Rate (ADR)", min_value=1000.0, value=5000.0, step=500.0
        )

    col4, col5 = st.columns(2)
    with col4:
        city = st.selectbox("City", ["Mumbai", "Delhi", "Bangalore", "Hyderabad"])
    with col5:
        category = st.selectbox("Hotel Class", ["Economy", "Luxury"])

    submitted = st.form_submit_button("🔮 Predict Demand & Curve", width="stretch")


# ─── Prediction Logic ────────────────────────────────────────
if submitted:
    base_payload = {
        "rooms_available": int(rooms_available),
        "check_in_date": check_in_date.isoformat(),
        "property_id": str(property_id),
        "room_category": room_category,
        "booking_channel": booking_channel.lower(),
        "city": city,
        "category": category,
    }

    with st.spinner("Calculating demand curve (9 scenarios)..."):
        predicted_raw = predict_at_adr(adr, base_payload, rooms_available)

        if predicted_raw is None:
            st.error("❌ Could not reach prediction API.")
        else:
            predicted_rooms = int(round(predicted_raw, 0))
            occupancy_pct = round((predicted_rooms / rooms_available) * 100, 1)
            revenue = predicted_rooms * adr

            curve_df = generate_demand_curve(base_payload, adr, rooms_available)
            st.session_state[CURVE_KEY] = {
                "df": curve_df,
                "user_adr": adr,
                "user_rooms": predicted_rooms,
                "user_revenue": revenue,
            }

            st.success("✅ Prediction successful")
            res_col1, res_col2, res_col3 = st.columns(3)
            res_col1.metric("Predicted Rooms Sold", predicted_rooms)
            res_col2.metric("Occupancy Rate", f"{occupancy_pct}%")
            res_col3.metric("Projected Revenue", f"₹{revenue:,.0f}")

            st.session_state[HISTORY_KEY].insert(
                0,
                {
                    "Date": check_in_date.isoformat(),
                    "City": city,
                    "Room": room_category,
                    "ADR": adr,
                    "Sold": predicted_rooms,
                    "Occupancy %": occupancy_pct,
                    "Revenue": revenue,
                },
            )


# ─── History & Analytics ─────────────────────────────────────
if st.session_state[HISTORY_KEY]:
    st.divider()
    df = pd.DataFrame(st.session_state[HISTORY_KEY])

    tab1, tab2 = st.tabs(["📋 History Logs", "📊 Demand Curve Analysis"])

    with tab1:
        st.dataframe(df, width="stretch")
        if st.button("🗑️ Clear History"):
            st.session_state[HISTORY_KEY] = []
            st.session_state[CURVE_KEY] = None
            st.rerun()

    with tab2:
        if st.session_state[CURVE_KEY] is None:
            st.info("👈 Submit a prediction to see the demand curve.")
        else:
            curve_data = st.session_state[CURVE_KEY]
            curve_df = curve_data["df"]
            user_adr = curve_data["user_adr"]
            user_rooms = curve_data["user_rooms"]
            user_revenue = curve_data["user_revenue"]

            # ─── Status badge for chart library ───
            if PLOTLY_AVAILABLE:
                st.caption("📊 Chart engine: Plotly (interactive)")
            else:
                st.caption("📊 Chart engine: Matplotlib (Plotly not installed)")

            # Detect flat curve
            curve_is_flat = curve_df["Rooms Sold"].std() < 0.5

            if curve_is_flat:
                st.warning(
                    "⚠️ **Model insensitivity detected:** Predicted rooms don't change "
                    "with price. Demand model may not have been trained with ADR as "
                    "a feature."
                )

            # Find optimal pricing
            optimal_idx = curve_df["Projected Revenue"].idxmax()
            optimal_row = curve_df.loc[optimal_idx]

            # Insight cards
            col1, col2, col3 = st.columns(3)
            with col1:
                delta = optimal_row["ADR"] - user_adr
                st.metric(
                    "💡 Revenue-Optimal Price",
                    f"₹{optimal_row['ADR']:,.0f}",
                    delta=f"₹{delta:+,.0f} vs your price",
                )
            with col2:
                delta_rev = optimal_row["Projected Revenue"] - user_revenue
                st.metric(
                    "📈 Max Revenue Possible",
                    f"₹{optimal_row['Projected Revenue']:,.0f}",
                    delta=f"₹{delta_rev:+,.0f}",
                )
            with col3:
                st.metric(
                    "🛏️ Rooms at Optimal Price",
                    f"{optimal_row['Rooms Sold']:.0f}",
                )

            # ─── THE CHART (with fallback + error handling) ───
            try:
                if PLOTLY_AVAILABLE:
                    # ─── PLOTLY VERSION ───
                    fig = go.Figure()

                    fig.add_trace(
                        go.Scatter(
                            x=curve_df["ADR"],
                            y=curve_df["Rooms Sold"],
                            name="Rooms Sold",
                            yaxis="y1",
                            line=dict(color="#3498db", width=3),
                            marker=dict(size=10),
                            mode="lines+markers",
                        )
                    )

                    fig.add_trace(
                        go.Scatter(
                            x=curve_df["ADR"],
                            y=curve_df["Projected Revenue"],
                            name="Projected Revenue",
                            yaxis="y2",
                            line=dict(color="#2ecc71", width=3, dash="dot"),
                            marker=dict(size=10, symbol="diamond"),
                            mode="lines+markers",
                        )
                    )

                    fig.add_vline(
                        x=user_adr,
                        line_dash="dash",
                        line_color="#e74c3c",
                        annotation_text=f"Your: ₹{user_adr:,.0f}",
                    )

                    if abs(optimal_row["ADR"] - user_adr) > 100:
                        fig.add_vline(
                            x=optimal_row["ADR"],
                            line_dash="dot",
                            line_color="#f39c12",
                            annotation_text=f"Optimal: ₹{optimal_row['ADR']:,.0f}",
                        )

                    fig.update_layout(
                        title="📈 Price vs. Demand & Revenue Curve",
                        xaxis=dict(title="Average Daily Rate (₹)", tickformat=","),
                        yaxis=dict(
                            title=dict(text="Rooms Sold", font=dict(color="#3498db")),
                            tickfont=dict(color="#3498db"),
                            side="left",
                        ),
                        yaxis2=dict(
                            title=dict(text="Revenue (₹)", font=dict(color="#2ecc71")),
                            tickfont=dict(color="#2ecc71"),
                            overlaying="y",
                            side="right",
                            tickformat=",",
                        ),
                        hovermode="x unified",
                        height=500,
                        template="plotly_dark",
                    )

                    st.plotly_chart(fig, width="stretch")
                else:
                    # ─── MATPLOTLIB FALLBACK ───
                    fig, ax1 = plt.subplots(figsize=(12, 5))
                    fig.patch.set_facecolor("#0E1117")
                    ax1.set_facecolor("#0E1117")

                    color_blue = "#3498db"
                    color_green = "#2ecc71"
                    color_red = "#e74c3c"
                    color_orange = "#f39c12"

                    # Left axis: Rooms Sold (line+marker)
                    ax1.plot(
                        curve_df["ADR"],
                        curve_df["Rooms Sold"],
                        color=color_blue,
                        marker="o",
                        linewidth=3,
                        markersize=10,
                        label="Rooms Sold",
                    )
                    ax1.set_xlabel("Average Daily Rate (₹)", color="white", fontsize=12)
                    ax1.set_ylabel("Rooms Sold", color=color_blue, fontsize=12)
                    ax1.tick_params(axis="y", labelcolor=color_blue)
                    ax1.tick_params(axis="x", labelcolor="white")
                    ax1.grid(True, alpha=0.2)

                    # Right axis: Projected Revenue
                    ax2 = ax1.twinx()
                    ax2.plot(
                        curve_df["ADR"],
                        curve_df["Projected Revenue"],
                        color=color_green,
                        marker="D",
                        linestyle="--",
                        linewidth=3,
                        markersize=10,
                        label="Projected Revenue",
                    )
                    ax2.set_ylabel(
                        "Projected Revenue (₹)", color=color_green, fontsize=12
                    )
                    ax2.tick_params(axis="y", labelcolor=color_green)

                    # User price line
                    ax1.axvline(
                        x=user_adr,
                        color=color_red,
                        linestyle="--",
                        linewidth=2,
                        alpha=0.7,
                    )
                    ax1.text(
                        user_adr,
                        ax1.get_ylim()[1] * 0.95,
                        f"  Your: ₹{user_adr:,.0f}",
                        color=color_red,
                        fontsize=10,
                    )

                    # Optimal price line (if different)
                    if abs(optimal_row["ADR"] - user_adr) > 100:
                        ax1.axvline(
                            x=optimal_row["ADR"],
                            color=color_orange,
                            linestyle=":",
                            linewidth=2,
                            alpha=0.7,
                        )
                        ax1.text(
                            optimal_row["ADR"],
                            ax1.get_ylim()[1] * 0.85,
                            f"  Optimal: ₹{optimal_row['ADR']:,.0f}",
                            color=color_orange,
                            fontsize=10,
                        )

                    plt.title(
                        "📈 Price vs. Demand & Revenue Curve",
                        color="white",
                        fontsize=16,
                        pad=20,
                    )

                    # Combined legend
                    lines1, labels1 = ax1.get_legend_handles_labels()
                    lines2, labels2 = ax2.get_legend_handles_labels()
                    ax1.legend(
                        lines1 + lines2,
                        labels1 + labels2,
                        loc="upper center",
                        bbox_to_anchor=(0.5, -0.12),
                        ncol=2,
                        frameon=False,
                        labelcolor="white",
                    )

                    plt.tight_layout()
                    st.pyplot(fig)
                    plt.close(fig)

            except Exception as e:
                st.error(f"❌ Chart rendering failed: {type(e).__name__}: {e}")
                st.write("**Debug — Curve DataFrame:**")
                st.write(curve_df)

            # ─── Business insight box ─────────────────────────
            if not curve_is_flat:
                if optimal_row["ADR"] > user_adr:
                    st.warning(
                        f"💰 **Pricing Opportunity:** Raising your price to "
                        f"₹{optimal_row['ADR']:,.0f} could increase revenue by "
                        f"₹{optimal_row['Projected Revenue'] - user_revenue:,.0f}"
                    )
                elif optimal_row["ADR"] < user_adr:
                    st.info(
                        f"📊 **Demand Insight:** Lowering price to "
                        f"₹{optimal_row['ADR']:,.0f} would sell more rooms "
                        f"and lift revenue by "
                        f"₹{optimal_row['Projected Revenue'] - user_revenue:,.0f}"
                    )
                else:
                    st.success(
                        f"✅ **Optimal Pricing:** ₹{user_adr:,.0f} is at the "
                        f"revenue-maximizing point."
                    )

            # Scenarios table
            with st.expander("📋 Detailed Scenarios"):
                st.dataframe(
                    curve_df.style.format(
                        {
                            "ADR": "₹{:,.0f}",
                            "Rooms Sold": "{:.0f}",
                            "Projected Revenue": "₹{:,.0f}",
                        }
                    ),
                    width="stretch",
                )
