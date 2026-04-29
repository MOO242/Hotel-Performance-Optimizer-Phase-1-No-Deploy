import pandas as pd
import os

from sqlalchemy import false
from src.components.exception import CustomException
from src.components.logger import logger


class CodeValidation:

    def get_file(self, file):
        self.file = os.path.join("Notebook", file)
        self.df = pd.read_csv(self.file)
        return self.df

    def check_nulls(self, critical_columns):

        try:
            logger.info(f"Check NULL's started for {self.file}")

            null_rows_df = self.df[self.df.isnull().any(axis=1)]

            if not null_rows_df.empty:
                critical_nulls = [
                    col
                    for col in critical_columns
                    if col in self.df.columns and self.df[col].isnull().any()
                ]

                cols_null_rows = self.df.columns[self.df.isnull().any()].to_list()
                logger.error(
                    f"{len(null_rows_df)} There is NULL in {self.file} {cols_null_rows}"
                )

                null_rows_df.to_csv(
                    os.path.join(
                        "artifacts", f"{os.path.basename(self.file)}.NULL.csv"
                    ),
                    index=False,
                )
                logger.info(
                    f"The NULL's rows saved to artifacts/NULL.csv for {self.file}"
                )

                if len(critical_nulls) > 0:
                    logger.error(f"CRITICAL: {critical_nulls} has NULLs!")
                    return False
                logger.info("Only minor NULLs found. Proceeding with ingestion.")
                return True
            else:
                logger.info(f"Null check passed - no nulls found in {self.file}")
                return True

        except Exception as e:
            logger.error(f"There is NULL")
            raise CustomException(e)

    def data_convertor(self):

        # self.df["booking_date"] = self.df["booking_date"].astype("datetime64[ns]")
        self.df["check_in_date"] = self.df["check_in_date"].astype("datetime64[ns]")
        # self.df["checkout_date"] = self.df["checkout_date"].astype("datetime64[ns]")
        # self.df["ratings_given"] = self.df["ratings_given"].astype("Int64")
        # self.df["nights"] = self.df["nights"].astype("Int64")
        # self.df["revenue_generated"] = self.df["revenue_generated"].astype("float64")
        # self.df["revenue_realized"] = self.df["revenue_realized"].astype("float64")

    def check_data_types(self, schema_):

        try:
            logger.info(f"Check data type started for {self.file}")

            for column, expected in schema_.items():
                if column in self.df.columns:
                    d_type = self.df[column].dtypes
                    if d_type == expected:
                        logger.info(f"Yes for {self.df[column].dtypes}")
                    else:
                        logger.error(
                            f"Type Mismatch in {column}: Excepted:{expected}:I got {self.df[column].dtypes}"
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
