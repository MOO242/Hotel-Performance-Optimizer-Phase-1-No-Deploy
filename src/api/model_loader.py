"""
model_loader.py
───────────────
Loads fitted preprocessor + trained model at application startup.
Loaded ONCE, used by every request.
"""

import os
import pickle
from dataclasses import dataclass
from src.components.logger import logger
from src.components.exception import CustomException


@dataclass
class ModelConfig:
    table_name: str
    date_column: str


class ModelLoader:

    def __init__(self, config: ModelConfig):
        self.config = config

        self.path = os.path.join(
            "artifacts",
            self.config.table_name,
            self.config.date_column,
        )

        self.preprocessor_file = self._load_artifact("preprocessor.pkl")
        self.model_file = self._load_artifact("model.pkl")

    def _load_artifact(self, file_name):
        path = os.path.join(self.path, file_name)
        try:
            with open(path, "rb") as f:
                return pickle.load(f)

        except FileNotFoundError as e:
            logger.error(f"Artifact not found.{path}")
            raise CustomException(e)
