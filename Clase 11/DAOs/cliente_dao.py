from sqlalchemy.orm import Session
from sqlalchemy import or_, select
from models.cliente import Cliente

class ClienteDAO:

    def __init__(self, db: Session):
        self.db = db

    def listar(self, filtro: str = ""):
        stmt = select(Cliente)
        termino = filtro.strip()
        if termino:
            patron = f"%{termino}%"
            stmt = stmt.where(
                or_(
                    Cliente.nombre_completo.ilike(patron),
                    Cliente.documento.ilike(patron),
                    Cliente.email.ilike(patron),
                    Cliente.telefono.ilike(patron),
                    Cliente.direccion.ilike(patron),
                )
            )
        stmt = stmt.order_by(Cliente.nombre_completo)
        return self.db.execute(stmt).scalars().all()

    def crear(self, cliente: Cliente):
        self.db.add(cliente)
        self.db.commit()
        self.db.refresh(cliente)
        return cliente

    def obtener(self, id_cliente: int):
        return self.db.get(Cliente, id_cliente)

    def editar(self, cliente: Cliente):
        self.db.commit()
        self.db.refresh(cliente)
        return cliente
    
    def eliminar(self, cliente: Cliente):
        self.db.delete(cliente)
        self.db.commit()
        return cliente