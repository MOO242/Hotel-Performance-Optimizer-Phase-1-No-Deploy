# 🏨 Hotel Performance Optimizer  
A production‑grade analytics and decision‑intelligence system for hotel revenue management, built on a modern data & ML architecture that progresses from **data ingestion → validation → semantic modeling → diagnostic analytics → forecasting → prescriptive decision support**.

---

## 📐 Architecture Overview (Updated to match the diagram)

```
Extract, Load, Transform (ELT)
   ├── API / Web Scraping / CSV
   └── SQL Databases (PostgreSQL / Snowflake / SQL Server)
        ↓
Feature Store & Data Validation
   ├── Schema checks
   ├── Missing/outlier detection
   └── Valid? 
        ├── No → Reject / Fix before ingestion
        └── Yes → Continue
        ↓
Semantic Layer (dbt)
   ├── KPI definitions
   ├── Metric logic
   └── Data modeling (Fact & Dim tables)
        ↓
Data Model
   ├── EDA & Descriptive Analysis (Python + SQL)
   ├── KPI Engine (Python package)
   └── Root Cause Analysis
        ↓
Forecasting (Demand & Price)
   ├── ADR Forecast
   ├── Occupancy Forecast
   ├── Derived RevPAR
   ├── Time‑Series Backtesting
   └── Model Evaluation (MAPE, RMSE)
        ↓
What‑If Analysis & Business Logic
   ├── Price recommendations
   ├── Revenue decision rules
   ├── Model serving (FastAPI)
   └── Streamlit interactive apps
        ↓
Decision & Prescriptive Analytics
   ├── Prescriptive Action Engine
   └── BI Dashboards (Power BI / Tableau)
        ↓
Orchestration & MLOps
   ├── Airflow DAGs (ingestion → features → training → scoring)
   ├── MLflow Tracking & Model Registry
   └── Artifact store (models, scalers, backtests)
```

---

## 🗂️ Project Structure (Aligned with the architecture)

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
├── Roadmap.jpg
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

## 📊 KPI Framework (kept as‑is — already excellent)

Your 10‑layer KPI framework is already world‑class and aligns perfectly with the architecture.

---

## 🛠️ Tech Stack (Updated to match the diagram)

| Layer                    | Technology                                  |
| ------------------------ | ------------------------------------------- |
| ELT & Data Ingestion     | Python, API clients, Web Scraping           |
| Database                 | PostgreSQL / Snowflake / SQL Server         |
| Data Modeling            | dbt (Semantic Layer)                        |
| Data Validation          | Python, Pandas                              |
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

## 📌 Roadmap (Updated to match architecture)

- [x] Architecture design (ELT → Validation → dbt → KPI → Forecast → Prescriptive)
- [x] Data ingestion layer  
- [x] Data validation & feature store  
- [x] Semantic layer (dbt)  
- [x] KPI engine  
- [x] Diagnostic analytics  
- [ ] ADR forecasting model  
- [ ] Occupancy forecasting model  
- [ ] RevPAR derived forecast  
- [ ] Backtesting engine  
- [ ] MLflow experiment tracking  
- [ ] MLflow model registry  
- [ ] Airflow DAGs (full pipeline)  
- [ ] Streamlit dashboards (Revenue, Forecast, Backtest, What‑If)  
- [ ] FastAPI deployment  
- [ ] Power BI / Tableau dashboards  

---

---
## 🖼️  Roadmap Diagram  

![Hotel Performance Optimizer Architecture](https://github.com/MOO242/Hotel-Performance-Optimizer/blob/main/Project_architecture.png)
---
