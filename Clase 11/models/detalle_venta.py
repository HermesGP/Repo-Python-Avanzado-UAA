from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey
from datetime import date
from decimal import Decimal
from database.config import Base

class DetalleVenta(Base):
    __tablename__ = "detalle_ventas"

    id_detalle: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_venta: Mapped[int] = mapped_column(ForeignKey("ventas.id_venta"), nullable=False)
    id_producto: Mapped[int] = mapped_column(ForeignKey("productos.id_producto"), nullable=False)
    cantidad: Mapped[int] = mapped_column(default=1)
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(12,0))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,0))
    descuento: Mapped[Decimal] = mapped_column(Numeric(12,0))
    iva: Mapped[Decimal] = mapped_column(Numeric(12,0))