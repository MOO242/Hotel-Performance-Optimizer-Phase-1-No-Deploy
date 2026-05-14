import os
import yaml
import pickle
import argparse
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.components.logger import logger
from src.components.exception import CustomException
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from src.components.data_ingestion import DataLoader, engine
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder


@dataclass
class FeaturePreprocessorConfig:
    table_name: str
    date_column: str
    config_path: str


class FeaturePreprocessor:

    def __init__(self, config: FeaturePreprocessorConfig):
        self.config = config

        self.output_dir = os.path.join(
            "artifacts",
            self.config.table_name,
            self.config.date_column,
            "preprocessor.pkl",
        )

        os.makedirs(os.path.dirname(self.output_dir), exist_ok=True)

    def load_schema(self):
        """Helper to load the YAML file."""
        with open(self.config.config_path, "r") as f:

            return yaml.safe_load(f)

    def get_preprocessor(self):

        try:

            logger.info("pre-processing start")
            schema = self.load_schema()
            cols = schema["features"]
            numerical_columns = cols["numerical"]
            nominal_columns = cols["nominal"]
            ordinal_dict = cols.get("ordinal", {})
            if ordinal_dict:
                ordinal_columns = list(cols["ordinal"].keys())
                ordinal_categories = [cols["ordinal"][col] for col in ordinal_columns]
            else:
                ordinal_columns = []
                ordinal_categories = []

            # ─── 2. Define ordinal order (lowest → highest) ───

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

            schema = self.load_schema()
            drop_cols = schema["drop_cols"]
            target_col = schema["model"]["target_column"]

            X_train = train_df.drop(columns=drop_cols, errors="ignore")
            y_train = train_df[target_col]

            X_val = val_df.drop(columns=drop_cols, errors="ignore")
            y_val = val_df[target_col]

            X_test = test_df.drop(columns=drop_cols, errors="ignore")
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

            with open(self.output_dir, "wb") as f:
                pickle.dump(preprocessor, f)

            logger.info(f"Train shape: {train_arr.shape}")
            logger.info(f"Val shape:   {val_arr.shape}")
            logger.info(f"Test shape:  {test_arr.shape}")
            logger.info(f"Preprocessor saved to: {self.output_dir}")

            return train_arr, val_arr, test_arr, self.output_dir

        except Exception as e:
            logger.error(f"Feature preprocessing failed: {e}")
            raise CustomException(e)


# ─── Run as a script (only when executed directly) ───
if __name__ == "__main__":

    logger.info("Starting preprocessing pipeline")
    # Integration of Argument Parser
    parser = argparse.ArgumentParser(description="Hotel Forecast Model Trainer CLI")
    parser.add_argument(
        "--config",
        required=True,
        help="Path to YAML config",
    )
    args = parser.parse_args()

    # Define your date column folder (example: "check_in_date")
    loader = DataLoader(engine)

    # Rate transformation
    active_config = FeaturePreprocessorConfig(
        date_column="check_in_date",
        table_name="fct_bookings_enriched",
        config_path=args.config,
    )

    preprocessor = FeaturePreprocessor(active_config)

    # File paths

    train_path = os.path.join(
        "artifacts", active_config.table_name, active_config.date_column, "train.csv"
    )
    val_path = os.path.join(
        "artifacts", active_config.table_name, active_config.date_column, "val.csv"
    )
    test_path = os.path.join(
        "artifacts", active_config.table_name, active_config.date_column, "test.csv"
    )

    # Run transformation
    train_arr, val_arr, test_arr, preprocessor_path = preprocessor.transform_bookings(
        train_path, val_path, test_path
    )

    logger.info("Preprocessing pipeline completed successfully")

    # Load the artifact to check
    with open(preprocessor_path, "rb") as f:
        preprocessor = pickle.load(f)

    print(f"Preprocessor type: {type(preprocessor).__name__}")
    print(f"Number of transformers: {len(preprocessor.transformers_)}")
    print(f"Feature names (first 10): {preprocessor.get_feature_names_out()[:10]}")
    print(f"Total features: {len(preprocessor.get_feature_names_out())}")
