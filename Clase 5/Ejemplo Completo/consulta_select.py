from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine
from models import Producto, Cliente, Pedido, DetallePedido

def consulta_select():
    with Session(engine) as session:

        print("\n=== Productos ===")
        productos = session.execute(select(Producto)).scalars().all()
        for p in productos:
            print(p.id, p.nombre, p.categoria, p.precio)

        print("\n=== Clientes ===")
        clientes = session.execute(select(Cliente)).scalars().all()
        for c in clientes:
            print(c.id, c.nombre, c.email)

        print("\n=== Pedidos ===")
        pedidos = session.execute(select(Pedido)).scalars().all()
        for ped in pedidos:
            print(ped.id, ped.fecha, ped.cliente.nombre)

        print("\n=== Detalles de pedidos ===")
        detalles = session.execute(select(DetallePedido)).scalars().all()
        for d in detalles:
            print(
                d.id,
                "Pedido:", d.pedido_id,
                "Producto:", d.producto.nombre,
                "Cantidad:", d.cantidad,
                "Subtotal:", d.subtotal
            )