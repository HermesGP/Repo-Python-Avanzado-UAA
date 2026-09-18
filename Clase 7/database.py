from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_engine("mysql+pymysql://hermes:PythonAvanzado@localhost/negocio", echo=True)

class Base(DeclarativeBase):
    pass