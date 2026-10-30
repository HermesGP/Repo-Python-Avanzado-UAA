import json
import os
import sys
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

if getattr(sys, "frozen", False):
    app_dir = Path(sys.executable).resolve().parent
else:
    app_dir = Path(__file__).resolve().parent.parent

config_path = app_dir / "config.json"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL and config_path.is_file():
    with config_path.open(encoding="utf-8") as config_file:
        settings = json.load(config_file)
    if not isinstance(settings, dict):
        raise ValueError(f"El archivo {config_path} debe contener un objeto JSON.")
    DATABASE_URL = settings.get("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError(
        f"Configura DATABASE_URL en el archivo de configuración config.json en {config_path} "
        "o como variable de entorno."
    )

engine = create_engine(DATABASE_URL, echo=False)


class Base(DeclarativeBase):
    pass


SessionLocal = sessionmaker(bind=engine)