from sqlalchemy.orm import Session
from sqlalchemy import select
from database import engine
from models import Venta
from decimal import Decimal

with Session(engine) as session:
    #Leyendo todos los datos
    ventas = session.execute(select(Venta)).scalars().all()
    print("Ventas:")
    for venta in ventas:
        print(venta)

    #Creando una nueva venta
    nueva = Venta(
            fecha="2025-01-10",
            producto="Mouse gamer",
            categoria="Perifericos",
            cantidad=2,
            precio=Decimal("300000")
        )
    session.add(nueva)
    session.commit()

    #Actualizando una venta
    venta_cambiar = session.get(Venta, 1)
    if venta_cambiar:
        venta_cambiar.cantidad = 10
        session.commit()

    #Borrando una venta
    venta_borrar = session.get(Venta, 2)
    if venta_borrar:
        session.delete(venta_borrar)
        session.commit()

    #Leyendo de nuevo para ver los cambios
    ventas_nuevas = session.execute(select(Venta)).scalars().all()
    print("Ventas Cambiadas:")
    for venta in ventas_nuevas:
        print(venta)
