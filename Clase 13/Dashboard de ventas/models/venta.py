from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from decimal import Decimal
from datetime import date
from database.config import Base

class Venta(Base):
    __tablename__ = "ventas"

    id_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"),nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12,0))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,0))
    descuento: Mapped[Decimal] = mapped_column(Numeric(12,0))
    iva: Mapped[Decimal] = mapped_column(Numeric(12,0))
    fecha_venta: Mapped[date] = mapped_column(default=date.today)