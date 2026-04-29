import pandas as pd
import os

from src.components.exception import CustomException
from src.components.logger import logger


class CodeValidation:
    """
    A utility class for validating raw booking datasets before ingestion.

    This class performs:
    - File loading
    - NULL validation (with critical vs. non‑critical columns)
    - Data type validation against a schema
    - Optional data type conversions

    Designed for use inside an ETL/ELT pipeline before pushing data
    into a warehouse or feature store.
    """

    def get_file(self, file):
        """
        Load a CSV file from the Notebook directory into a pandas DataFrame.

        Args:
            file (str): The filename inside the Notebook/ directory.

        Returns:
            pd.DataFrame: Loaded DataFrame stored in self.df.

        Raises:
            CustomException: If file loading fails.
        """
        try:
            self.file = os.path.join("Notebook", file)
            self.df = pd.read_csv(self.file)
            return self.df
        except Exception as e:
            raise CustomException(e)

    def check_nulls(self, critical_columns):
        """
        Validate NULL values in the dataset.

        - Saves all NULL rows to artifacts/<file>.NULL.csv
        - Flags critical columns that must never contain NULLs
        - Allows non‑critical NULLs to pass

        Args:
            critical_columns (list[str]): Columns that cannot contain NULL values.

        Returns:
            bool:
                True  → No NULLs OR only non‑critical NULLs
                False → Critical NULLs found

        Raises:
            CustomException: If validation fails unexpectedly.
        """
        try:
            logger.info(f"Check NULL's started for {self.file}")

            null_rows_df = self.df[self.df.isnull().any(axis=1)]

            if not null_rows_df.empty:
                # Identify critical NULLs
                critical_nulls = [
                    col
                    for col in critical_columns
                    if col in self.df.columns and self.df[col].isnull().any()
                ]

                cols_null_rows = self.df.columns[self.df.isnull().any()].to_list()
                logger.error(
                    f"{len(null_rows_df)} NULL rows found in {self.file}: {cols_null_rows}"
                )

                # Save NULL rows
                null_rows_df.to_csv(
                    os.path.join(
                        "artifacts", f"{os.path.basename(self.file)}.NULL.csv"
                    ),
                    index=False,
                )
                logger.info(
                    f"NULL rows saved to artifacts/{os.path.basename(self.file)}.NULL.csv"
                )

                if len(critical_nulls) > 0:
                    logger.error(f"CRITICAL: {critical_nulls} contain NULL values!")
                    return False

                logger.info("Only non‑critical NULLs found. Proceeding with ingestion.")
                return True

            else:
                logger.info(f"No NULLs found in {self.file}")
                return True

        except Exception as e:
            logger.error("NULL validation failed.")
            raise CustomException(e)

    def data_convertor(self):
        """
        Convert selected columns into their correct data types.

        Notes:
            - Only check_in_date is currently active.
            - Other conversions are commented out for incremental rollout.
        """
        self.df["check_in_date"] = self.df["check_in_date"].astype("datetime64[ns]")

    def check_data_types(self, schema_):
        """
        Validate each column's data type against a predefined schema.

        Args:
            schema_ (dict): Mapping of column → expected dtype (as pandas dtype string).

        Logs:
            - INFO when a column matches expected dtype
            - ERROR when a mismatch is found

        Raises:
            CustomException: If validation fails unexpectedly.
        """
        try:
            logger.info(f"Check data type started for {self.file}")

            for column, expected in schema_.items():
                if column in self.df.columns:
                    actual = self.df[column].dtypes
                    if actual == expected:
                        logger.info(f"{column}: OK ({actual})")
                    else:
                        logger.error(
                            f"Type Mismatch in {column}: Expected {expected}, got {actual}"
                        )

        except Exception as e:
            raise CustomException(e)


# Columns that can NEVER be null
critical_columns = [
    "booking_id",
    "property_id",
    "booking_date",
    "check_in_date",
    "checkout_date",
    "no_guests",
    "room_category",
    "booking_platform",
    "booking_status",
    "rooms_sold",
    "room_available",
]

# Columns that CAN be null
nullable_columns = [
    "ratings_given",
    "revenue_generated",
    "revenue_realized",
    "room_rate",
    "nights",
]

# schema for data type
schema_ = {
    "booking_id": "str",
    "property_id": "str",
    "booking_date": "datetime64[ns]",
    "check_in_date": "datetime64[ns]",
    "checkout_date": "datetime64[ns]",
    "no_guests": "int64",
    "room_category": "str",
    "booking_platform": "str",
    "booking_status": "str",
    "ratings_given": "Int64",
    "revenue_generated": "float64",
    "revenue_realized": "float64",
    "room_rate": "float64",
    "nights": "Int64",
    "room_available": "int64",
    "rooms_sold": "int64",
}
