"""
model_demand_trainer.py
────────────────────────
Integrated Engine for training Rate and Demand models.
"""

import os
import json
import pickle
import argparse
import numpy as np
from src.mlpipeline.data_transformation_engine import (
    FeaturePreprocessor,
    FeaturePreprocessorConfig,
)
from src.components.logger import logger
from src.components.exception import CustomException

from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    mean_absolute_percentage_error,
)


class ForecastModel:
    """Trains and evaluates ML models for hotel demand forecasting."""

    def __init__(self, config: FeaturePreprocessorConfig):

        try:
            self.config = config

            self.output_dir = os.path.join(
                "artifacts", self.config.table_name, self.config.date_column
            )

            self.model_path = os.path.join(self.output_dir, "model.pkl")
            self.metrics_path = os.path.join(self.output_dir, "metrics.json")

            os.makedirs(self.output_dir, exist_ok=True)
            logger.info(
                f"ModelDemandTrainer initialized for table '{self.config.table_name}'"
            )

        except Exception as e:
            logger.error("Failed to initialize ModelDemandTrainer")
            raise CustomException(e)

    # ---------------------------------------------------------
    # Evaluation helper
    # ---------------------------------------------------------
    def evaluate(self, y_true, y_pred):
        """Compute standard regression metrics."""
        return {
            "MAE": mean_absolute_error(y_true, y_pred),
            "RMSE": np.sqrt(mean_squared_error(y_true, y_pred)),
            "R2": r2_score(y_true, y_pred),
            "MAPE": mean_absolute_percentage_error(y_true, y_pred),
        }

    # ---------------------------------------------------------
    # Main training logic
    # ---------------------------------------------------------
    def train_models(self, train_arr, val_arr, test_arr):
        try:
            logger.info("Starting model training...")

            # Split arrays
            X_train, y_train = train_arr[:, :-1], train_arr[:, -1]
            X_val, y_val = val_arr[:, :-1], val_arr[:, -1]
            X_test, y_test = test_arr[:, :-1], test_arr[:, -1]

            # Candidate models
            models = {
                "Linear Regression": LinearRegression(),
                "Random Forest": RandomForestRegressor(random_state=42),
                "XGBoost": XGBRegressor(random_state=42),
            }

            all_val_metrics = {}

            # Train & validate
            for name, model in models.items():
                logger.info(f"Training model: {name}")
                model.fit(X_train, y_train)

                y_pred_val = model.predict(X_val)
                val_metrics = self.evaluate(y_val, y_pred_val)
                all_val_metrics[name] = val_metrics

                logger.info(
                    f"{name}  Val MAE: {val_metrics['MAE']:.3f}, "
                    f"MAPE: {val_metrics['MAPE']:.3f}"
                )

            # Select best model
            winner_name = min(all_val_metrics, key=lambda k: all_val_metrics[k]["MAE"])
            winner_model = models[winner_name]

            logger.info(f"Best model selected: {winner_name}")

            # Evaluate on test set
            y_pred_test = winner_model.predict(X_test)
            test_metrics = self.evaluate(y_test, y_pred_test)

            logger.info(f"Test metrics: {test_metrics}")

            # Save model
            with open(self.model_path, "wb") as f:
                pickle.dump(winner_model, f)
            logger.info(f"Saved best model to {self.model_path}")

            # Save metrics
            all_metrics = {
                "val_metrics": all_val_metrics,
                "winner": winner_name,
                "test_metrics": test_metrics,
            }

            with open(self.metrics_path, "w") as f:
                json.dump(all_metrics, f, indent=2, default=float)
            logger.info(f"Saved metrics to {self.metrics_path}")

            return winner_name, all_metrics

        except Exception as e:
            logger.error("Model training failed")
            raise CustomException(e)


# ---------------------------------------------------------
# Script execution
# ---------------------------------------------------------
if __name__ == "__main__":

    # Integration of Argument Parser
    parser = argparse.ArgumentParser(description="Hotel Forecast Model Trainer CLI")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML config",
    )
    args = parser.parse_args()
    try:

        logger.info("Starting demand forecasting pipeline...")
        

        # Model forecast
        active_config = FeaturePreprocessorConfig(
            date_column="check_in_date",
            table_name="fct_bookings_enriched",
            config_path=args.config,
        )
        # Preprocessing
        pp = FeaturePreprocessor(active_config)
        train_arr, val_arr, test_arr, _ = pp.transform_bookings(
            os.path.join(
                "artifacts",
                active_config.table_name,
                active_config.date_column,
                "train.csv",
            ),
            os.path.join(
                "artifacts",
                active_config.table_name,
                active_config.date_column,
                "val.csv",
            ),
            os.path.join(
                "artifacts",
                active_config.table_name,
                active_config.date_column,
                "test.csv",
            ),
        )

        # Training
        trainer = ForecastModel(active_config)
        winner, metrics = trainer.train_models(train_arr, val_arr, test_arr)

        print(f"\nWinner: {winner}")
        print(f"Test metrics: {metrics}")

    except Exception as e:
        logger.error("Demand forecasting pipeline failed")
        raise CustomException(e)
