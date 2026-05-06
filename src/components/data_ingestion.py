import os
import pandas as pd
from sqlalchemy import create_engine
from src.components.exception import CustomException
from dotenv import load_dotenv
from src.components.logger import logger
from src.components.data_validation import CodeValidation
from src.config import (
    critical_columns,
    rules,
    schema_,
)

load_dotenv()

"""
SQL Ingestion & Loading Module
Handles:
- Secure DB connection
- CSV ingestion into PostgreSQL
- Verification of row counts
- Safe data loading from SQL tables
"""

# -----------------------------
# Database Connection
# -----------------------------

DB_SERVER_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("POSTGRES_DB")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_LOCAL_PORT = os.getenv("POSTGRES_PORT")

logger.info("Initializing PostgreSQL engine...")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER_HOST}:{DB_LOCAL_PORT}/{DB_NAME}"
)

try:
    with engine.connect() as conn:
        logger.info("Database connection successful!")
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    raise CustomException(e)


# -----------------------------
# SQL Ingestion Engine
# -----------------------------


class SQLIngestionEngine:
    """
    Handles ingestion of CSV files into PostgreSQL tables.
    """

    def __init__(self, engine):
        self.engine = engine

    def ingest(self, df: pd.DataFrame, table_name: str, schema: str = None):
        """
        Ingest CSV into PostgreSQL table.
        """
        logger.info(f"Starting ingestion: for table={table_name}")

        try:

            logger.info(f"Data Shape: {df.shape} rows")

            df.to_sql(
                table_name,
                self.engine,
                schema=schema,
                if_exists="replace",
                index=False,
                chunksize=5000,
            )

            logger.info(f"Successfully inserted into {table_name}")

            return self.verify(table_name)

        except Exception as e:
            logger.error(f"Ingestion failed for {table_name}: {e}")
            raise CustomException(e)

    def verify(self, table_name: str):
        """
        Verify row count in the target table.
        """
        logger.info(f"Verifying table: {table_name}")

        try:
            query = f"SELECT COUNT(*) AS row_count FROM {table_name}"
            df = pd.read_sql(query, self.engine)

            logger.info(f"Verification complete. Rows in table: {df.iloc[0, 0]}")

            return df

        except Exception as e:
            logger.error(f"Verification failed for table {table_name}: {e}")
            raise CustomException(e)


# -----------------------------
# Data Loader
# -----------------------------


class DataLoader:
    """
    Loads data from PostgreSQL tables into DataFrames.
    """

    def __init__(self, engine):
        self.engine = engine

    def data_load(self, table_name: str):
        """
        Load entire table into a DataFrame.
        """
        logger.info(f"Loading table: {table_name}")

        try:
            df = pd.read_sql(f"SELECT * FROM {table_name}", self.engine)
            logger.info(f"Loaded {df.shape} from {table_name}")
            return df

        except Exception as e:
            logger.error(f"Failed to load table {table_name}: {e}")
            raise CustomException(e)


# -----------------------------
# Main Execution
# -----------------------------

if __name__ == "__main__":

    validation = CodeValidation()
    engine_obj = SQLIngestionEngine(engine)

    validation.get_file("fact_bookings.csv")
    validation.data_convertor()
    validation.check_nulls(critical_columns)
    validation.check_data_types(schema_)
    validation.check_rules(rules)

    engine_obj.ingest(validation.df, "fact_bookings")
