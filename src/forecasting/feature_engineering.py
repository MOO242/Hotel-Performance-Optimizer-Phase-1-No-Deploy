import pandas as pd
from src.components.data_ingestion import DataLoader, engine
from src.components.logger import logger
from src.components.exception import CustomException

Data = DataLoader(engine)
df = Data.data_load("fact_bookings")


class FeatureEngineering:

    def __init__(self, df):
        self.df = df

    def calculate_lead_time(self):
        try:
            logger.info(f"Calculating lead time for {df}")
            self.df["lead_time"] = (
                self.df["check_in_date"] - self.df["booking_date"]
            ).dt.days
            return self.df["lead_time"]

        except Exception as e:
            logger.error("Wrong time")
            raise CustomException(e)


feature_engineer = FeatureEngineering(df)
time = feature_engineer.calculate_lead_time()
print(df.head())
