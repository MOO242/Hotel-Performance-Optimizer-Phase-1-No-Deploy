# 🏨 Hotel Performance Optimizer

A production-grade hospitality ML system that predicts hotel rates and demand, exposes them via a FastAPI service, and lets revenue managers explore pricing scenarios through an interactive Streamlit dashboard — all containerized with Docker and deployed publicly on HuggingFace Spaces.

🔗 **Live Demo:** [huggingface.co/spaces/MoAlrazek/HotelPerformanceOptimizer](https://huggingface.co/spaces/MoAlrazek/HotelPerformanceOptimizer)

📂 **Repository:** [github.com/MOO242/Hotel-Performance-Optimizer](https://github.com/MOO242/Hotel-Performance-Optimizer)

---

## 🎯 What This Project Does

Built end-to-end across 3 weeks: ingests booking data, models it through a dbt semantic layer, trains two ML forecasters (rates + demand), and serves predictions through a containerized FastAPI/Streamlit stack with business guardrails and a public deployment.

The system answers two questions hoteliers actually ask:
1. **What rate should I charge** for a given property, room class, season, and channel?
2. **How many rooms will sell** at a given price, and what's the revenue-optimal price point?

---

## 📐 Architecture (Phase 1+2 Shipped)

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1 — DATA SOURCE                                      │
│  AtliQ Grands CSV (synthetic, 134,590 bookings)            │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2 — DATA WAREHOUSE                                   │
│  PostgreSQL (raw + staged tables)                          │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3 — SEMANTIC LAYER (dbt)                             │
│  - fct_bookings_enriched (booking grain)                   │
│  - mtr_occupancy (date grain)                               │
│  - 10-Layer KPI Framework                                   │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 4 — PRE-ML PIPELINE                                  │
│  Feature engineering → YAML config-driven preprocessor      │
│  → preprocessor.pkl                                         │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 5 — ML MODELS                                        │
│  - Rate Forecaster (Random Forest, R²=0.80, MAE=±₹1,780)   │
│  - Demand Forecaster (XGBoost, R²=0.76, MAE=2.74 rooms)    │
│  → model.pkl                                                │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 6 — EXPERIMENT TRACKING                              │
│  MLflow (run logs, metric history)                          │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 7 — SERVING & UI                                     │
│  FastAPI service (POST /predict_rate, /predict_demand)     │
│   - 3-layer business guardrails                             │
│  Streamlit dashboard (Whatiftool + Demand + Rate pages)    │
│   - 9-point demand curve with revenue optimization          │
│   - Confidence ranges using actual model MAE               │
│   - Hurdle rate disclosure                                  │
└────────────────────────┬────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────┐
│  LAYER 8 — DEPLOYMENT                                       │
│  Docker Compose (local) → HuggingFace Spaces (public)      │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Model Results

### Rate Forecaster (Room Rate Prediction)
Predicts `room_rate_amount` from booking attributes. Trained on 81,989 bookings / validated on 26,691 / tested on 25,910 using a time-based split on `check_in_date`.

| Model              | Val MAE | Val MAPE | Test R² |
|--------------------|---------|----------|---------|
| Linear Regression  | 3,244   | 74.8%    | —       |
| **Random Forest** ⭐ | **1,792** | **32.0%** | **0.80** |
| XGBoost            | 1,848   | 32.7%    | —       |

**Test Performance:** MAE = ₹1,780 | RMSE = ₹3,035 | R² = 0.80 | MAPE = 31.8%

### Demand Forecaster (Rooms Sold Prediction)
Predicts `rooms_sold` per hotel-date.

| Model              | Val MAE | Val MAPE | Test R² |
|--------------------|---------|----------|---------|
| Linear Regression  | 2.45    | 16.7%    | —       |
| Random Forest      | 2.30    | 13.9%    | —       |
| **XGBoost** ⭐      | **2.30** | **13.9%** | **0.76** |

**Test Performance:** MAE = 2.74 rooms | RMSE = 3.44 | R² = 0.76 | MAPE = 22.3%

---

## 🛡️ Business Guardrails (Production Design)

Statistical accuracy isn't business correctness. The demand model originally predicted **222% occupancy** for tiny hotels and **−12.59 rooms sold** for out-of-distribution inputs — both mathematically explainable, both physically impossible.

Three layers of defense were added:

1. **API-level clamping** — `rooms_sold ∈ [0, rooms_available]`, with warning logs when guardrails fire
2. **UI transparency** — disclose to users when predictions were clamped (no silent corrections)
3. **Schema validation** — Pydantic bounds (`rooms_available ≥ 20`) reject unrealistic inputs upstream

Plus: every prediction in the UI displays the model's MAE next to it (±₹1,780 for rates, ±2.74 rooms for demand). Revenue managers should never pretend ML is magic — they need error bars to make defensible pricing decisions.

---

## 📊 Dataset Note

This project uses the **AtliQ Grands dataset** — synthetic hospitality data designed for analytics learning. Values are illustrative, not real-market pricing. The engineering patterns are production-ready and apply directly to real hotel chains.

---

## 📊 KPI Framework

The project follows a 10-layer analytics maturity model that progresses from *what happened* → *why* → *what will happen* → *what should we do*.

| Layer | Focus | Example KPIs |
|-------|-------|--------------|
| 1 | Outcome KPIs | RevPAR, ADR, Occupancy %, Room Revenue |
| 2 | Primary Drivers | ADR × Occupancy decomposition |
| 3 | Demand & Booking Health | Lead Time, LOS, Pickup, Cancellation Rate |
| 4 | Segment Performance | Segment mix, Revenue contribution, ADR premium |
| 5 | Channel & Source | Channel mix, Net ADR, OTA dependency |
| 6 | Time Comparisons | YoY, MoM, WoW, Rolling trends, Seasonality |
| 7 | Distribution & Inventory | Availability %, Sell-out days, Compression nights |
| 8 | Forecast & Forward-Looking | OTB Revenue, Forecast accuracy (MAPE) |
| 9 | Commercial Strategy | ADR Opportunity, Price Elasticity, Displacement |
| 10 | Data Quality & Governance | Completeness, Reconciliation, Outlier flags |

---

## 🗂️ Project Structure

```
hotel_performance_optimizer/
│
├── artifacts/                              # Trained models + transformers
│   ├── fct_bookings_enriched/
│   │   └── check_in_date/
│   │       ├── train.csv, val.csv, test.csv
│   │       ├── preprocessor.pkl
│   │       ├── model.pkl
│   │       └── metrics.json
│   └── mtr_occupancy/
│       └── check_in_date/
│           └── (same structure)
│
├── configs/                                # YAML configs (one per model)
│   ├── rate_forecast.yaml
│   └── demand_forecast.yaml
│
├── src/
│   ├── components/                         # SHARED utilities (imported)
│   │   ├── logger.py
│   │   ├── exception.py
│   │   └── data_ingestion.py
│   │
│   ├── mlpipeline/                         # EXECUTABLE pipelines
│   │   ├── data_splitter.py
│   │   ├── data_transformation_engine.py   # YAML config-driven
│   │   ├── rate_forecast.py
│   │   └── demand_forecast.py
│   │
│   └── api/                                # FastAPI service
│       ├── schemas.py                      # Pydantic models
│       ├── model_loader.py                 # Loads pickles once at startup
│       └── serve.py                        # FastAPI app + endpoints
│
├── streamlit_app/                          # Streamlit UI
│   ├── whatiftool.py                       # Landing page (v1.0)
│   └── pages/
│       ├── Demand.py                       # Demand predictor + curve
│       └── Rate.py                         # Rate predictor + confidence band
│
├── dbt_project/                            # Semantic layer
├── notebooks/                              # EDA + experiments
├── Dockerfile                              # FastAPI container
├── Dockerfile.streamlit                    # Streamlit container
├── docker-compose.yml                      # Multi-container orchestration
├── requirements.txt
└── README.md
```

### Design Principles

- **components/** = shared utilities imported across pipelines
- **mlpipeline/** = scripts run via `python -m`, never imported elsewhere
- **api/** = FastAPI service that loads pickled artifacts and serves predictions
- **streamlit_app/** = revenue manager UI calling the FastAPI service internally
- **YAML config-driven preprocessing** — adding a new forecast = a config file, not a refactor

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Data Source | CSV (AtliQ Grands) |
| Database | PostgreSQL |
| Semantic Layer | dbt |
| ML Pipeline | scikit-learn, Random Forest, XGBoost |
| Experiment Tracking | MLflow |
| API Layer | FastAPI + Pydantic |
| UI Layer | Streamlit + Plotly + Matplotlib |
| Containerization | Docker + Docker Compose |
| Deployment | HuggingFace Spaces |
| Logging | Python logging |
| Language | Python 3.12 |

---

## 📌 Roadmap

### ✅ Phase 1 — Data & ML (Shipped May 14, 2026)
- [x] PostgreSQL ingestion + dbt semantic layer
- [x] 10-Layer KPI Framework
- [x] Time-based train/val/test splitter (60/20/20)
- [x] YAML config-driven preprocessing engine
- [x] Rate Forecaster (Random Forest, R²=0.80)
- [x] Demand Forecaster (XGBoost, R²=0.76)

### ✅ Phase 2 — Production & Deployment (Shipped May 16-17, 2026)
- [x] FastAPI service (`/predict_rate`, `/predict_demand`)
- [x] 3-layer business guardrails
- [x] Streamlit dashboard (Whatiftool + Demand + Rate pages)
- [x] 9-point demand curve with revenue optimization
- [x] Hurdle rate logic + confidence range disclosure
- [x] Docker Compose multi-container orchestration
- [x] MLflow experiment tracking
- [x] HuggingFace Spaces public deployment

### 🚧 Phase 3 — In Progress
- [ ] Tableau Public + Power BI executive dashboards (connected to PostgreSQL)
- [ ] `lead_time` feature engineering
- [ ] Hyperparameter tuning (GridSearchCV)
- [ ] TimeSeriesSplit cross-validation

### 📋 Phase 4 — Planned
- [ ] MLflow Model Registry (versioning + staging)
- [ ] Airflow DAGs (scheduled retraining)
- [ ] A/B testing framework
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Pytest test suite
- [ ] ADR + RevPAR derived forecasts
- [ ] Backtesting engine

---

## 🚀 Running the Project

### Prerequisites
- Python 3.12+
- Docker + Docker Compose
- PostgreSQL with AtliQ Grands data loaded
- dbt models materialized (`fct_bookings_enriched`, `mtr_occupancy`)

### Local Installation

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

### Training Pipeline (One-time setup)

```bash
# Step 1: Time-based train/val/test split
python -m src.mlpipeline.data_splitter

# Step 2: Feature preprocessing (sklearn pipeline)
python -m src.mlpipeline.data_transformation_engine

# Step 3: Train models
python -m src.mlpipeline.rate_forecast      # Rate Forecaster
python -m src.mlpipeline.demand_forecast    # Demand Forecaster
```

### Running The Service (Docker Compose)

```bash
# Build and start both FastAPI + Streamlit containers
docker compose up --build

# Access:
#   FastAPI:    http://localhost:8000
#   FastAPI docs: http://localhost:8000/docs
#   Streamlit:  http://localhost:8501
```

### Running Without Docker

```bash
# Terminal 1: FastAPI
uvicorn src.api.serve:app --reload --port 8000

# Terminal 2: Streamlit
streamlit run streamlit_app/whatiftool.py
```

---

## 🔬 Example API Call

```bash
curl -X POST http://localhost:8000/predict_rate \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Mumbai",
    "room_type": "RT1",
    "booking_channel": "direct online",
    "day_type": "weekday",
    "property_id": "16559",
    "season": "Peak",
    "room_class": "Premium",
    "category": "Luxury",
    "number_of_guests": 2,
    "number_of_nights": 3,
    "guest_rating_score": 4.5,
    "hurdle_rate": 433.33
  }'

# Response:
# {"prediction": 9750.0}
```

---

## 💡 Key Engineering Decisions

1. **Time-based split, not random** — prevents data leakage on a temporal target
2. **Generic preprocessor + YAML configs** — one engine serves two models, third is a config file
3. **Business guardrails over retraining** — clamp at API layer, disclose in UI, validate in schema
4. **Disclose model MAE in UI** — revenue managers see confidence ranges, not just point estimates
5. **Load pickles at startup** — predictions are O(1), not O(file_load)
6. **Multi-container Docker** — FastAPI and Streamlit deploy independently, scale independently
7. **synthetic data, real patterns** — engineering is portable, not the numbers

---

## 📜 License

MIT — see [LICENSE](LICENSE) for details.

---

## 🖼️ Architecture Diagram

![Hotel Performance Optimizer Architecture](https://github.com/MOO242/Hotel-Performance-Optimizer/blob/main/Project_architecture.png)
