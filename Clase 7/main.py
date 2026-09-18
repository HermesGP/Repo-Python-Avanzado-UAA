from models import Base, Producto, Cliente, Venta, DetalleVenta
from database import engine
from sqlalchemy import text
from sqlalchemy.orm import Session
from query import crear_producto, crear_cliente, crear_venta_con_detalle, consultar_clientes, consultar_producto_por_id, ventas_mayores_a, actualizar_cliente, ventas_con_cliente, total_vendido_por_cliente
from pathlib import Path

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with open(Path(__file__).parent / "insert.sql") as f:
        sql = f.read()
    with Session(engine) as session:
        for sentencia in sql.split(";"):
            if sentencia.strip():
                session.execute(text(sentencia))
        session.commit()
        print("Insert SQL completado")               
    crear_producto()
    crear_cliente()
    crear_venta_con_detalle()
    consultar_clientes()
    consultar_producto_por_id(1)
    ventas_mayores_a(100000)
    actualizar_cliente(1)
    ventas_con_cliente()
    total_vendido_por_cliente()