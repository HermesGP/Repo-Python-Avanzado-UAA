from decimal import Decimal
from .productos import validar_producto

class Producto:
    def __init__(self, nombre: str, precio: Decimal, activo: bool = True):
        datos = validar_producto(nombre, precio)
        self.nombre = datos["nombre"]
        self.precio = datos["precio"]
        self.activo = activo