import pandas as pd

from src.components.logger import logger
from src.components.exception import CustomException

from src.components.data_ingestion import DataLoader, engine

from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()

data = DataLoader(engine)


class DataTransformation:

    def __init__(self, features_data, kpi):
        self.features_data = features_data
        self.kpi = kpi

    def label_encode(self, column, mapping):
        try:

            logger.info(f"Label encoding started for {column}")

            self.features_data[column + "_le"] = self.features_data[column].map(mapping)

            logger.info(f"Label encoding complete for {column}")
            return self.features_data

        except Exception as e:
            raise CustomException(e)

    def one_hot_encode(self, column):
        try:
            logger.info(f"One-Hot-encoding started for {column}")
            self.features_data = pd.get_dummies(self.features_data, columns=OneHot)

            logger.info(f"one-Hot encoding complete for {column}")
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

            logger.info(f"Binary encode encoding complete for {binary_map}")
            return self.features_data

        except Exception as e:
            raise CustomException(e)


features_data = data.data_load("features_enriched")
kpi = data.data_load("mtr_occupancy")

season_map = {"Low Season": 0, "High Season": 1, "Peak Season": 2}

room_map = {"Standard": 0, "Elite": 1, "Premium": 2, "Presidential": 3}


OneHot = ["city", "booking_channel", "booking_status"]
binary_map = {"day_type": "weekeday", "category": "Luxury"}


dataTransformation = DataTransformation(features_data, kpi)
features_data = dataTransformation.label_encode("season", season_map)
features_data = dataTransformation.label_encode("room_class", room_map)
features_data = dataTransformation.one_hot_encode(OneHot)
features_data = dataTransformation.binary_encode(binary_map)
# Add this to verify encoding worked:
print(
    dataTransformation.features_data[
        [
            "season",
            "season_le",
            "room_class",
            "room_class_le",
            "day_type",
            "day_type_bin",
        ]
    ].head()
)
