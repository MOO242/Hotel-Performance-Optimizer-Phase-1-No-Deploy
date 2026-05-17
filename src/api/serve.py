"""
serve.py
────────
FastAPI service for Hotel Performance Optimizer.

Endpoints:
    GET  /                - Health check
    POST /predict_rate    - Predict room rate from booking attributes
    POST /predict_demand  - Predict rooms_sold for hotel-date
"""

import pandas as pd
import mlflow
from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    RateBookingInput,
    RatePredictionResponse,
    DemandBookingInput,
    DemandPredictionResponse,
)
from src.api.model_loader import ModelLoader, ModelConfig
from src.components.logger import logger

# === MLFLOW SETUP ===
mlflow.set_tracking_uri("http://localhost:5000")
mlflow.set_experiment("HotelPerformanceOptimizer")

# === APP INITIALIZATION ===
app = FastAPI(
    title="Hotel Performance Optimizer API",
    description="ML-powered hospitality forecasting (Rate + Demand)",
    version="1.0.0",
)

# === LOAD MODELS ONCE AT STARTUP ===
logger.info("Loading models...")

rate_loader = ModelLoader(
    config=ModelConfig(
        table_name="fct_bookings_enriched",
        date_column="check_in_date",
    )
)


demand_loader = ModelLoader(
    config=ModelConfig(
        table_name="mtr_occupancy",
        date_column="check_in_date",
    )
)

logger.info("All models loaded. API ready.")


# === HEALTH CHECK ===
@app.get("/")
def root():
    return {
        "service": "Hotel Performance Optimizer",
        "status": "healthy",
        "endpoints": ["/predict_rate", "/predict_demand", "/docs"],
    }


# === RATE PREDICTION ===


@app.post("/predict_rate", response_model=RatePredictionResponse)
def predict_rate(booking: RateBookingInput):
    """Predict room rate (INR) from booking attributes."""
    try:
        df = pd.DataFrame([booking.model_dump()])
        X = rate_loader.preprocessor_file.transform(df)

        if hasattr(X, "toarray"):
            X = X.toarray()

        prediction = rate_loader.model_file.predict(X)[0]

        logger.info(f"Rate prediction: ₹{prediction:.2f}")

        # === MLFLOW LOGGING ===
        with mlflow.start_run(run_name="predict_rate"):
            # Log all inputs as parameters
            for key, value in booking.model_dump().items():
                mlflow.log_param(key, value)
            # Log prediction as metric
            mlflow.log_metric("predicted_rate", float(prediction))
            mlflow.set_tag("endpoint", "predict_rate")
            mlflow.set_tag("model", "RandomForest_Rate_v1.0")

        return RatePredictionResponse(
            prediction=float(prediction),
        )

    except Exception as e:
        logger.error(f"Rate prediction failed: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict_demand", response_model=DemandPredictionResponse)
def predict_demand(Demand: DemandBookingInput):
    """Predict rooms sold for a hotel-date."""
    try:

        df = pd.DataFrame([Demand.model_dump()])
        logger.info(f"Production DataFrame structure:\n{df.dtypes}")
        logger.info(f"Production DataFrame columns order: {list(df.columns)}")
        X = demand_loader.preprocessor_file.transform(df)

        if hasattr(X, "toarray"):
            X = X.toarray()
        prediction = demand_loader.model_file.predict(X)[0]
        logger.info(f"Raw prediction before clamp: {prediction}")
        logger.info(f"Demand prediction : {prediction:.2f} room")

        # === MLFLOW LOGGING ===
        with mlflow.start_run(run_name="predict_demand"):
            # Log all inputs as parameters
            for key, value in Demand.model_dump().items():
                mlflow.log_param(key, value)
            # Log prediction as metric
            mlflow.log_metric("predicted_demand", max(0.0, float(prediction)))
            mlflow.set_tag("endpoint", "predict_demand")
            mlflow.set_tag("model", "RandomForest_Demand_v1.0")

        return DemandPredictionResponse(prediction=max(0.0, float(prediction)))

    except Exception as e:
        logger.error(f"Demand prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Demand prediction failed: {str(e)}"
        )
