from .modelo import Producto

class Carrito:
    def __init__(self):
        self.items = []

    def agregar(self, producto: Producto, cantidad: int = 1):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor que cero")
        if producto.activo is False:
            raise ValueError("El producto no está activo")

        self.items.append({
            "producto": producto,
            "cantidad": cantidad,
        })

    def cantidad_total(self):
        return sum(item["cantidad"] for item in self.items)

    def subtotal(self):
        return sum(item["producto"].precio * item["cantidad"] for item in self.items)

    def vaciar(self):
        self.items.clear()
