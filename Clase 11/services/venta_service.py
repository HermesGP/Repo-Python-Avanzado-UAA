from datetime import date
from decimal import Decimal, ROUND_HALF_UP

from sqlalchemy import select

from DAOs.cliente_dao import ClienteDAO
from DAOs.detalle_venta_dao import DetalleVentaDAO
from DAOs.producto_dao import ProductoDAO
from DAOs.venta_dao import VentaDAO
from database.config import SessionLocal
from models.cliente import Cliente
from models.detalle_venta import DetalleVenta
from models.producto import Producto
from models.venta import Venta

IVA_TASA = Decimal("0.10")


def redondear_monto(monto: Decimal) -> Decimal:
    return monto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)


def calcular_iva(subtotal: Decimal) -> Decimal:
    return redondear_monto(subtotal * IVA_TASA)


class VentaService:
    def listar(self, documento: str = "", fecha: date | None = None):
        with SessionLocal() as db:
            return VentaDAO(db).listar_con_cliente(documento, fecha)

    def buscar_por_documento(self, documento: str):
        with SessionLocal() as db:
            return VentaDAO(db).buscar_por_documento(documento)

    def buscar_por_fecha(self, fecha: date):
        with SessionLocal() as db:
            return VentaDAO(db).buscar_por_fecha(fecha)

    def obtener_detalle(self, id_venta: int):
        with SessionLocal() as db:
            encabezado = VentaDAO(db).obtener_con_cliente(id_venta)
            if encabezado is None:
                raise ValueError("Venta no encontrada.")
            detalles = DetalleVentaDAO(db).listar_por_venta(id_venta)
            return encabezado[0], encabezado[1], detalles

    def obtener_opciones(self):
        with SessionLocal() as db:
            clientes = [
                cliente
                for cliente in ClienteDAO(db).listar()
                if cliente.estado
            ]
            productos = [
                producto
                for producto in ProductoDAO(db).listar()
                if producto.estado and producto.stock > 0
            ]
            return clientes, productos

    def crear_venta(
        self,
        id_cliente: int,
        lineas: list[tuple[int, int]],
        fecha_venta: date | None = None,
    ) -> int:
        if not lineas:
            raise ValueError("Agregue al menos un producto a la venta.")

        cantidades: dict[int, int] = {}
        for id_producto, cantidad in lineas:
            if cantidad <= 0:
                raise ValueError("La cantidad de cada producto debe ser mayor que cero.")
            cantidades[id_producto] = cantidades.get(id_producto, 0) + cantidad

        with SessionLocal.begin() as db:
            cliente = db.get(Cliente, id_cliente)
            if cliente is None or not cliente.estado:
                raise ValueError("Seleccione un cliente activo.")

            productos: dict[int, Producto] = {}
            detalles: list[DetalleVenta] = []
            for id_producto, cantidad in cantidades.items():
                producto = db.execute(
                    select(Producto)
                    .where(Producto.id_producto == id_producto)
                    .with_for_update()
                ).scalar_one_or_none()
                if producto is None or not producto.estado:
                    raise ValueError(f"El producto con ID {id_producto} no está disponible.")
                if producto.stock < cantidad:
                    raise ValueError(
                        f"Stock insuficiente para {producto.descripcion}: "
                        f"disponible {producto.stock}, solicitado {cantidad}."
                    )

                subtotal_linea = producto.precio_venta * cantidad
                detalles.append(
                    DetalleVenta(
                        id_producto=id_producto,
                        cantidad=cantidad,
                        precio_unitario=producto.precio_venta,
                        subtotal=subtotal_linea,
                        descuento=Decimal("0"),
                        iva=calcular_iva(subtotal_linea),
                    )
                )
                productos[id_producto] = producto

            subtotal = sum(
                (detalle.subtotal for detalle in detalles),
                Decimal("0"),
            )
            descuento = sum(
                (detalle.descuento for detalle in detalles),
                Decimal("0"),
            )
            iva = sum((detalle.iva for detalle in detalles), Decimal("0"))
            venta = Venta(
                id_cliente=id_cliente,
                fecha_venta=fecha_venta or date.today(),
                subtotal=subtotal,
                descuento=descuento,
                iva=iva,
                total=subtotal - descuento + iva,
            )
            db.add(venta)
            db.flush()

            for detalle in detalles:
                detalle.id_venta = venta.id_venta
                db.add(detalle)
                productos[detalle.id_producto].stock -= detalle.cantidad

            id_venta = venta.id_venta

        return id_venta
