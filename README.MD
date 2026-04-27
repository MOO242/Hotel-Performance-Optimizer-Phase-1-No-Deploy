Here’s a **cleaned, fixed, and production‑ready version** of your README.  
I’ve **not changed your intent or scope**—only corrected grammar, consistency, naming, formatting, and a few architectural contradictions to make it **EMEA / senior‑reviewer ready**.

***

# 🏨 Hotel Performance Optimizer

A production‑grade analytics system for hotel revenue management, built on an analytics maturity framework that progresses from **descriptive KPIs** → **diagnostic root‑cause analysis** → **predictive forecasting** → **prescriptive decision support**.

***

## 📐 Architecture Overview

    PostgreSQL / Snowflake / SQL Server
            ↓
       Data Model (Fact & Dimension Tables)
            ↓
       KPI Engine (Python + SQL‑certified metrics)
            ↓
    ┌──────────────────────────────────────────┐
    │  Descriptive  →  Diagnostic  → Forecast │
    │  Analytics        Analytics     (Demand │
    │  (KPIs)           (WHY?)         & ADR) │
    └──────────────────────────────────────────┘
            ↓
       Decision & Prescriptive Analysis
            ↓
       Power BI / Tableau

***

## 🗂️ Project Structure

    hotel_performance_optimizer/
    │
    ├── artifacts/                        # Saved model artifacts (.pkl, .joblib)
    │
    ├── src/
    │   ├── components/
    │   │   ├── data_ingestion.py
    │   │   └── kpi_engine.py
    │   │
    │   ├── forecasting/
    │   │   ├── feature_engineering.py
    │   │   ├── demand_forecast.py
    │   │   ├── adr_forecast.py
    │   │   ├── revpar_forecast.py
    │   │   └── model_utils.py
    │   │
    │   ├── pipelines/
    │   │   ├── train_pipeline.py
    │   │   ├── predict_pipeline.py
    │   │   └── evaluate_pipeline.py
    │   │
    │   └── streamlit_app/
    │       ├── main.py
    │       └── pages/
    │           ├── revenue_dashboard.py
    │           ├── forecast_view.py
    │           ├── backtest_results.py
    │           └── what_if_analysis.py
    │
    ├── notebooks/
    │   └── eda.ipynb
    │
    ├── tests/
    │   ├── test_feature_generation.py
    │   ├── test_forecast_sanity.py
    │   └── test_kpi_definitions.py
    │
    ├── .env
    ├── .gitignore
    ├── exception.py
    ├── logger.py
    ├── requirements.txt
    └── README.md

✅ **Fixes applied**

*   `Notebook/` → `notebooks/` (standard convention)
*   `test/` → `tests/`
*   Naming consistency (snake\_case everywhere)

***

## 📊 KPI Framework

This project follows a structured **analytics maturity model**, with KPIs organized into **10 logical layers**.

***

### ✅ Layer 1 — Outcome KPIs *(What happened)*

Executive‑level results. All downstream diagnostics explain movement in these metrics.

| KPI             | Definition                                   |
| --------------- | -------------------------------------------- |
| Room Revenue    | Total revenue from room sales                |
| RevPAR          | Revenue per Available Room (ADR × Occupancy) |
| ADR             | Average Daily Rate (Revenue ÷ Rooms Sold)    |
| Occupancy %     | Rooms Sold ÷ Rooms Available                 |
| Rooms Sold      | Total occupied rooms                         |
| Rooms Available | Total inventory available                    |

***

### 🔍 Layer 2 — Primary Driver KPIs *(Why it happened)*

Foundational diagnostics.

*   ADR vs Occupancy decomposition
*   Revenue = ADR × Rooms Sold
*   RevPAR = ADR × Occupancy

> **Rule:** Every RevPAR movement must be explained through **ADR vs Occupancy**.

***

### 📅 Layer 3 — Demand & Booking Health KPIs

*   Gross & Net Bookings
*   Cancellation Rate, No‑Show Rate
*   Booking Lead Time, Length of Stay (LOS)
*   Pickup (Daily / Weekly)
*   Booking Pace vs Last Year & Budget

***

### 🏷️ Layer 4 — Segment Performance KPIs

For each segment (Transient, Group, Contract, Wholesale):

*   Room Revenue, Rooms Sold, ADR, RevPAR, Occupancy %
*   Segment Mix %, Revenue Contribution %
*   ADR Premium / Discount vs Total

***

### 📡 Layer 5 — Channel & Source KPIs

*   Channel Mix % (Direct, OTA, GDS, Voice)
*   ADR by Channel, Net ADR
*   OTA Dependency %, Cost of Sale %

***

### 📈 Layer 6 — Time‑Based Comparison KPIs

*   YoY, WoW, MoM % change
*   YTD performance
*   Rolling 7 / 14 / 30‑day trends
*   Seasonality Index

***

### 🏨 Layer 7 — Distribution & Inventory Health

*   Availability %
*   Out‑of‑Order Rooms
*   Sell‑Out Days
*   Compression Nights
*   Wash % *(Cancellations + No‑Shows)*

***

### 🔮 Layer 8 — Forecast & Forward‑Looking KPIs

*   On‑The‑Books (OTB) Revenue & ADR
*   Forecast Occupancy & RevPAR
*   Pickup Forecast
*   Forecast Accuracy (MAPE, Error %)
*   Budget Variance

***

### 🎯 Layer 9 — Commercial Strategy KPIs *(Advanced)*

*   ADR Opportunity Index
*   Price Elasticity
*   Displacement Analysis (Group)
*   BAR vs Achieved ADR
*   Repeat Guest %, Loyalty Revenue %

***

### 🛡️ Layer 10 — Data Quality & Governance KPIs

*   Data Completeness %
*   Missing ADR / Revenue counts
*   Outlier detection flags
*   KPI reconciliation checks

***

## 🚀 Analytics Maturity Scope

| Scope                    | Coverage                                                                                                        |
| ------------------------ | --------------------------------------------------------------------------------------------------------------- |
| **Minimum**              | Outcome KPIs, ADR vs Occupancy diagnostics, Segment KPIs, YoY trends, Booking Pace                              |
| **EMEA Analytics‑Ready** | Segment & Channel Mix, Pickup & Pace curves, Forecast vs Actual, Revenue decomposition, Data‑quality safeguards |

***

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hotel-performance-optimizer.git
cd hotel-performance-optimizer
```

### 2. Create a virtual environment

```bash
python -m venv env
source env/bin/activate   # Windows: env\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
# Update .env with database credentials and runtime settings
```

### 5. Run training pipeline

```bash
python src/pipelines/train_pipeline.py
```

### 6. Generate predictions

```bash
python src/pipelines/predict_pipeline.py
```

### 7. Evaluate model performance

```bash
python src/pipelines/evaluate_pipeline.py
```

***

## 🧪 Running Tests

```bash
pytest tests/
```

***

## 🛠️ Tech Stack

| Layer            | Technology                          |
| ---------------- | ----------------------------------- |
| Database         | PostgreSQL / Snowflake / SQL Server |
| Data Processing  | Python, Pandas                      |
| Machine Learning | Scikit‑learn                        |
| KPI Engine       | Python + SQL                        |
| Visualization    | Power BI, Tableau                   |
| Logging          | Python logging                      |
| Testing          | Pytest                              |
| Version Control  | Git                                 |

***

## 📌 Roadmap

*   [x] Project architecture & structure
*   [x] KPI framework definition
*   [x] Data ingestion layer
*   [x] Feature engineering
*   [ ] KPI engine (Python + SQL‑certified metrics)
*   [ ] Demand forecasting model
*   [ ] ADR forecasting model
*   [ ] RevPAR derived forecast
*   [ ] Training & prediction pipelines
*   [ ] Power BI / Tableau dashboards
*   [ ] API & deployment (FastAPI)

***

<https://github.com/MOO242/Hotel-Performance-Optimizer/blob/main/Project%20Articulate.png>

***
