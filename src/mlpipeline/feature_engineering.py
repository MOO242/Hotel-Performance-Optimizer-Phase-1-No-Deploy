import pandas as pd
from src.components.logger import logger
from src.components.exception import CustomException


class FeatureEngineering:
    """
    Apply feature engineering transformations to a hotel bookings dataset.

    Parameters
    ----------
    bookings : pd.DataFrame
        Raw bookings dataset loaded from the database.
    """

    def __init__(self, bookings: pd.DataFrame):
        self.bookings = bookings.copy()

    # ---------------------------------------------------------
    # 1. Lead Time
    # ---------------------------------------------------------
    def calculate_lead_time(self) -> pd.DataFrame:
        """
        Compute lead time (days between booking date and check-in date).
        """
        try:
            logger.info("Calculating lead_time feature")

            df = self.bookings.copy()
            df["lead_time"] = (df["check_in_date"] - df["booking_date"]).dt.days

            logger.info("lead_time calculation complete")
            self.bookings = df
            return df

        except Exception as e:
            logger.error("Lead time calculation failed")
            raise CustomException(e)

    # ---------------------------------------------------------
    # 2. Cancellation Rate per Property
    # ---------------------------------------------------------
    def calculate_cancellation_rate(self) -> pd.DataFrame:
        """
        Compute cancellation rate (%) per property_id.
        """
        try:
            logger.info("Calculating cancellation_rate feature")

            df = self.bookings.copy()
            total = df.groupby("property_id")["booking_id"].count()
            cancelled = (
                df[df["booking_status"] == "Cancelled"]
                .groupby("property_id")["booking_id"]
                .count()
            )

            rate = (cancelled / total * 100).fillna(0)
            df["cancellation_rate"] = df["property_id"].map(rate)

            logger.info("cancellation_rate calculation complete")
            self.bookings = df
            return df

        except Exception as e:
            logger.error("Cancellation rate calculation failed")
            raise CustomException(e)

    # ---------------------------------------------------------
    # 3. No-Show Rate per Property
    # ---------------------------------------------------------
    def calculate_no_show_rate(self) -> pd.DataFrame:
        """
        Compute no-show rate (%) per property_id.
        """
        try:
            logger.info("Calculating no_show_rate feature")

            df = self.bookings.copy()
            total = df.groupby("property_id")["booking_id"].count()
            no_show = (
                df[df["booking_status"] == "No Show"]
                .groupby("property_id")["booking_id"]
                .count()
            )

            rate = (no_show / total * 100).fillna(0)
            df["no_show_rate"] = df["property_id"].map(rate)

            logger.info("no_show_rate calculation complete")
            self.bookings = df
            return df

        except Exception as e:
            logger.error("No-show rate calculation failed")
            raise CustomException(e)

    # ---------------------------------------------------------
    # 4. Platform Cancellation Rate
    # ---------------------------------------------------------
    def calculate_platform_cancel_rate(self) -> pd.DataFrame:
        """
        Compute cancellation rate (%) per booking_channel.
        """
        try:
            logger.info("Calculating platform_cancel_rate feature")

            df = self.bookings.copy()
            total = df.groupby("booking_channel")["booking_id"].count()
            cancelled = (
                df[df["booking_status"] == "Cancelled"]
                .groupby("booking_channel")["booking_id"]
                .count()
            )

            rate = (cancelled / total * 100).fillna(0)
            df["platform_cancel_rate"] = df["booking_channel"].map(rate)

            logger.info("platform_cancel_rate calculation complete")
            self.bookings = df
            return df

        except Exception as e:
            logger.error("Platform cancel rate calculation failed")
            raise CustomException(e)

    # ---------------------------------------------------------
    # 5. Run All Feature Engineering Steps
    # ---------------------------------------------------------
    def run_all(self) -> pd.DataFrame:
        """
        Apply all feature engineering steps in sequence.
        """
        logger.info("Running full feature engineering pipeline")

        self.calculate_lead_time()
        self.calculate_cancellation_rate()
        self.calculate_no_show_rate()
        self.calculate_platform_cancel_rate()

        logger.info("Feature engineering pipeline complete")
        return self.bookings
