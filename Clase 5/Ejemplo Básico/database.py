from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

cadena_conexion = "mysql+pymysql://hermes:PythonAvanzado@localhost:3306/tienda"

engine = create_engine(cadena_conexion, echo=True)

class Base(DeclarativeBase):
    pass