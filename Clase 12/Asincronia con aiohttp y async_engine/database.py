from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "mysql+asyncmy://hermes:PythonAvanzado@localhost/placeholder"

class Base(DeclarativeBase):
    pass

engine = create_async_engine(DATABASE_URL, echo=True)

SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False
)
