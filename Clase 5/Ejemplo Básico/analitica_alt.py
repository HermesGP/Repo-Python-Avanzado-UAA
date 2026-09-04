# analytics.py
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import select
from database import engine
from models import Venta

def reporte_analitico_core():
    # Consulta SQLAlchemy Core
    stmt = select(Venta.categoria, Venta.cantidad, Venta.precio)

    # Pandas convierte directamente la consulta en DataFrame
    df = pd.read_sql(stmt, engine)

    # Cálculo analítico
    df["total"] = df["cantidad"] * df["precio"]
    df_categoria = df.groupby("categoria")["total"].sum().reset_index()

    print(df_categoria)

    # Gráfico
    plt.figure(figsize=(8, 5))
    plt.bar(df_categoria["categoria"], df_categoria["total"], color="skyblue")
    plt.title("Total vendido por categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Millones de Gs")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    reporte_analitico_core()