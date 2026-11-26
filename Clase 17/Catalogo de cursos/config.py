import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "clave-desarrollo"
    )

    APP_NAME = os.getenv(
        "APP_NAME",
        "Mi aplicación Flask"
    )

    DEBUG = os.getenv(
        "DEBUG", "False"
    ).lower() == "true"

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///app.db"
    )