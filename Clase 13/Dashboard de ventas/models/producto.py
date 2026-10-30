from sqlalchemy import String, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import date
from database.config import Base

class Producto(Base):
    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50))
    descripcion: Mapped[str] = mapped_column(String(200))
    precio_compra: Mapped[Decimal] = mapped_column(Numeric(12,0))
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(12,0))
    stock: Mapped[int] = mapped_column(default=0)
    estado: Mapped[bool] = mapped_column(default=True)
    fecha_registro: Mapped[date] = mapped_column(default=date.today)