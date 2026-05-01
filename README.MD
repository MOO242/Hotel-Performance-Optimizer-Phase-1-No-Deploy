# 🏨 Hotel Performance Optimizer  

A production‑grade analytics and decision‑intelligence system for hotel revenue management, built on a modern analytics maturity framework that progresses from **descriptive KPIs → diagnostic analysis → predictive forecasting → prescriptive decision support**.

---

## 📐 Architecture Overview

<<<<<<< HEAD
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

* ADR vs Occupancy decomposition
* Revenue = ADR × Rooms Sold
* RevPAR = ADR × Occupancy

> **Rule:** Every RevPAR movement must be explained through **ADR vs Occupancy**.

***

### 📅 Layer 3 — Demand & Booking Health KPIs

* Gross & Net Bookings
* Cancellation Rate, No‑Show Rate
* Booking Lead Time, Length of Stay (LOS)
* Pickup (Daily / Weekly)
* Booking Pace vs Last Year & Budget

***

### 🏷️ Layer 4 — Segment Performance KPIs

For each segment (Transient, Group, Contract, Wholesale):

* Room Revenue, Rooms Sold, ADR, RevPAR, Occupancy %
* Segment Mix %, Revenue Contribution %
* ADR Premium / Discount vs Total

***

### 📡 Layer 5 — Channel & Source KPIs

* Channel Mix % (Direct, OTA, GDS, Voice)
* ADR by Channel, Net ADR
* OTA Dependency %, Cost of Sale %

***

### 📈 Layer 6 — Time‑Based Comparison KPIs

* YoY, WoW, MoM % change
* YTD performance
* Rolling 7 / 14 / 30‑day trends
* Seasonality Index

***

### 🏨 Layer 7 — Distribution & Inventory Health

* Availability %
* Out‑of‑Order Rooms
* Sell‑Out Days
* Compression Nights
* Wash % *(Cancellations + No‑Shows)*

***

### 🔮 Layer 8 — Forecast & Forward‑Looking KPIs

* On‑The‑Books (OTB) Revenue & ADR
* Forecast Occupancy & RevPAR
* Pickup Forecast
* Forecast Accuracy (MAPE, Error %)
* Budget Variance

***

### 🎯 Layer 9 — Commercial Strategy KPIs *(Advanced)*

* ADR Opportunity Index
* Price Elasticity
* Displacement Analysis (Group)
* BAR vs Achieved ADR
* Repeat Guest %, Loyalty Revenue %

***

### 🛡️ Layer 10 — Data Quality & Governance KPIs

* Data Completeness %
* Missing ADR / Revenue counts
* Outlier detection flags
* KPI reconciliation checks

***

***

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/hotel-performance-optimizer.git
cd hotel-performance-optimizer
=======
```
SQL Databases (PostgreSQL / Snowflake / SQL Server)
        ↓
Secure SQL Layer (Views, Data Contracts, Governance)
        ↓
Data Model (Fact & Dimension Tables)
        ↓
Feature Store & Data Validation
        ↓
Is Data Valid?
   ├── No → Reject / Fix Before Ingestion
   └── Yes → EDA & Descriptive Analysis (Python + SQL)
        ↓
Diagnostic Analytics
   ├── KPI Engine (Python + SQL‑certified metrics)
   ├── Root Cause Analysis
   └── Booking Health & Demand Signals
        ↓
Predictive Forecasting
   ├── ADR Forecast
   ├── Occupancy Forecast
   ├── RevPAR Derived Forecast
   ├── Time‑Series Backtesting
   └── Model Evaluation & MLflow Tracking
        ↓
Prescriptive Decision Engine
   ├── What‑If Analysis
   ├── Price Recommendations
   ├── Revenue Strategy Logic
   └── FastAPI Model Serving
        ↓
BI & Apps
   ├── Power BI / Tableau
   └── Streamlit App (Dashboards, Forecast View, Backtests, What‑If)
>>>>>>> b0e8f845cf57eaa7977d28398f3b93cd9be965e7
```

**Orchestration & MLOps Layer**
- Airflow DAGs: ingestion → feature engineering → training → validation → model registry  
- MLflow: experiment tracking, model registry, metrics store  
- Artifacts: model.pkl, scalers, encoders, backtest results  

---

## 🗂️ Project Structure 

```
hotel_performance_optimizer/
│
├── airflow/                         # DAGs for ingestion, training, scoring
│
├── artifacts/                       # Saved models, scalers, backtests
│
├── mlops/                           # MLflow configs, model registry logic
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── feature_store.py
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
├── Roadmap.drawio
├── Roadmap.jpg                      # Updated architecture diagram
├── Diagnostic_Analytics.md
├── Predictive_Analytics.md
├── Prescriptive_Analytics.md
├── .env
├── .gitignore
├── exception.py
├── logger.py
├── requirements.txt
└── README.md
```

---

## 📊 KPI Framework 

- **Layer 1–2:** Outcome KPIs + Drivers  
- **Layer 3–7:** Demand, Segments, Channels, Inventory  
- **Layer 8:** Forecast KPIs  
- **Layer 9:** Commercial Strategy KPIs  
- **Layer 10:** Data Quality KPIs  

**KPI Engine → Diagnostic Layer → Forecast Layer → Prescriptive Layer**

---

## 🛠️ Tech Stack 

| Layer                    | Technology                                  |
| ------------------------ | ------------------------------------------- |
| Database                 | PostgreSQL / Snowflake / SQL Server         |
| Data Modeling            | SQL Views, Fact/Dim Tables                  |
| Data Validation          | Python, Pandas,                             |
| Feature Store            | Python, SQL                                 |
| Machine Learning         | Scikit‑learn, MLflow                        |
| Orchestration            | Apache Airflow                              |
| KPI Engine               | Python + SQL                                |
| API Layer                | FastAPI                                     |
| App Layer                | Streamlit                                   |
| Visualization            | Power BI, Tableau                           |
| Logging                  | Python logging                              |
| Testing                  | Pytest                                      |

---

## 📌 Roadmap 

- [x] Architecture design (SQL → Validation → KPI → Forecast → Prescriptive)
- [x] Data ingestion layer  
- [x] Data validation & feature store  
- [x] KPI engine structure  
- [x] Diagnostic analytics  
- [ ] ADR forecasting model  
- [ ] Occupancy forecasting model  
- [ ] RevPAR derived forecast  
- [ ] Backtesting engine  
- [ ] MLflow integration  
- [ ] Airflow DAGs (full pipeline)  
- [ ] Streamlit dashboards (Revenue, Forecast, Backtest, What‑If)  
- [ ] FastAPI deployment  
- [ ] Power BI / Tableau dashboards  

---

## 🖼️  Roadmap Diagram  

![Hotel Performance Optimizer Architecture](https://raw.githubusercontent.com/MOO242/Hotel-Performance-Optimizer/main/Project_Architecture.jpg)

<<<<<<< HEAD
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
=======
>>>>>>> b0e8f845cf57eaa7977d28398f3b93cd9be965e7
