from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
from sqlalchemy import engine

load_dotenv()


DB_SERVER_HOST = os.getenv("POSTGRES_HOST")
DB_NAME = os.getenv("postgres")
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_LOCAL_PORT = os.getenv("POSTGRES_PORT")

engine = create_engine(
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER_HOST}:{DB_LOCAL_PORT}/{DB_NAME}"
)


