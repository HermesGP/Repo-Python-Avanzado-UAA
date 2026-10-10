from sqlalchemy.orm import Session
from sqlalchemy import select
from models.producto import Producto

class ProductoDAO:

    def __init__(self, db: Session):
        self.db = db

    def listar(self, filtro: str = ""):
        stmt = select(Producto)
        if filtro:
            stmt = stmt.where(Producto.descripcion.ilike(f"%{filtro}%"))
        return self.db.execute(stmt).scalars().all()

    def crear(self, producto: Producto):
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def obtener(self, id_producto: int):
        return self.db.get(Producto, id_producto)

    def editar(self, producto: Producto):
        self.db.commit()
        self.db.refresh(producto)
        return producto
    
    def eliminar(self, producto: Producto):
        self.db.delete(producto)
        self.db.commit()
        return producto