from sqlalchemy.orm import Session
from database import engine
from models import Producto, Cliente, Pedido, DetallePedido
from datetime import date
from decimal import Decimal

def consulta_insert():
    with Session(engine) as session:

        # Productos
        p1 = Producto(nombre="Monitor LED 24 pulgadas", categoria="Pantallas", precio=Decimal("1450000"))
        p2 = Producto(nombre="Teclado mecánico RGB", categoria="Perifericos", precio=Decimal("650000"))
        p3 = Producto(nombre="Auriculares USB", categoria="Audio", precio=Decimal("420000"))

        session.add_all([p1, p2, p3])
        session.commit()

        # Clientes
        c1 = Cliente(nombre="Juan Pérez", email="juan@example.com")
        c2 = Cliente(nombre="Ana López", email="ana@example.com")

        session.add_all([c1, c2])
        session.commit()

        # Pedido de Juan
        pedido1 = Pedido(fecha=date(2025, 1, 10), cliente_id=c1.id)
        session.add(pedido1)
        session.commit()

        # Detalles del pedido
        d1 = DetallePedido(
            pedido_id=pedido1.id,
            producto_id=p1.id,
            cantidad=1,
            subtotal=p1.precio * 1
        )
        d2 = DetallePedido(
            pedido_id=pedido1.id,
            producto_id=p2.id,
            cantidad=2,
            subtotal=p2.precio * 2
        )

        session.add_all([d1, d2])
        session.commit()