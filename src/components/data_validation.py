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
        try:
            self.file = os.path.join("Notebook", file)
            self.df = pd.read_csv(self.file)
            return self.df
        except Exception as e:
            raise CustomException(e)

    def check_nulls(self, critical_columns):
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

                logger.info("Only non-critical NULLs found. Proceeding with ingestion.")
                return True

            else:
                logger.info(f"No NULLs found in {self.file}")
                return True

        except Exception as e:
            logger.error("NULL validation failed.")
            raise CustomException(e)

    def data_convertor(self):

        self.df["check_in_date"] = self.df["check_in_date"].astype("datetime64[ns]")

    def check_data_types(self, schema_):
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

    def check_rules(self, rules):

        try:
            for column, rule in rules.items():

                invalid_mask = (
                    ~self.df[column]
                    .dropna()
                    .isin(rule["values"])
                    .reindex(self.df.index, fill_value=False)
                )
                has_invalid = invalid_mask.any()
                invalid_rows = self.df[invalid_mask]

                if has_invalid:
                    logger.error(f"Rules Mismatch in {column}: Rule should be {rule}")

                    invalid_rows.to_csv(
                        os.path.join(
                            "artifacts", f"{os.path.basename(self.file)}.RULES.csv"
                        ),
                        index=False,
                    )
                    return False

            else:
                logger.info(f"Rules are matching in {self.file}")
                return True
        except Exception as e:
            raise CustomException(e)
