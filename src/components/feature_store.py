import pandas as pd
from src.components.data_ingestion import DataLoader, engine
from src.forecasting.feature_engineering import FeatureEngineering
from src.components.logger import logger
from src.components.exception import CustomException

Data = DataLoader(engine)
bookings = Data.data_load("fct_bookings_enriched")


class FeatureStore:
    """
    Save Feature into PostgreSQL table.

    """

    def __init__(self, table_name, engine):
        self.table_name = table_name
        self.bookings = bookings
        self.engine = engine

    def save(self, df):

        try:
            logger.info("Starting ingestion Feature")

            df.to_sql(
                self.table_name,
                self.engine,
                if_exists="replace",
                index=False,
                chunksize=5000,
            )

            logger.info("Successfully inserted")

        except Exception as e:
            logger.error(f"Ingestion failed {e}")
            raise CustomException(e)

    def verify(self, df):

        try:
            logger.info("Starting verification")

            query = f"SELECT COUNT(*) AS row_count FROM {self.table_name}"
            df = pd.read_sql(query, engine)

            logger.info("verification Successfully completed")
            return df

        except Exception as e:
            logger.error(f"verification failed {e}")
            raise CustomException(e)


# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":

    feature_engineer = FeatureEngineering(bookings)
    Feature_Store = FeatureStore("features_enriched", engine)

    bookings = feature_engineer.calculate_lead_time()
    bookings = feature_engineer.calculate_cancellation_rate()
    bookings = feature_engineer.calculate_no_show_rate()
    bookings = feature_engineer.calculate_platform_cancel_rate()

    Feature_Store.save(feature_engineer.bookings)
    Feature_Store.verify(feature_engineer.bookings)
