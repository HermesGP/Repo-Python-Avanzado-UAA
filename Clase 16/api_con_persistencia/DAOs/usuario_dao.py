from database.config import SessionLocal
from models.usuario import Usuario

class UsuarioDAO:
    def __init__(self):
        self.session = SessionLocal()

    def agregar(self, usuario: Usuario):
        self.session.add(usuario)
        self.session.commit()

    def obtener(self, usuario_id: int):
        return self.session.query(Usuario).filter(Usuario.id == usuario_id).first()

    def obtener_todos(self):
        return self.session.query(Usuario).all()

    def actualizar(self, usuario: Usuario):
        self.session.merge(usuario)
        self.session.commit()

    def eliminar(self, usuario: Usuario):
        self.session.delete(usuario)
        self.session.commit()

    def buscar_por_nombre(self, nombre: str):
        return self.session.query(Usuario).filter(Usuario.nombre.ilike(f"%{nombre}%")).all()