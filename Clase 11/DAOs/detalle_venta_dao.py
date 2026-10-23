from sqlalchemy.orm import Session
from sqlalchemy import select
from models.producto import Producto
from models.detalle_venta import DetalleVenta

class DetalleVentaDAO:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        stmt = select(DetalleVenta)
        return self.db.execute(stmt).scalars().all()

    def listar_por_venta(self, id_venta: int):
        stmt = (
            select(DetalleVenta, Producto)
            .join(Producto, DetalleVenta.id_producto == Producto.id_producto)
            .where(DetalleVenta.id_venta == id_venta)
            .order_by(DetalleVenta.id_detalle)
        )
        return self.db.execute(stmt).all()

    def crear(self, detalle_venta: DetalleVenta):
        self.db.add(detalle_venta)
        self.db.commit()
        self.db.refresh(detalle_venta)
        return detalle_venta

    def obtener(self, id_detalle: int):
        return self.db.get(DetalleVenta, id_detalle)

    def editar(self, detalle_venta: DetalleVenta):
        self.db.commit()
        self.db.refresh(detalle_venta)
        return detalle_venta
    
    def eliminar(self, detalle_venta: DetalleVenta):
        self.db.delete(detalle_venta)
        self.db.commit()
        return detalle_venta