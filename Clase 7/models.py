from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Numeric, ForeignKey
from datetime import date
from decimal import Decimal
from database import Base

class Producto(Base):
    __tablename__ = "productos"

    id_producto: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(50)) 
    descripcion: Mapped[str] = mapped_column(String(200))
    precio_compra: Mapped[Decimal] = mapped_column(Numeric(12,0))
    precio_venta: Mapped[Decimal] = mapped_column(Numeric(12,0))
    stock: Mapped[int] = mapped_column(default=0)
    estado: Mapped[bool] = mapped_column(default=True)
    fecha_creacion: Mapped[date] = mapped_column()

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

class Venta(Base):
    __tablename__ = "ventas"

    id_venta: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey("clientes.id_cliente"),nullable=False)
    total: Mapped[Decimal] = mapped_column(Numeric(12,0))
    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,0))
    descuento: Mapped[Decimal] = mapped_column(Numeric(12,0))
    iva: Mapped[Decimal] = mapped_column(Numeric(12,0))
    fecha_venta: Mapped[date] = mapped_column(default=date.today)

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