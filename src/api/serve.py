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
from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    RateBookingInput,
    RatePredictionResponse,
    DemandBookingInput,
    DemandPredictionResponse,
)
from src.api.model_loader import ModelLoader, ModelConfig
from src.components.logger import logger

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
        X = demand_loader.preprocessor_file.transform(df)

        if hasattr(X, "toarray"):
            X = X.toarray()
        prediction = demand_loader.model_file.predict(X)[0]

        logger.info(f"Demand prediction : {prediction:.2f} room")

        return DemandPredictionResponse(
            prediction=float(prediction),
        )

    except Exception as e:
        logger.error(f"Demand prediction failed: {e}")
        raise HTTPException(
            status_code=500, detail=f"Demand prediction failed: {str(e)}"
        )
