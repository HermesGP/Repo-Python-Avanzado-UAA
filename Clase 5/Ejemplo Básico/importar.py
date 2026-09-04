import csv
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from database import engine
from models import Venta
from pathlib import Path

ruta_csv = Path(__file__).resolve().with_name("ventas.csv")

with Session(engine) as session:
    with open(ruta_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            venta = Venta(
                fecha=datetime.strptime(row["fecha"], "%Y-%m-%d").date(),
                producto=row["producto"],
                categoria=row["categoria"],
                cantidad=int(row["cantidad"]),
                precio=Decimal(row["precio"])
            )
            session.add(venta)

    session.commit()