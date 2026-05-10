"""
booking_splitter.py
───────────────────
Splits enriched bookings DataFrame into training and test sets
using a time-based cutoff — preserves temporal order for honest forecasting.

Business rationale:
    Hotel demand is time-series. Random splits would let the model "peek
    into the future" during training, inflating performance metrics.
    A time-based split simulates real production: train on historical
    bookings, predict on future ones.
"""

import os
import pandas as pd
from dataclasses import dataclass

from src.components.logger import logger
from src.components.exception import CustomException
from src.components.data_ingestion import DataLoader, engine


@dataclass
class BookingSplitterConfig:
    """Configuration for time-based booking split."""

    cutoff_date: str = "2022-07-01"
    date_column: str = "booking_date"
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")


class BookingSplitter:
    """Splits enriched bookings into train/test sets on a date cutoff."""

    def __init__(self, config: BookingSplitterConfig = None):
        self.config = config or BookingSplitterConfig()
        os.makedirs(os.path.dirname(self.config.train_data_path), exist_ok=True)

    def split_by_booking_date(self, df: pd.DataFrame) -> tuple[str, str]:
        """
        Split DataFrame on the cutoff date and persist both halves to CSV.

        Parameters
        ----------
        df : pd.DataFrame
            The enriched bookings DataFrame loaded from fct_bookings_enriched.

        Returns
        -------
        train_path, test_path : tuple[str, str]
            File paths to the saved CSVs (consumed by FeaturePreprocessor).
        """
        try:
            # Validate the date column exists — fail loud, fail clear
            if self.config.date_column not in df.columns:
                raise CustomException(
                    Exception(
                        f"Column '{self.config.date_column}' not in DataFrame. Available columns: {list(df.columns)}"
                    )
                )

            # Defensive: ensure date column is datetime (SQL may return strings)
            df = df.copy()
            df[self.config.date_column] = pd.to_datetime(df[self.config.date_column])
            cutoff = pd.to_datetime(self.config.cutoff_date)

            # Time-based split — past becomes train, future becomes test.
            # Mirrors a real forecasting scenario: model learns from historical
            # bookings, then predicts on bookings it has never seen.
            train_df = df[df[self.config.date_column] < cutoff]
            test_df = df[df[self.config.date_column] >= cutoff]

            # Persist to disk (FeaturePreprocessor will read these)
            train_df.to_csv(self.config.train_data_path, index=False)
            test_df.to_csv(self.config.test_data_path, index=False)

            # Log row counts + date ranges for debugging and reproducibility
            logger.info(
                f"Train set: {len(train_df):,} rows | "
                f"{train_df[self.config.date_column].min().date()} to "
                f"{train_df[self.config.date_column].max().date()}"
            )
            logger.info(
                f"Test set:  {len(test_df):,} rows | "
                f"{test_df[self.config.date_column].min().date()} to "
                f"{test_df[self.config.date_column].max().date()}"
            )
            logger.info(f"Cutoff date: {cutoff.date()}")

            return self.config.train_data_path, self.config.test_data_path

        except Exception as e:
            logger.error(f"Booking split failed: {e}")
            raise CustomException(e)


# ─── Run as a script (only when executed directly) ───
if __name__ == "__main__":
    loader = DataLoader(engine)
    df = loader.data_load("fct_bookings_enriched")

    splitter = BookingSplitter()
    splitter.split_by_booking_date(df)
