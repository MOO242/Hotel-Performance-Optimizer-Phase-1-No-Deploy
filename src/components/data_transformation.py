import os
import pickle
import pandas as pd
from dataclasses import dataclass
from src.components.logger import logger
from src.components.exception import CustomException
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.pkl")


class DataTransformation:

    def __init__(
        self,
        features_data,
    ):
        self.features_data = features_data
        self.config = DataTransformationConfig()

    def get_preprocessor(self):

        try:

            logger.info("pre-processing start")
            numerical_columns = [
                "lead_time",
                "cancellation_rate",
                "no_show_rate",
                "platform_cancel_rate",
                "hurdle_rate",
            ]
            nominal_columns = [
                "city",
                "day_type",
                "room_type",
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
                    ("name", num_pipeline, numerical_columns),
                    ("name", nominal_pipeline, nominal_columns),
                    ("name", ordinal_pipeline, ordinal_columns),
                ],
                remainder="drop",
            )

            return preprocessor
        except Exception as e:
            logger.error("pre-processing failed!")
            raise CustomException(e)

    def initiate_data_transformation(self, train_path, test_path):
        # We will fill this together
        pass










