import io
from pathlib import Path
from typing import cast

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("Agg")

import pandas as pd
import seaborn as sns
from matplotlib.figure import Figure
from matplotlib.container import BarContainer
from matplotlib.ticker import FuncFormatter, MaxNLocator

PLOTS_DIR = Path(__file__).resolve().parent.parent / "assets" / "plots"

sns.set_style("dark")
plt.style.use("dark_background")

def _miles(valor, _pos=None):
    return f"{valor:,.0f}".replace(",", ".")


def _nueva_figura():
    # Figure se usa sin pyplot: así es seguro generar gráficos desde varios hilos.
    fig = Figure(figsize=(6.4, 3.8), dpi=110)
    return fig, fig.subplots()


def _a_png(fig: Figure, nombre: str):
    fig.tight_layout()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    datos = buffer.getvalue()
    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    (PLOTS_DIR / f"{nombre}.png").write_bytes(datos)
    return datos


def _sin_datos(ax, titulo: str):
    ax.set_title(titulo)
    ax.text(0.5, 0.5, "Sin datos para mostrar", ha="center", va="center",
            transform=ax.transAxes)
    ax.set_xticks([])
    ax.set_yticks([])


def _rotulos_meses(ax):
    ax.tick_params(axis="x", rotation=45)
    for etiqueta in ax.get_xticklabels():
        etiqueta.set_ha("right")


def grafico_top_productos(df: pd.DataFrame):
    fig, ax = _nueva_figura()
    titulo = "Top 5 productos por ganancia"
    if df.empty:
        _sin_datos(ax, titulo)
    else:
        sns.barplot(data=df, x="ganancia", y="producto", ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel("Ganancia")
        ax.set_ylabel("")
        ax.xaxis.set_major_formatter(FuncFormatter(_miles))
        for contenedor in ax.containers:
            ax.bar_label(cast(BarContainer, contenedor),
                         labels=[_miles(v) for v in df["ganancia"]],
                         padding=3, fontsize=8)
        ax.margins(x=0.15)
    return _a_png(fig, "top_productos")


def grafico_clientes_acumulados(df: pd.DataFrame):
    fig, ax = _nueva_figura()
    titulo = "Clientes acumulados por mes"
    if df.empty:
        _sin_datos(ax, titulo)
    else:
        sns.lineplot(data=df, x="mes", y="clientes_acumulados",
                 marker="o", linewidth=2.2, ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Clientes")
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        _rotulos_meses(ax)
    return _a_png(fig, "clientes_acumulados")


def grafico_histograma_ventas(df: pd.DataFrame):
    fig, ax = _nueva_figura()
    titulo = "Ganancia acumulada según volumen de venta"
    if df.empty:
        _sin_datos(ax, titulo)
    else:
        # weights suma la ganancia de las ventas que caen en cada intervalo.
        sns.histplot(data=df, x="total", weights="ganancia", bins=8,
                      edgecolor="white", ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel("Volumen de la venta (total)")
        ax.set_ylabel("Ganancia acumulada")
        ax.xaxis.set_major_formatter(FuncFormatter(_miles))
        ax.yaxis.set_major_formatter(FuncFormatter(_miles))
        ax.tick_params(axis="x", rotation=30)
    return _a_png(fig, "histograma_ventas")


def grafico_ganancias_mensuales(df: pd.DataFrame):
    fig, ax = _nueva_figura()
    titulo = "Ganancias mes a mes"
    if df.empty:
        _sin_datos(ax, titulo)
    else:
        sns.barplot(data=df, x="mes", y="ganancia", ax=ax)
        ax.set_title(titulo)
        ax.set_xlabel("Mes")
        ax.set_ylabel("Ganancia")
        ax.yaxis.set_major_formatter(FuncFormatter(_miles))
        _rotulos_meses(ax)
    return _a_png(fig, "ganancias_mensuales")
