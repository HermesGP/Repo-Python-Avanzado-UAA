import pandas as pd
from sqlalchemy import func, select

from database.config import SessionLocal
from models.cliente import Cliente
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from models.venta import Venta

# Ganancia de una línea: lo vendido (sin IVA) menos el costo de los productos.
GANANCIA_LINEA = (
    DetalleVenta.subtotal
    - DetalleVenta.descuento
    - Producto.precio_compra * DetalleVenta.cantidad
)


def _a_dataframe(filas, columnas: list[str]) -> pd.DataFrame:
    df = pd.DataFrame(filas, columns=columnas)
    for columna in columnas:
        if df[columna].dtype == object and columna not in ("producto", "fecha"):
            df[columna] = df[columna].astype(float)
    return df


class DashboardService:
    def top_productos_ganancia(self, limite: int = 5):
        stmt = (
            select(
                Producto.descripcion.label("producto"),
                func.sum(GANANCIA_LINEA).label("ganancia"),
            )
            .join(DetalleVenta, DetalleVenta.id_producto == Producto.id_producto)
            .group_by(Producto.id_producto, Producto.descripcion)
            .order_by(func.sum(GANANCIA_LINEA).desc())
            .limit(limite)
        )
        with SessionLocal() as db:
            filas = db.execute(stmt).all()
        return _a_dataframe(filas, ["producto", "ganancia"])

    def clientes_acumulados_por_mes(self):
        stmt = select(Cliente.fecha_registro.label("fecha")).where(
            Cliente.fecha_registro.is_not(None)
        )
        with SessionLocal() as db:
            filas = db.execute(stmt).all()
        df = pd.DataFrame(filas, columns=["fecha"])
        if df.empty:
            return pd.DataFrame(columns=["mes", "clientes_acumulados"])
        df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M")
        por_mes = df.groupby("mes").size()
        # Se rellenan los meses sin altas para que la línea sea continua.
        meses = pd.period_range(por_mes.index.min(), por_mes.index.max(), freq="M")
        acumulado = por_mes.reindex(meses, fill_value=0).cumsum()
        return pd.DataFrame(
            {
                "mes": acumulado.index.astype(str),
                "clientes_acumulados": acumulado.values,
            }
        )
    def _ganancia_por_venta(self):
        stmt = (
            select(
                Venta.id_venta,
                Venta.fecha_venta.label("fecha"),
                Venta.total,
                func.sum(GANANCIA_LINEA).label("ganancia"),
            )
            .join(DetalleVenta, DetalleVenta.id_venta == Venta.id_venta)
            .join(Producto, Producto.id_producto == DetalleVenta.id_producto)
            .group_by(Venta.id_venta, Venta.fecha_venta, Venta.total)
        )
        with SessionLocal() as db:
            filas = db.execute(stmt).all()
        return _a_dataframe(filas, ["id_venta", "fecha", "total", "ganancia"])

    def ventas_por_volumen(self):
        df = self._ganancia_por_venta()
        return df[["total", "ganancia"]]
    
    def ganancias_por_mes(self):
        df = self._ganancia_por_venta()
        if df.empty:
            return pd.DataFrame(columns=["mes", "ganancia"])
        df["mes"] = pd.to_datetime(df["fecha"]).dt.to_period("M")
        por_mes = df.groupby("mes")["ganancia"].sum()
        meses = pd.period_range(por_mes.index.min(), por_mes.index.max(), freq="M")
        por_mes = por_mes.reindex(meses, fill_value=0.0)
        return pd.DataFrame(
            {"mes": por_mes.index.astype(str), "ganancia": por_mes.values}
        )
