import streamlit as st

st.set_page_config(
    page_title="Hotel Performance Optimizer", page_icon="🏢", layout="wide"
)

# ─── 1. Header & Branding ──────────────────────────────────
st.title("🚀 Hotel Revenue What-If Tool")
st.caption("v1.0 | Real-time AI Forecasting Engine")

# ─── 2. Socials & Developer Info ───────────────────────────
st.markdown(
    f"""
Developed by: **Mohamed Al Razek** [![GitHub](https://img.shields.io/badge/GitHub-100000?style=flat&logo=github&logoColor=white)](https://github.com/MOO242) 
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/mohamed-al-razek-950a00104/)
""",
    unsafe_allow_html=True,
)

st.divider()

# ─── 3. KPIs / System Health ───────────────────────────────
c1, c2, c3, c4 = st.columns(4)
c1.metric("System Status", "ONLINE", delta="Healthy")
c2.metric("Active Model", "RandomForest v1.0")
c3.metric("Training Samples", "134,000")
c4.metric("Last Retrain", "2026-05-15")

# ─── 4. Navigation Cards ───────────────────────────────────
st.write("### 🕹️ Action Center")
col_nav1, col_nav2 = st.columns(2)

with col_nav1:
    st.markdown("""
    #### 📊 Demand Predictor
    Predict total rooms sold based on pricing and property type.
    """)
    if st.button("Open Demand Module", use_container_width=True):
        st.switch_page("pages/Demand.py")

with col_nav2:
    st.markdown("""
    #### 📈 Rate Optimizer
    Find the recommended price point for your rooms.
    """)
    if st.button("Open Rate Module", use_container_width=True):
        st.switch_page("pages/Rate.py")

# ─── 5. Technical Documentation ────────────────────────────
st.divider()

with st.expander("🛠️ Technical Architecture & System Design"):
    col_text, col_img = st.columns([1, 1])

    with col_text:
        st.write("### The Tech Stack")
        st.write("""
        - **Backend:** FastAPI for high-performance, asynchronous ML inference.
        - **Pipeline:** dbt (data build tool) for robust feature engineering and modular SQL within PostgreSQL.
        - **Orchestration:** Dockerized environment ensuring consistent deployment across Dev/Prod.
        - **Modeling:** Scikit-Learn pipelines utilizing Random Forest Regressors with complex OneHot and Ordinal encoding.
        - **Visuals:** Matplotlib and Streamlit Native Charts for real-time business intelligence.
        """)

    with col_img:
        st.write("### Pipeline Flow")
        # Ensure image_277c05.png is in your root directory or provide the full path
        st.image(
            "Project_architecture.png",
            caption="End-to-End Hotel Performance Optimizer Architecture",
            use_container_width=True,
        )
        st.info(
            "System includes ELT (dbt), Feature Store, MLFlow tracking, and Streamlit/FastAPI serving."
        )

st.divider()
st.caption(
    "Built with Python, Scikit-Learn, and Streamlit. © 2026 Hotel Performance Optimizer."
)
