"""
booking_splitter.py
───────────────────
Splits enriched bookings DataFrame into training, validation, and test sets
using time‑based cutoffs — preserving temporal order for honest forecasting.

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

    date_column: str
    table_name: str
    train_end: float = 0.60
    val_end: float = 0.80


class BookingSplitter:

    def __init__(self, config: BookingSplitterConfig):
        self.config = config

        self.output_dir = os.path.join(
            "artifacts",
            self.config.table_name,
            self.config.date_column,
        )
        self.train_data_path = os.path.join(self.output_dir, "train.csv")
        self.val_data_path = os.path.join(self.output_dir, "val.csv")
        self.test_data_path = os.path.join(self.output_dir, "test.csv")

        os.makedirs(self.output_dir, exist_ok=True)

    # ---------------------------------------------------------
    # Main splitting logic
    # ---------------------------------------------------------

    """Splits enriched bookings into train/val/test sets based on date cutoffs."""

    def split_by_booking_date(self, df: pd.DataFrame) -> tuple[str, str, str]:
        """
        Split DataFrame into train/val/test sets using time‑based cutoffs.

        Returns
        -------
        train_path, val_path, test_path : tuple[str, str, str]
        """
        try:
            # Validate date column
            if self.config.date_column not in df.columns:
                raise CustomException(
                    Exception(
                        f"Column '{self.config.date_column}' not found. "
                        f"Available columns: {list(df.columns)}"
                    )
                )

            df = df.copy()
            df[self.config.date_column] = pd.to_datetime(df[self.config.date_column])

            # Convert cutoff strings → datetime
            cutoff_train = pd.to_datetime(
                df[self.config.date_column].quantile(self.config.train_end)
            )
            cutoff_val = pd.to_datetime(
                df[self.config.date_column].quantile(self.config.val_end)
            )

            # Time‑based splits
            train_df = df[df[self.config.date_column] <= cutoff_train]

            val_df = df[
                (df[self.config.date_column] > cutoff_train)
                & (df[self.config.date_column] <= cutoff_val)
            ]

            test_df = df[df[self.config.date_column] > cutoff_val]

            # Save to disk
            train_df.to_csv(self.train_data_path, index=False)
            val_df.to_csv(self.val_data_path, index=False)
            test_df.to_csv(self.test_data_path, index=False)

            # Logging for reproducibility
            logger.info(
                f"Train set: {len(train_df):,} rows | "
                f"{train_df[self.config.date_column].min().date()}  "
                f"{train_df[self.config.date_column].max().date()}"
            )

            logger.info(
                f"Val set:   {len(val_df):,} rows | "
                f"{val_df[self.config.date_column].min().date()}  "
                f"{val_df[self.config.date_column].max().date()}"
            )

            logger.info(
                f"Test set:  {len(test_df):,} rows | "
                f"{test_df[self.config.date_column].min().date()}  "
                f"{test_df[self.config.date_column].max().date()}"
            )

            logger.info(
                f"Cutoff dates  Train end: {self.config.train_end} | "
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
    # Rate data split
    rate_cfg = BookingSplitterConfig(
        date_column="check_in_date",
        table_name="fct_bookings_enriched",
    )

    # Demand data split
    demand_cfg = BookingSplitterConfig(
        date_column="check_in_date",
        table_name="mtr_occupancy",
    )

    # Instantiate preprocessor
    active_config = rate_cfg  # < SWITCH BETWEEN the script

    df = loader.data_load(active_config.table_name)

    splitter = BookingSplitter(active_config)

    splitter.split_by_booking_date(df)

    logger.info("Booking split pipeline completed successfully")
