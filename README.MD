# 🏨 Hotel Performance Optimizer  

A production‑grade analytics and decision‑intelligence system for hotel revenue management, built on a modern analytics maturity framework that progresses from **descriptive KPIs → diagnostic analysis → predictive forecasting → prescriptive decision support**.

---

## 📐 Architecture Overview

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

```markdown
![Hotel Performance Optimizer Architecture](Project_Architecture.jpg)

```
