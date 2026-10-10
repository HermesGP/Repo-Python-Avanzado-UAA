from database.config import SessionLocal
from DAOs.producto_dao import ProductoDAO
from models.producto import Producto
from decimal import Decimal
from datetime import date

class ProductoService:

    # -----------------------------
    # VALIDACIONES DE NEGOCIO
    # -----------------------------
    def validar_fecha_registro(self, fecha: date):
        hoy = date.today()
        if fecha.year < hoy.year:
            raise ValueError("No se permiten productos registrados en años anteriores.")

    def validar_precios(self, compra: Decimal, venta: Decimal):
        if compra < 0 or venta < 0:
            raise ValueError("Los precios no pueden ser negativos.")
        if venta < compra:
            raise ValueError("El precio de venta no puede ser menor al precio de compra.")

    def validar_stock(self, stock: int):
        if stock < 0:
            raise ValueError("El stock no puede ser negativo.")

    # -----------------------------
    # CREAR PRODUCTO
    # -----------------------------
    def crear_producto(self, codigo, descripcion, precio_compra, precio_venta, stock, fecha):
        self.validar_fecha_registro(fecha)
        self.validar_precios(precio_compra, precio_venta)
        self.validar_stock(stock)

        p = Producto(
            codigo=codigo,
            descripcion=descripcion,
            precio_compra=precio_compra,
            precio_venta=precio_venta,
            stock=stock,
            estado=True,
            fecha_registro=fecha
        )
        with SessionLocal() as db:
            return ProductoDAO(db).crear(p)

    # -----------------------------
    # EDITAR PRODUCTO
    # -----------------------------
    def editar_producto(self, id_producto, codigo, descripcion, precio_compra, precio_venta, stock, fecha):
        self.validar_fecha_registro(fecha)
        self.validar_precios(precio_compra, precio_venta)
        self.validar_stock(stock)

        with SessionLocal() as db:
            dao = ProductoDAO(db)
            prod = dao.obtener(id_producto)
            if not prod:
                raise ValueError("Producto no encontrado.")
            prod.codigo = codigo
            prod.descripcion = descripcion
            prod.precio_compra = precio_compra
            prod.precio_venta = precio_venta
            prod.stock = stock
            prod.fecha_registro = fecha

            return dao.editar(prod)

    # -----------------------------
    # BÚSQUEDA
    # -----------------------------
    def buscar(self, texto: str):
        with SessionLocal() as db:
            return ProductoDAO(db).listar(texto)

    # -----------------------------
    # ELIMINAR PRODUCTO
    # -----------------------------
    def eliminar_producto(self, id_producto):
        with SessionLocal() as db:
            dao = ProductoDAO(db)
            prod = dao.obtener(id_producto)
            if not prod:
                raise ValueError("Producto no encontrado.")
            return dao.eliminar(prod)



