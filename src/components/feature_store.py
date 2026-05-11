"""
Feature Engineering Pipeline

This script loads the raw bookings dataset from PostgreSQL, applies the full
feature engineering pipeline (lead time, cancellation rate, no-show rate,
platform cancellation rate), and saves the enriched feature dataset back
into the database as `features_enriched`.

Workflow:
1. Load raw bookings table: fct_bookings_enriched
2. Apply FeatureEngineering.run_all()
3. Save engineered features into PostgreSQL
4. Verify row count after ingestion
"""

import pandas as pd
from src.components.data_ingestion import DataLoader, engine
from src.forecasting.feature_engineering import FeatureEngineering
from src.components.logger import logger
from src.components.exception import CustomException

# Load raw data
data = DataLoader(engine)
bookings = data.data_load("fct_bookings_enriched")


class FeatureStore:
    """
    Save engineered features into a PostgreSQL table.
    """

    def __init__(self, engine):
        self.engine = engine

    def save(self, df, table_name):
        try:
            logger.info(f"Starting ingestion into table: {table_name}")

            df.to_sql(
                table_name,
                self.engine,
                if_exists="replace",
                index=False,
                chunksize=5000,
            )

            logger.info("Feature ingestion completed successfully")

        except Exception as e:
            logger.error(f"Feature ingestion failed: {e}")
            raise CustomException(e)

    def verify(self, table_name):
        try:
            logger.info(f"Verifying table: {table_name}")

            query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
            df = pd.read_sql(query, self.engine)

            logger.info("Verification completed successfully")
            return df

        except Exception as e:
            logger.error(f"Verification failed: {e}")
            raise CustomException(e)


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":

    """
    Main Execution:
    Runs the feature engineering pipeline and writes the enriched dataset
    to the `features_enriched` table in PostgreSQL.
    """

    logger.info("Starting Feature Engineering pipeline")

    feature_engineer = FeatureEngineering(bookings)

    # Apply all feature engineering steps
    bookings = feature_engineer.run_all()

    # Save to DB
    Feature_Store = FeatureStore(engine)
    Feature_Store.save(bookings, "features_enriched")

    # Verify ingestion
    print(Feature_Store.verify("features_enriched"))
