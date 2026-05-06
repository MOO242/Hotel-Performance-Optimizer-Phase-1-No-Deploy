import pandas as pd
from src.components.data_ingestion import DataLoader, engine
from src.forecasting.feature_engineering import FeatureEngineering
from src.components.logger import logger
from src.components.exception import CustomException
from src.components.data_transformation import DataTransformation

data = DataLoader(engine)
bookings = data.data_load("fct_bookings_enriched")
features_data = data.data_load("features_enriched")


class FeatureStore:
    """
    Save Feature into PostgreSQL table.

    """

    def __init__(self, table_name, engine):
        self.bookings = bookings
        self.engine = engine

    def save(self, df, table_name):

        try:
            logger.info("Starting ingestion Feature")

            df.to_sql(
                table_name,
                self.engine,
                if_exists="replace",
                index=False,
                chunksize=5000,
            )

            logger.info("Successfully inserted")

        except Exception as e:
            logger.error(f"Ingestion failed {e}")
            raise CustomException(e)

    def verify(self, table_name):

        try:
            logger.info("Starting verification")

            query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
            df = pd.read_sql(query, self.engine)

            logger.info("verification Successfully completed")
            return df

        except Exception as e:
            logger.error(f"verification failed {e}")
            raise CustomException(e)


# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":

    """Feature Engineering to database"""

    feature_engineer = FeatureEngineering(bookings)
    Feature_Store = FeatureStore("features_enriched", engine)

    bookings = feature_engineer.calculate_lead_time()
    bookings = feature_engineer.calculate_cancellation_rate()
    bookings = feature_engineer.calculate_no_show_rate()
    bookings = feature_engineer.calculate_platform_cancel_rate()

    Feature_Store.save(feature_engineer.bookings, "features_enriched")
    Feature_Store.verify("features_enriched")

    """ Data Transformation to database"""

    dataTransformation = DataTransformation(features_data)

    season_map = {"Low Season": 0, "High Season": 1, "Peak Season": 2}
    room_map = {"Standard": 0, "Elite": 1, "Premium": 2, "Presidential": 3}
    OneHot = ["city", "booking_channel", "booking_status"]
    binary_map = {"day_type": "weekeday", "category": "Luxury"}

    features_data = dataTransformation.label_encode("season", season_map)
    features_data = dataTransformation.label_encode("room_class", room_map)
    features_data = dataTransformation.one_hot_encode(OneHot)
    features_data = dataTransformation.binary_encode(binary_map)

    """Save as Pki file in artifacts    """
    dataTransformation.save_preprocessor()

    Feature_Store.save(dataTransformation.features_data, "features_transformed")
    Feature_Store.verify("features_transformed")
