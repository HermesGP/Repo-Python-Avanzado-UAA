import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from database import engine
from models import Venta


with Session(engine) as session:

    stmt = (
        select(
            Venta.categoria,
            func.sum(Venta.cantidad * Venta.precio).label("total")
        )
        .group_by(Venta.categoria)
    )

    resultados = session.execute(stmt).all()

    df = pd.DataFrame(resultados, columns=["categoria", "total"])
    print(df)

    plt.figure(figsize=(8, 5))
    plt.bar(df["categoria"], df["total"], color="skyblue")
    plt.title("Total vendido por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Millones de Gs")
    plt.tight_layout()
    plt.show()