from datetime import date

from DAOs.cliente_dao import ClienteDAO
from database.config import SessionLocal
from models.cliente import Cliente


class ClienteService:
    def validar_datos(
        self,
        nombre_completo: str,
        documento: str,
        email: str,
        telefono: str,
        direccion: str,
    ):
        campos = {
            "nombre completo": nombre_completo,
            "documento": documento,
            "correo electrónico": email,
            "teléfono": telefono,
            "dirección": direccion,
        }
        faltantes = [nombre for nombre, valor in campos.items() if not valor.strip()]
        if faltantes:
            raise ValueError(f"Complete los campos obligatorios: {', '.join(faltantes)}.")

    def crear_cliente(
        self,
        nombre_completo: str,
        documento: str,
        email: str,
        telefono: str,
        direccion: str,
        estado: bool,
        fecha_registro: date,
    ):
        self.validar_datos(nombre_completo, documento, email, telefono, direccion)
        cliente = Cliente(
            nombre_completo=nombre_completo.strip(),
            documento=documento.strip(),
            email=email.strip(),
            telefono=telefono.strip(),
            direccion=direccion.strip(),
            estado=estado,
            fecha_registro=fecha_registro,
        )
        with SessionLocal() as db:
            return ClienteDAO(db).crear(cliente)

    def editar_cliente(
        self,
        id_cliente: int,
        nombre_completo: str,
        documento: str,
        email: str,
        telefono: str,
        direccion: str,
        estado: bool,
        fecha_registro: date,
    ):
        self.validar_datos(nombre_completo, documento, email, telefono, direccion)
        with SessionLocal() as db:
            dao = ClienteDAO(db)
            cliente = dao.obtener(id_cliente)
            if not cliente:
                raise ValueError("Cliente no encontrado.")
            cliente.nombre_completo = nombre_completo.strip()
            cliente.documento = documento.strip()
            cliente.email = email.strip()
            cliente.telefono = telefono.strip()
            cliente.direccion = direccion.strip()
            cliente.estado = estado
            cliente.fecha_registro = fecha_registro
            return dao.editar(cliente)

    def buscar(self, texto: str):
        with SessionLocal() as db:
            return ClienteDAO(db).listar(texto)

    def eliminar_cliente(self, id_cliente: int):
        with SessionLocal() as db:
            dao = ClienteDAO(db)
            cliente = dao.obtener(id_cliente)
            if not cliente:
                raise ValueError("Cliente no encontrado.")
            return dao.eliminar(cliente)
