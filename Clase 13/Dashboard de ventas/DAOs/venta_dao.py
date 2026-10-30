from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import date
from models.cliente import Cliente
from models.venta import Venta

class VentaDAO:

    def __init__(self, db: Session):
        self.db = db

    def listar(self):
        stmt = select(Venta).order_by(
            Venta.fecha_venta.desc(),
            Venta.id_venta.desc(),
        )
        return self.db.execute(stmt).scalars().all()

    def listar_con_cliente(self, documento: str = "", fecha: date | None = None):
        stmt = (
            select(Venta, Cliente)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
        )
        if documento.strip():
            stmt = stmt.where(Cliente.documento.ilike(f"%{documento.strip()}%"))
        if fecha is not None:
            stmt = stmt.where(Venta.fecha_venta == fecha)
        stmt = stmt.order_by(Venta.fecha_venta.desc(), Venta.id_venta.desc())
        return self.db.execute(stmt).all()

    def buscar_por_documento(self, documento: str):
        stmt = (
            select(Venta)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
            .where(Cliente.documento.ilike(f"%{documento.strip()}%"))
            .order_by(Venta.fecha_venta.desc(), Venta.id_venta.desc())
        )
        return self.db.execute(stmt).scalars().all()

    def buscar_por_fecha(self, fecha: date):
        stmt = (
            select(Venta)
            .where(Venta.fecha_venta == fecha)
            .order_by(Venta.fecha_venta.desc(), Venta.id_venta.desc())
        )
        return self.db.execute(stmt).scalars().all()

    def obtener_con_cliente(self, id_venta: int):
        stmt = (
            select(Venta, Cliente)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
            .where(Venta.id_venta == id_venta)
        )
        return self.db.execute(stmt).one_or_none()

    def crear(self, venta: Venta):
        self.db.add(venta)
        self.db.commit()
        self.db.refresh(venta)
        return venta

    def obtener(self, id_venta: int):
        return self.db.get(Venta, id_venta)

    def editar(self, venta: Venta):
        self.db.commit()
        self.db.refresh(venta)
        return venta
    
    def eliminar(self, venta: Venta):
        self.db.delete(venta)
        self.db.commit()
        return venta