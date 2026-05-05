from src.components.logger import logger
from src.components.exception import CustomException


class FeatureEngineering:

    def __init__(self, bookings):
        self.bookings = bookings

    def calculate_lead_time(self):
        try:
            logger.info("Calculating lead time")
            self.bookings["lead_time"] = (
                self.bookings["check_in_date"] - self.bookings["booking_date"]
            ).dt.days
            logger.info("Calculating completed")
            return self.bookings
            
        except Exception as e:
            logger.error("Wrong time")
            raise CustomException(e)

    def calculate_cancellation_rate(self):
        try:
            logger.info("Calculating cancellation rate")

            total = self.bookings.groupby("property_id")["booking_id"].count()
            cancelled = (
                self.bookings[self.bookings["booking_status"] == "Cancelled"]
                .groupby("property_id")["booking_id"]
                .count()
            )
            cancellation_rate = cancelled / total * 100
            self.bookings["cancellation_rate"] = (
                self.bookings["property_id"].map(cancellation_rate).fillna(0)
            )

            logger.info("Cancellation rate calculation complete")

            return self.bookings

        except Exception as e:
            logger.error(f"Cancellation rate calculation failed: {e}")
            raise CustomException(e)

    def calculate_no_show_rate(self):
        try:
            logger.info("Calculating No Show rate")

            total = self.bookings.groupby("property_id")["booking_id"].count()
            No_Show = (
                self.bookings[self.bookings["booking_status"] == "No Show"]
                .groupby("property_id")["booking_id"]
                .count()
            )
            no_show_rate = No_Show / total * 100
            self.bookings["no_show_rate"] = (
                self.bookings["property_id"].map(no_show_rate).fillna(0)
            )

            logger.info("No Show rate calculation complete")

            return self.bookings

        except Exception as e:
            logger.error(f"No show calculation failed: {e}")
            raise CustomException(e)

    def calculate_platform_cancel_rate(self):
        try:
            logger.info("Calculating platform cancel rate")

            total = self.bookings.groupby("booking_channel")["booking_id"].count()
            platform_cancel = (
                self.bookings[self.bookings["booking_status"] == "Cancelled"]
                .groupby("booking_channel")["booking_id"]
                .count()
            )
            platform_cancel_rate = platform_cancel / total * 100
            self.bookings["platform_cancel_rate"] = (
                self.bookings["booking_channel"].map(platform_cancel_rate).fillna(0)
            )

            logger.info("platform cancel rate calculation complete")

            return self.bookings

        except Exception as e:
            logger.error(f"platform cancel rate calculation failed: {e}")
            raise CustomException(e)
