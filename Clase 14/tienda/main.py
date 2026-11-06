from carrito import Carrito
from precios import calcular_total
from modelo import Producto

def main():
    producto1 = Producto(
        nombre="Teclado Mecánico Ajazz",
        precio=350000
    )
    producto2 = Producto(
        nombre="Mouse Gamer Logitech",
        precio=150000
    )

    carrito = Carrito()
    carrito.agregar(producto1, cantidad=2)
    carrito.agregar(producto2, cantidad=1)

    subtotal = carrito.subtotal()
    total = calcular_total(subtotal, descuento=10, impuesto=10)

    for item in carrito.items:
        print("-" * 20)
        producto = item["producto"]
        print("Producto:", producto.nombre)
        print("Precio:", producto.precio)
        print("Cantidad:", item["cantidad"])
    print("-" * 20)
    print("Subtotal:", subtotal)
    print("Cantidad total:", carrito.cantidad_total())
    print("Total:", total)


if __name__ == "__main__":
    main()