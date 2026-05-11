import os
import pickle
import pandas as pd
import numpy as np
from dataclasses import dataclass
from scipy import sparse
from src.components.logger import logger
from src.components.exception import CustomException
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder


@dataclass
class FeaturePreprocessorConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class FeaturePreprocessor:

    def __init__(
        self,
        date_column,
    ):
        self.date_column = date_column
        self.config = FeaturePreprocessorConfig()
        self.preprocessor_path = os.path.join(
            "artifacts", date_column, "preprocessor.pkl"
        )
        os.makedirs(os.path.dirname(self.preprocessor_path), exist_ok=True)

    def get_preprocessor(self):

        try:

            logger.info("pre-processing start")
            numerical_columns = [
                "hurdle_rate",
                "number_of_guests",
                "guest_rating_score",
                "number_of_nights",
            ]
            nominal_columns = [
                "city",
                "day_type",
                "room_type",
                "property_id",
                "booking_channel",
            ]

            ordinal_columns = ["season", "room_class", "category"]

            # ─── 2. Define ordinal order (lowest → highest) ───

            ordinal_categories = [
                ["Low Season", "Shoulder", "High Season", "Peak"],  # season
                ["Standard", "Elite", "Premium", "Presidential"],  # room_class
                ["Economy", "Luxury"],  # category
            ]

            num_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),
                    ("scaler", StandardScaler()),
                ]
            )

            nominal_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore")),
                    ("scaler", StandardScaler(with_mean=False)),
                ]
            )

            # ─── 5. Ordinal categorical pipeline ───
            ordinal_pipeline = Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")),
                    (
                        "ordinal_encoder",
                        OrdinalEncoder(
                            categories=ordinal_categories,  # ← the order YOU defined
                            handle_unknown="use_encoded_value",  # don't crash on unseen
                            unknown_value=-1,  # mark unknown as -1
                        ),
                    ),
                    ("scaler", StandardScaler()),  # default (output is dense)
                ]
            )

            preprocessor = ColumnTransformer(
                transformers=[
                    ("num", num_pipeline, numerical_columns),
                    ("nominal", nominal_pipeline, nominal_columns),
                    ("ordinal", ordinal_pipeline, ordinal_columns),
                ],
                remainder="drop",
            )

            return preprocessor

        except Exception as e:
            logger.error("pre-processing failed!")
            raise CustomException(e)

    def transform_bookings(self, train_path, val_path, test_path):

        train_df = pd.read_csv(train_path)
        val_df = pd.read_csv(val_path)
        test_df = pd.read_csv(test_path)

        try:

            for df in [train_df, val_df, test_df]:
                df["property_id"] = df["property_id"].astype(str)

            drop_cols = [
                "booking_id",  # ID
                "property_name",  # Cardinality risk
                "check_in_date",  # Date (split column)
                "checkout_date",  # Date (derivable)
                "booking_date",  # Date
                "room_rate_amount",  # TARGET → becomes y
                "revenue_booked_amount",  # LEAKAGE
                "revenue_realized",  # LEAKAGE
                "booking_status",  # OUTCOME leakage
            ]

            target_col = "room_rate_amount"

            X_train = train_df.drop(columns=drop_cols)
            y_train = train_df[target_col]

            X_val = val_df.drop(columns=drop_cols)
            y_val = val_df[target_col]

            X_test = test_df.drop(columns=drop_cols)
            y_test = test_df[target_col]

            preprocessor = self.get_preprocessor()

            X_train_arr = preprocessor.fit_transform(X_train)
            X_val_arr = preprocessor.transform(X_val)
            X_test_arr = preprocessor.transform(X_test)

            # 6. Handle sparse matrices
            if hasattr(X_train_arr, "toarray"):
                X_train_arr = X_train_arr.toarray()
                X_val_arr = X_val_arr.toarray()
                X_test_arr = X_test_arr.toarray()

            # 7. Combine X + y → final arrays

            train_arr = np.c_[X_train_arr, np.array(y_train)]
            val_arr = np.c_[X_val_arr, np.array(y_val)]
            test_arr = np.c_[X_test_arr, np.array(y_test)]

            with open(self.preprocessor_path, "wb") as f:
                pickle.dump(preprocessor, f)

            logger.info(f"Train shape: {train_arr.shape}")
            logger.info(f"Val shape:   {val_arr.shape}")
            logger.info(f"Test shape:  {test_arr.shape}")
            logger.info(f"Preprocessor saved to: {self.preprocessor_path}")

            return train_arr, val_arr, test_arr, self.preprocessor_path

        except Exception as e:
            logger.error(f"Feature preprocessing failed: {e}")
            raise CustomException(e)


# ─── Run as a script (only when executed directly) ───
if __name__ == "__main__":

    logger.info("Starting preprocessing pipeline")

    # Define your date column folder (example: "check_in_date")
    date_column = "check_in_date"

    # Instantiate preprocessor
    preprocessor = FeaturePreprocessor(date_column)

    # File paths
    train_path = os.path.join("artifacts", date_column, "train.csv")
    val_path = os.path.join("artifacts", date_column, "val.csv")
    test_path = os.path.join("artifacts", date_column, "test.csv")

    # Run transformation
    train_arr, val_arr, test_arr, preprocessor_path = preprocessor.transform_bookings(
        train_path, val_path, test_path
    )

    logger.info("Preprocessing pipeline completed successfully")
