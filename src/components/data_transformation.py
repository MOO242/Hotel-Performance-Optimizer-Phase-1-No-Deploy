import os
import pickle
import pandas as pd
from dataclasses import dataclass
from src.components.logger import logger
from src.components.exception import CustomException


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
        self.preprocessor = {}

    def label_encode(self, column, mapping):
        try:

            logger.info(f"Label encoding started for {column}")

            self.features_data[column + "_le"] = self.features_data[column].map(mapping)

            self.preprocessor[column] = mapping

            logger.info(f"Label encoding complete for {column}")
            return self.features_data

        except Exception as e:
            raise CustomException(e)

    def one_hot_encode(self, columns):
        try:

            logger.info(f"One-Hot-encoding started for {columns}")

            self.features_data = pd.get_dummies(
                self.features_data, columns=columns, dtype=int
            )

            self.preprocessor["one_hot_columns"] = columns

            logger.info(f"one-Hot encoding complete for {columns}")
            return self.features_data

        except Exception as e:
            raise CustomException(e)

    def binary_encode(self, binary_map):
        try:
            logger.info(f"binary encoding started for {list(binary_map.keys())}")
            for column, positive_value in binary_map.items():

                self.features_data[column + "_bin"] = (
                    self.features_data[column] == positive_value
                ).astype(int)

            self.preprocessor["binary_map"] = binary_map
            logger.info(f"Binary encode encoding complete for {binary_map}")
            return self.features_data

        except Exception as e:
            raise CustomException(e)

    def save_preprocessor(self):
        try:
            logger.info("Saving preprocessor...")
            os.makedirs("artifacts", exist_ok=True)

            with open(self.config.preprocessor_obj_file_path, "wb") as f:

                pickle.dump(self.preprocessor, f)
            logger.info("Preprocessor saved!")
            """ Test if the data is correct"""
            with open("artifacts/preprocessor.pkl", "rb") as f:
                preprocessor = pickle.load(f)
                print(preprocessor)
        except Exception as e:
            raise CustomException(e)
