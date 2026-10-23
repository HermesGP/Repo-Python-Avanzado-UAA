from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import date
from database.config import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_completo: Mapped[str] = mapped_column(String(200))
    documento: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
    telefono: Mapped[str] = mapped_column(String(20))
    direccion: Mapped[str] = mapped_column(String(200))
    estado: Mapped[bool] = mapped_column(default=True)
    fecha_registro: Mapped[date] = mapped_column(default=date.today)