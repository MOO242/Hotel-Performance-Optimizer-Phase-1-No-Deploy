# 🏨 Hotel Performance Optimizer  

A production-grade analytics and decision-intelligence system for hotel revenue management, built on a modern data & ML architecture that progresses from **data ingestion → validation → semantic modeling → diagnostic analytics → forecasting → prescriptive decision support**.

---

## 📐 Architecture Overview  

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
   ├── Time-Series Backtesting
   └── Model Evaluation (MAPE, RMSE)
        ↓
What-If Analysis & Business Logic
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

## 🎯 Model Results

### Rate Forecaster (RPO)
Predicts `room_rate_amount` from booking attributes. Trained on 81,989 bookings (60%) / validated on 26,691 (20%) / tested on 25,910 (20%) using a time-based split on `check_in_date`.

| Model | Val MAE | Val MAPE | Test R² |
|-------|---------|----------|---------|
| Linear Regression | 3,244 | 74.8% | — |
| **Random Forest** ⭐ | **1,792** | **32.0%** | **0.80** |
| XGBoost | 1,848 | 32.7% | — |

**Test Results:** MAE = ₹1,780 | RMSE = ₹3,035 | R² = 0.80 | MAPE = 31.8%

### Demand Forecaster
Predicts `rooms_sold` per hotel-date.

| Model | Val MAE | Val MAPE | Test R² |
|-------|---------|----------|---------|
| Linear Regression | 2.45 | 16.7% | — |
| Random Forest | 2.30 | 13.9% | — |
| **XGBoost** ⭐ | **2.30** | **13.9%** | **0.76** |

**Test Results:** MAE = 2.74 rooms | RMSE = 3.44 | R² = 0.76 | MAPE = 22.3%

---

## 📊 Dataset Note

This project uses the **AtliQ Grands dataset** — a synthetic dataset designed for hospitality analytics learning. Values are illustrative, not real-market pricing. The engineering patterns demonstrated here are production-ready and applicable to real hotel data.

---

# 📊 KPI Framework  

This project follows a structured **analytics maturity model**, with KPIs organized into **10 logical layers** that move from *what happened* → *why it happened* → *what will happen* → *what should we do*.

---

## **Layer 1 — Outcome KPIs (What happened)**  
Executive-level results. All diagnostics explain movement in these metrics.

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
- Cancellation Rate, No-Show Rate  
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

## **Layer 6 — Time-Based Comparison KPIs**

- YoY, MoM, WoW % change  
- YTD performance  
- Rolling 7 / 14 / 30-day trends  
- Seasonality Index  

---

## **Layer 7 — Distribution & Inventory Health**

- Availability %  
- Out-of-Order Rooms  
- Sell-Out Days  
- Compression Nights  
- Wash % (Cancellations + No-Shows)  

---

## **Layer 8 — Forecast & Forward-Looking KPIs**

- On-The-Books (OTB) Revenue & ADR  
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
├── artifacts/                              # Outputs organized by data source
│   ├── fct_bookings_enriched/
│   │   └── check_in_date/
│   │       ├── train.csv, val.csv, test.csv
│   │       ├── preprocessor.pkl
│   │       ├── model.pkl
│   │       └── metrics.json
│   └── mtr_occupancy/                      # Demand data artifacts
│       └── <date_column>/
│           └── (same structure)
│
├── src/
│   ├── components/                         # SHARED infrastructure (imported)
│   │   ├── logger.py
│   │   ├── exception.py
│   │   └── data_ingestion.py               # DataLoader + PostgreSQL engine
│   │
│   └── mlpipeline/                         # EXECUTABLE pipelines (python -m)
│       ├── data_splitter.py                # Generic: time-based train/val/test split
│       ├── data_transformation.py          # Generic: sklearn preprocessing
│       ├── rate_forecast.py                # RPO trainer (room rate prediction)
│       └── demand_forecast.py              # Demand trainer (rooms sold prediction)
│
├── dbt_project/                            # Semantic layer
├── notebooks/
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

### Design Principles

- **components/** = shared utilities imported across pipelines
- **mlpipeline/** = scripts run via `python -m`, never imported elsewhere
- **Generic splitter + preprocessor** serve any table via `table_name` + `date_column` params
- **Specialized trainers** per model type for business-specific evaluation
- **Artifacts organized by data source** for clean multi-model separation

---

# 🛠️ Tech Stack  

| Layer                    | Technology                                  |
| ------------------------ | ------------------------------------------- |
| ELT & Data Ingestion     | Python, API clients, Web Scraping           |
| Database                 | PostgreSQL / Snowflake / SQL Server         |
| Semantic Layer           | dbt                                          |
| Data Validation          | Python, Pandas                              |
| Feature Store            | Python, SQL                                 |
| Machine Learning         | Scikit-learn, XGBoost, MLflow               |
| Orchestration            | Apache Airflow                              |
| KPI Engine               | Python + SQL                                |
| API Layer                | FastAPI                                     |
| App Layer                | Streamlit                                   |
| Visualization            | Power BI, Tableau                           |
| Logging                  | Python logging                              |
| Testing                  | Pytest                                      |

---

# 📌 Roadmap

### ✅ Shipped (Phase 1)
- [x] Architecture design
- [x] Data ingestion layer (PostgreSQL + dbt)
- [x] Data validation & feature store
- [x] Semantic layer (dbt: `fct_bookings_enriched`, `mtr_occupancy`)
- [x] KPI engine
- [x] Diagnostic analytics
- [x] Time-based train/val/test splitter (60/20/20)
- [x] sklearn preprocessing pipeline (generic engine)
- [x] **Rate Forecaster (RPO)** — Random Forest, Test R² = 0.80
- [x] **Demand Forecaster** — XGBoost, Test R² = 0.76

### 🚧 In Progress (Phase 2)
- [ ] `lead_time` feature engineering
- [ ] MLflow experiment tracking
- [ ] Hyperparameter tuning (GridSearchCV)
- [ ] TimeSeriesSplit cross-validation

### 📋 Planned (Phase 3)
- [ ] ADR + RevPAR derived forecasts
- [ ] Backtesting engine
- [ ] FastAPI serving endpoints
- [ ] Streamlit dashboards (hotelier UI)
- [ ] Airflow DAGs
- [ ] Power BI / Tableau dashboards
- [ ] Docker containerization
- [ ] Tests directory (pytest)

---

## 🚀 Running the Pipeline

### Prerequisites
- Python 3.12+
- PostgreSQL with AtliQ Grands data loaded
- dbt models materialized (`fct_bookings_enriched`, `mtr_occupancy`)

### Installation
```bash
git clone https://github.com/MOO242/Hotel-Performance-Optimizer.git
cd Hotel-Performance-Optimizer

python -m venv env
.\env\Scripts\activate         # Windows
# source env/bin/activate      # Linux/Mac

pip install -r requirements.txt
cp .env.example .env
# Edit .env with PostgreSQL credentials
```

### Execution
```bash
# Step 1: Time-based train/val/test split
python -m src.mlpipeline.data_splitter

# Step 2: Feature preprocessing (sklearn pipeline)
python -m src.mlpipeline.data_transformation

# Step 3: Train models (choose one)
python -m src.mlpipeline.rate_forecast      # Rate Forecaster (RPO)
python -m src.mlpipeline.demand_forecast    # Demand Forecaster
```

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

---

## 🖼️ Architecture Diagram  

![Hotel Performance Optimizer Architecture](https://github.com/MOO242/Hotel-Performance-Optimizer/blob/main/Project_architecture.png)
