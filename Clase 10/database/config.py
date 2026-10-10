import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError(
        "Falta la variable de entorno DATABASE_URL, "
        "por ejemplo: mysql+pymysql://usuario:password@localhost/negocio"
    )

engine = create_engine(DATABASE_URL, echo=False)

class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind=engine)
