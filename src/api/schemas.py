from pydantic import BaseModel, Field
from typing import Literal

"""
schemas.py
──────────
Pydantic models for API input/output validation.
"""


# === RATE PREDICTION SCHEMAS ===
class RateBookingInput(BaseModel):

    # numerical
    hurdle_rate: float = Field(..., ge=0)
    number_of_guests: int = Field(..., ge=1, le=6)
    number_of_nights: int = Field(..., ge=1, le=30)
    guest_rating_score: float = Field(..., ge=1, le=5)

    # nominal

    property_id: str = Field(..., description="Hotel property ID(as string)")
    city: str = Field(..., description="Hotel city")
    booking_channel: str = Field(..., description="Booking channel")
    day_type: Literal["weekday", "weekend"]
    room_type: Literal["RT1", "RT2", "RT3", "RT4"]

    # ordinal

    season: Literal["Low Season", "Shoulder", "High Season", "Peak"]
    room_class: Literal["Standard", "Elite", "Premium", "Presidential"]
    category: Literal["Economy", "Luxury"]


class RatePredictionResponse(BaseModel):

    prediction: float = Field(
        ..., ge=0, description="Recommended room rate in inr per night"
    )
    model_version: str = "v1.0"
    model_type: str = "RandomForestRegressor"


# === DEMAND PREDICTION SCHEMAS ===
class DemandBookingInput(BaseModel):
    # numerical
    rooms_available: int = Field(..., ge=0)

    # nominal

    property_id: str = Field(..., description="Hotel property ID(as string)")
    room_category: Literal["RT1", "RT2", "RT3", "RT4"]


class DemandPredictionResponse(BaseModel):

    prediction: float = Field(..., ge=0, description="Recommended room sold per night")
    model_version: str = "v1.0"
    model_type: str = "XGBRegressor"
