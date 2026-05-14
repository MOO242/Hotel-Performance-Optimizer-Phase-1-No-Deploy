import os
import pickle
import pandas as pd
from dataclasses import dataclass
from src.components.logger import logger
from src.components.exception import CustomException


@dataclass
class PredictionConfig:
    table_name: str = "fct_bookings_enriched"
    date_column: str = "check_in_date"
    mae_error: float = 1780
    R2: float = 80
    r2_score: float = 0.79
    confidence_pct: float = 80


class RatePrediction:

    def __init__(self, config: PredictionConfig):

        self.config = config

        self.file_path = os.path.join(
            "artifacts", self.config.table_name, self.config.date_column
        )

        self.model = self._load_artifact("model.pkl")
        self.preprocessor = self._load_artifact("preprocessor.pkl")

    def _load_artifact(self, file_name):
        path = os.path.join(self.file_path, file_name)
        try:
            with open(path, "rb") as f:
                return pickle.load(f)

        except FileNotFoundError as e:
            logger.error(f"Artifact not found.{path}")
            raise CustomException(e)

    def get_rate(self, input_data: dict):

        if not isinstance(input_data, dict) or not input_data:
            raise ValueError("input_data must be a non-empty dictionary")

        df = pd.DataFrame([input_data])
        transformed_data = self.preprocessor.transform(df)
        prediction = self.model.predict(transformed_data)[0]

        return {
            "predicted_rate": round(prediction, 2),
            "range_min": round(prediction - self.config.mae_error, 2),
            "range_max": round(prediction + self.config.mae_error, 2),
            "confidence_level": (
                f"{self.config.confidence_pct}% " f"(R2: {self.config.r2_score})"
            ),
        }


if __name__ == "__main__":
    inference = RatePrediction(PredictionConfig())

    future_booking = {
        "check_in_date": "2026-12-25",
        "room_type": "RT1",
        "booking_channel": "direct online",
        "city": "Delhi",
        "room_class": "Standard",
        "property_id": "16562",
        "day_type": "journey",
        "number_of_guests": "2",
        "guest_rating_score": "5",
        "hurdle_rate": "433.33",
        "number_of_nights": "2",
        "season": "High Season",
        "category": "Luxury",
    }

    result = inference.get_rate(future_booking)

    print("--- Future Rate Forecast ---")
    print(f"Recommended Price: {result['predicted_rate']}")
    print(f"Strategic Range:   {result['range_min']} - {result['range_max']}")
    print(f"Confidence:        {result['confidence_level']}")
