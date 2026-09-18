from datetime import date
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database import engine
from models import Producto, Cliente, Venta, DetalleVenta


# 1. Crear un producto
def crear_producto():
    with Session(engine) as session:
        producto = Producto(
            codigo="P001",
            descripcion="Teclado mecanico",
            precio_compra=Decimal("50000"),
            precio_venta=Decimal("80000"),
            stock=20,
            fecha_creacion=date.today(),
        )
        session.add(producto)
        session.commit()
        print(f"Producto creado con id: {producto.id_producto}")


# 2. Crear un cliente
def crear_cliente():
    with Session(engine) as session:
        cliente = Cliente(
            nombre_completo="Juan Perez",
            documento="2345678",
            email="juan.perez@correo.com",
            telefono="+595981234567",
            direccion="Av. Mariscal Lopez 1450, Asuncion",
        )
        session.add(cliente)
        session.commit()
        print(f"Cliente creado con id: {cliente.id_cliente}")


# 3. Crear una venta con su detalle
def crear_venta_con_detalle():
    with Session(engine) as session:
        productos_solicitados = [(1, 1), (2, 2)]
        detalles = []
        productos = {}

        for id_producto, cantidad in productos_solicitados:
            producto = session.get(Producto, id_producto)
            if producto is None:
                raise ValueError(f"Producto no encontrado: {id_producto}")
            if producto.stock < cantidad:
                raise ValueError(
                    f"Stock insuficiente para el producto {producto.codigo}: "
                    f"disponible {producto.stock}, solicitado {cantidad}"
                )

            subtotal = producto.precio_venta * cantidad
            detalles.append(
                DetalleVenta(
                    id_producto=id_producto,
                    cantidad=cantidad,
                    precio_unitario=producto.precio_venta,
                    subtotal=subtotal,
                    descuento=Decimal("0"),
                    iva=subtotal * Decimal("0.1"),
                )
            )
            productos[id_producto] = producto

        subtotal = sum((detalle.subtotal for detalle in detalles), Decimal("0"))
        iva = sum((detalle.iva for detalle in detalles), Decimal("0"))
        descuento = sum((detalle.descuento for detalle in detalles), Decimal("0"))

        venta = Venta(
            id_cliente=1,
            subtotal=subtotal,
            descuento=descuento,
            iva=iva,
            total=subtotal - descuento + iva,
        )
        session.add(venta)
        session.flush()  # para obtener venta.id_venta antes del commit

        for detalle in detalles:
            detalle.id_venta = venta.id_venta
        session.add_all(detalles)

        subtotal_guardado = sum((detalle.subtotal for detalle in detalles), Decimal("0"))
        iva_guardado = sum((detalle.iva for detalle in detalles), Decimal("0"))
        if venta.subtotal != subtotal_guardado or venta.iva != iva_guardado:
            raise ValueError("Los totales de la venta no coinciden con sus detalles")

        for detalle in detalles:
            productos[detalle.id_producto].stock -= detalle.cantidad

        session.commit()
        print(
            f"Venta creada con id: {venta.id_venta}, "
            f"subtotal: {venta.subtotal}, iva: {venta.iva}, total: {venta.total}"
        )


# 4. Consultar todos los clientes
def consultar_clientes():
    with Session(engine) as session:
        clientes = session.execute(select(Cliente)).scalars().all()
        for cliente in clientes:
            print(cliente.id_cliente, cliente.nombre_completo, cliente.email)


# 5. Consultar producto por id
def consultar_producto_por_id(id_producto: int):
    with Session(engine) as session:
        producto = session.get(Producto, id_producto)
        if producto:
            print(producto.id_producto, producto.descripcion, producto.precio_venta)
        else:
            print("Producto no encontrado")


# 6. Filtrar ventas con total superior a 100000
def ventas_mayores_a(monto: int = 100000):
    with Session(engine) as session:
        ventas = session.execute(
            select(Venta.id_venta, Cliente.nombre_completo, Venta.total)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
            .where(Venta.total > monto)
            .order_by(Venta.total.asc())
        ).all()
        for id_venta, nombre, total in ventas:
            print(id_venta, nombre, total)


# 7. Actualizar un cliente
def actualizar_cliente(id_cliente: int):
    with Session(engine) as session:
        cliente = session.get(Cliente, id_cliente)
        if cliente:
            cliente.telefono = "+595981234567"
            cliente.direccion = "Tte. Cnel. Martínez 144, Asuncion"
            session.commit()
            print("Cliente actualizado")
        else:
            print("Cliente no encontrado")


# 8. Consulta con JOIN: ventas con el nombre del cliente
def ventas_con_cliente():
    with Session(engine) as session:
        resultados = session.execute(
            select(Venta.id_venta, Venta.total, Cliente.nombre_completo)
            .join(Cliente, Venta.id_cliente == Cliente.id_cliente)
        ).all()
        for id_venta, total, nombre in resultados:
            print(id_venta, nombre, total)


# 9. Consulta con GROUP BY: total vendido por cliente
def total_vendido_por_cliente():
    with Session(engine) as session:
        total_vendido = func.sum(Venta.total).label("total_vendido")
        resultados = session.execute(
            select(Cliente.nombre_completo, total_vendido)
            .join(Venta, Venta.id_cliente == Cliente.id_cliente)
            .group_by(Cliente.id_cliente)
            .order_by(total_vendido.asc())
        ).all()
        for nombre, total_vendido in resultados:
            print(nombre, total_vendido)

    

