# 🏨 Hotel Performance Optimizer  

A production‑grade analytics and decision‑intelligence system for hotel revenue management, built on a modern data & ML architecture that progresses from **data ingestion → validation → semantic modeling → diagnostic analytics → forecasting → prescriptive decision support**.

---

## 📐 Architecture Overview  
*(Fully updated to match your diagram)*

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

# 📊 KPI Framework  

This project follows a structured **analytics maturity model**, with KPIs organized into **10 logical layers** that move from *what happened* → *why it happened* → *what will happen* → *what should we do*.

---

## **Layer 1 — Outcome KPIs (What happened)**  
Executive‑level results. All diagnostics explain movement in these metrics.

| KPI             | Definition                                   |
| --------------- | -------------------------------------------- |
| Room Revenue    | Total revenue from room sales                |
| RevPAR          | Revenue per Available Room                   |
| ADR             | Average Daily Rate                           |
| Occupancy %     | Rooms Sold ÷ Rooms Available                 |
| Rooms Sold      | Total occupied rooms                         |
| Rooms Available | Total inventory available                    |

---

## **Layer 2 — Primary Driver KPIs (Why it happened)**  
Foundational decomposition.

- ADR vs Occupancy impact  
- Revenue = ADR × Rooms Sold  
- RevPAR = ADR × Occupancy  

**Rule:** Every RevPAR movement must be explained through **ADR vs Occupancy**.

---

## **Layer 3 — Demand & Booking Health KPIs**

- Gross & Net Bookings  
- Cancellation Rate, No‑Show Rate  
- Booking Lead Time  
- Length of Stay (LOS)  
- Pickup (Daily / Weekly)  
- Pace vs LY & Budget  

---

## **Layer 4 — Segment Performance KPIs**

For each segment (Transient, Group, Contract, Wholesale):

- Revenue, Rooms Sold, ADR, RevPAR  
- Segment Mix %, Revenue Contribution %  
- ADR Premium / Discount vs Total  

---

## **Layer 5 — Channel & Source KPIs**

- Channel Mix % (Direct, OTA, GDS, Voice)  
- ADR by Channel  
- Net ADR (after commissions)  
- OTA Dependency %  
- Cost of Sale %  

---

## **Layer 6 — Time‑Based Comparison KPIs**

- YoY, MoM, WoW % change  
- YTD performance  
- Rolling 7 / 14 / 30‑day trends  
- Seasonality Index  

---

## **Layer 7 — Distribution & Inventory Health**

- Availability %  
- Out‑of‑Order Rooms  
- Sell‑Out Days  
- Compression Nights  
- Wash % (Cancellations + No‑Shows)  

---

## **Layer 8 — Forecast & Forward‑Looking KPIs**

- On‑The‑Books (OTB) Revenue & ADR  
- Forecast Occupancy & RevPAR  
- Pickup Forecast  
- Forecast Accuracy (MAPE, Error %)  
- Budget Variance  

---

## **Layer 9 — Commercial Strategy KPIs (Advanced)**

- ADR Opportunity Index  
- Price Elasticity  
- Displacement Analysis (Group)  
- BAR vs Achieved ADR  
- Loyalty Revenue %, Repeat Guest %  

---

## **Layer 10 — Data Quality & Governance KPIs**

- Data Completeness %  
- Missing ADR / Revenue counts  
- Outlier detection flags  
- KPI reconciliation checks  

---

# 🗂️ Project Structure  


```
hotel_performance_optimizer/
│
├── airflow/                         # DAGs for ingestion, training, scoring
├── artifacts/                       # Saved models, scalers, backtests
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

# 🛠️ Tech Stack  
*(Updated to match the architecture diagram)*

| Layer                    | Technology                                  |
| ------------------------ | ------------------------------------------- |
| ELT & Data Ingestion     | Python, API clients, Web Scraping           |
| Database                 | PostgreSQL / Snowflake / SQL Server         |
| Semantic Layer           | dbt                                          |
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

# 📌 Roadmap  
*(Clean, aligned with architecture)*

- [x] Architecture design  
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
- [ ] Airflow DAGs  
- [ ] Streamlit dashboards  
- [ ] FastAPI deployment  
- [ ] Power BI / Tableau dashboards  

---
## Setup

### Prerequisites
- Python 3.12+
- PostgreSQL with `fct_bookings_enriched` table loaded

### Installation

```bash
# Clone the repo
git clone https://github.com/MOO242/hotel-performance-optimizer.git
cd hotel-performance-optimizer

# Create virtual environment
python -m venv env
source env/bin/activate  # Linux/Mac
# OR
.\env\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database credentials

# Run the pipeline
python -m src.components.data_splitter
```

### License
This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---
## 🖼️  Roadmap Diagram  

![Hotel Performance Optimizer Architecture](https://github.com/MOO242/Hotel-Performance-Optimizer/blob/main/Project_architecture.png)
---
