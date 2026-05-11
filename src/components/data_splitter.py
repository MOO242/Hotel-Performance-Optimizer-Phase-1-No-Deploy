"""
booking_splitter.py
───────────────────
Splits enriched bookings DataFrame into training, validation, and test sets
using time‑based cutoffs — preserving temporal order for honest forecasting.

Business rationale:
    Hotel demand is time‑series. Random splits would let the model "peek
    into the future" during training, inflating performance metrics.
    A time‑based split simulates real production: train on historical
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
    """Configuration for time‑based booking split."""

    train_end: str = "2022-06-21"  # 60%
    val_end: str = "2022-07-08"  # 20%


class BookingSplitter:
    """Splits enriched bookings into train/val/test sets based on date cutoffs."""

    def __init__(self, date_column: str):
        self.date_column = date_column
        self.config = BookingSplitterConfig()

        self.output_dir = os.path.join("artifacts", self.date_column)
        self.train_data_path = os.path.join(self.output_dir, "train.csv")
        self.val_data_path = os.path.join(self.output_dir, "val.csv")
        self.test_data_path = os.path.join(self.output_dir, "test.csv")

        os.makedirs(self.output_dir, exist_ok=True)

    # ---------------------------------------------------------
    # Quantile helper (exploratory only)
    # ---------------------------------------------------------
    def print_quantile_cutoffs(self, df: pd.DataFrame):
        """Print quantile‑based cutoffs for exploratory analysis."""
        df = df.copy()
        df[self.date_column] = pd.to_datetime(df[self.date_column])

        print(f"20% cutoff: {df[self.date_column].quantile(0.20).date()}")
        print(f"40% cutoff: {df[self.date_column].quantile(0.40).date()}")
        print(f"60% cutoff: {df[self.date_column].quantile(0.60).date()}")
        print(f"80% cutoff: {df[self.date_column].quantile(0.80).date()}")

    # ---------------------------------------------------------
    # Main splitting logic
    # ---------------------------------------------------------
    def split_by_booking_date(self, df: pd.DataFrame) -> tuple[str, str, str]:
        """
        Split DataFrame into train/val/test sets using time‑based cutoffs.

        Returns
        -------
        train_path, val_path, test_path : tuple[str, str, str]
        """
        try:
            # Validate date column
            if self.date_column not in df.columns:
                raise CustomException(
                    Exception(
                        f"Column '{self.date_column}' not found. "
                        f"Available columns: {list(df.columns)}"
                    )
                )

            df = df.copy()
            df[self.date_column] = pd.to_datetime(df[self.date_column])

            # Convert cutoff strings → datetime
            cutoff_train = pd.to_datetime(self.config.train_end)
            cutoff_val = pd.to_datetime(self.config.val_end)

            # Time‑based splits
            train_df = df[df[self.date_column] <= cutoff_train]

            val_df = df[
                (df[self.date_column] > cutoff_train)
                & (df[self.date_column] <= cutoff_val)
            ]

            test_df = df[df[self.date_column] > cutoff_val]

            # Save to disk
            train_df.to_csv(self.train_data_path, index=False)
            val_df.to_csv(self.val_data_path, index=False)
            test_df.to_csv(self.test_data_path, index=False)

            # Logging for reproducibility
            logger.info(
                f"Train set: {len(train_df):,} rows | "
                f"{train_df[self.date_column].min().date()} → "
                f"{train_df[self.date_column].max().date()}"
            )

            logger.info(
                f"Val set:   {len(val_df):,} rows | "
                f"{val_df[self.date_column].min().date()} → "
                f"{val_df[self.date_column].max().date()}"
            )

            logger.info(
                f"Test set:  {len(test_df):,} rows | "
                f"{test_df[self.date_column].min().date()} → "
                f"{test_df[self.date_column].max().date()}"
            )

            logger.info(
                f"Cutoff dates → Train end: {self.config.train_end} | "
                f"Val end: {self.config.val_end}"
            )

            return self.train_data_path, self.val_data_path, self.test_data_path

        except Exception as e:
            logger.error(f"Booking split failed: {e}")
            raise CustomException(e)


# ---------------------------------------------------------
# Script execution
# ---------------------------------------------------------
if __name__ == "__main__":
    logger.info("Starting booking split pipeline")

    loader = DataLoader(engine)
    df = loader.data_load("fct_bookings_enriched")

    splitter = BookingSplitter("check_in_date")

    logger.info("Quantile cutoffs (exploratory only):")
    splitter.print_quantile_cutoffs(df)

    splitter.split_by_booking_date(df)

    logger.info("Booking split pipeline completed successfully")
