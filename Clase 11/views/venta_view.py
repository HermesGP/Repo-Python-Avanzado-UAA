from datetime import date
from decimal import Decimal

import flet as ft
from sqlalchemy.exc import SQLAlchemyError

from models.cliente import Cliente
from models.producto import Producto
from services.cliente_service import ClienteService
from services.venta_service import VentaService, calcular_iva


def formatear_monto(monto: Decimal) -> str:
    # Ejemplo: Decimal("1500000") -> "Gs. 1,500,000"
    return f"Gs. {monto:,.0f}"


# ============================================================
# Vista principal: lista y búsqueda de ventas
# Aquí se intercambian las otras dos vistas (detalle y nueva venta)
# ============================================================
class VentaView(ft.Column):
    def __init__(self):
        super().__init__(expand=True, spacing=12)
        self.service = VentaService()

        # --- Filtros de búsqueda ---
        self.txt_documento = ft.TextField(
            label="Buscar por documento del cliente",
            expand=True,
            on_submit=self.buscar,
        )

        # --- DatePicker (el campo es de solo lectura; se llena desde el calendario) ---
        self.txt_fecha = ft.TextField(label="Fecha", read_only=True, width=180)
        self.date_picker = ft.DatePicker(on_change=self.fecha_seleccionada)

        # --- Tabla de ventas ---
        self.tabla = ft.DataTable(
            width=float("inf"),
            show_checkbox_column=False,
            columns=[
                ft.DataColumn(label=ft.Text("Venta")),
                ft.DataColumn(label=ft.Text("Fecha")),
                ft.DataColumn(label=ft.Text("Cliente")),
                ft.DataColumn(label=ft.Text("Documento")),
                ft.DataColumn(label=ft.Text("Total")),
            ],
            rows=[],
        )

        # Zona intercambiable: muestra la lista, el detalle o la nueva venta
        self.contenido = ft.Column(
            controls=[],
            expand=True,
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        # --- Diseño de la vista: encabezado con botón + zona intercambiable ---
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text("Gestión de ventas", size=24, weight=ft.FontWeight.BOLD, expand=True),
                    ft.Button(
                        "Nueva venta",
                        icon=ft.Icons.ADD,
                        on_click=self.abrir_nueva_venta,
                    ),
                ]
            ),
            self.contenido,
        ]

    # Se ejecuta cuando la vista ya está en la página: muestra la lista
    def did_mount(self):
        self.mostrar_lista()

    # ============================================================
    # SnackBar para errores
    # ============================================================
    def mostrar_error(self, mensaje: str):
        self.page.show_dialog(
            ft.SnackBar(
                content=ft.Text(mensaje),
                bgcolor=ft.Colors.RED_400,
                action="Cerrar",
            )
        )

    # ============================================================
    # Mostrar lista (filtros + tabla)
    # ============================================================
    def mostrar_lista(self):
        self.contenido.controls = [
            ft.ResponsiveRow(
                controls=[
                    self.txt_documento,
                    ft.Row(
                        controls=[
                            self.txt_fecha,
                            ft.IconButton(
                                icon=ft.Icons.CALENDAR_MONTH,
                                tooltip="Elegir fecha",
                                on_click=lambda e: self.page.show_dialog(self.date_picker),
                            ),
                        ],
                        col={"xs": 12, "md": 4},
                    ),
                    ft.Row(
                        controls=[
                            ft.Button("Buscar", on_click=self.buscar),
                            ft.OutlinedButton("Limpiar filtros", on_click=self.limpiar_filtros),
                        ],
                        col={"xs": 12, "md": 4},
                    ),
                ]
            ),
            ft.Text("Haga clic en una venta para ver su comprobante."),
            ft.Column(
                controls=[self.tabla],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
        ]
        self.buscar(None)

    # ============================================================
    # DatePicker
    # ============================================================
    def fecha_seleccionada(self, e):
        if self.date_picker.value:
            self.txt_fecha.value = date.strftime(self.date_picker.value, "%Y-%m-%d")
            self.buscar(None)

    # ============================================================
    # Buscar y cargar tabla (un clic en la fila abre el detalle)
    # ============================================================
    def buscar(self, e):
        try:
            texto_fecha = (self.txt_fecha.value or "").strip()
            fecha = date.fromisoformat(texto_fecha) if texto_fecha else None
            ventas = self.service.listar(
                documento=self.txt_documento.value or "",
                fecha=fecha,
            )
            self.tabla.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(venta.id_venta))),
                        ft.DataCell(ft.Text(venta.fecha_venta.isoformat())),
                        ft.DataCell(ft.Text(cliente.nombre_completo)),
                        ft.DataCell(ft.Text(cliente.documento)),
                        ft.DataCell(ft.Text(formatear_monto(venta.total))),
                    ],
                    on_select_change=lambda e, id_venta=venta.id_venta: self.abrir_detalle(id_venta),
                )
                for venta, cliente in ventas
            ]
            self.update()
        except (ValueError, SQLAlchemyError) as ex:
            self.mostrar_error(str(ex))

    # ============================================================
    # Limpiar filtros
    # ============================================================
    def limpiar_filtros(self, e):
        self.txt_documento.value = ""
        self.txt_fecha.value = ""
        self.buscar(None)

    # ============================================================
    # Navegación: reemplaza el contenido por otra vista
    # ============================================================
    def abrir_nueva_venta(self, e):
        try:
            self.contenido.controls = [NuevaVentaView(self)]
            self.update()
        except SQLAlchemyError as ex:
            self.mostrar_error(str(ex))

    def abrir_detalle(self, id_venta: int):
        try:
            self.contenido.controls = [DetalleVentaView(self, id_venta)]
            self.update()
        except (ValueError, SQLAlchemyError) as ex:
            self.mostrar_error(str(ex))


# ============================================================
# Vista de detalle: cabecera y detalles de una venta (solo lectura)
# ============================================================
class DetalleVentaView(ft.Column):
    def __init__(self, app: VentaView, id_venta: int):
        super().__init__(expand=True, spacing=12)
        self.app = app
        # Cabecera de la venta, datos del cliente y lista de (detalle, producto)
        self.venta, self.cliente, self.detalles = app.service.obtener_detalle(id_venta)

        # --- Diseño: título + datos del cliente + tabla de detalles + totales ---
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text(
                        f"Venta Nro. {self.venta.id_venta}",
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        expand=True,
                    ),
                    ft.OutlinedButton("Volver", on_click=self.volver),
                ]
            ),
            ft.Text(f"Fecha: {self.venta.fecha_venta.isoformat()}"),
            ft.Text(f"Cliente: {self.cliente.nombre_completo}"),
            ft.Text(f"Documento: {self.cliente.documento}"),
            ft.Text(f"Correo: {self.cliente.email}"),
            ft.Text(f"Teléfono: {self.cliente.telefono}"),
            ft.DataTable(
                width=float("inf"),
                columns=[
                    ft.DataColumn(label=ft.Text("Código")),
                    ft.DataColumn(label=ft.Text("Producto")),
                    ft.DataColumn(label=ft.Text("Cantidad")),
                    ft.DataColumn(label=ft.Text("Precio unitario")),
                    ft.DataColumn(label=ft.Text("Subtotal")),
                    ft.DataColumn(label=ft.Text("Descuento")),
                    ft.DataColumn(label=ft.Text("IVA")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(producto.codigo)),
                            ft.DataCell(ft.Text(producto.descripcion)),
                            ft.DataCell(ft.Text(str(detalle.cantidad))),
                            ft.DataCell(ft.Text(formatear_monto(detalle.precio_unitario))),
                            ft.DataCell(ft.Text(formatear_monto(detalle.subtotal))),
                            ft.DataCell(ft.Text(formatear_monto(detalle.descuento))),
                            ft.DataCell(ft.Text(formatear_monto(detalle.iva))),
                        ]
                    )
                    for detalle, producto in self.detalles
                ],
            ),
            ft.Column(
                controls=[
                    ft.Text(f"Subtotal: {formatear_monto(self.venta.subtotal)}"),
                    ft.Text(f"Descuento: {formatear_monto(self.venta.descuento)}"),
                    ft.Text(f"IVA: {formatear_monto(self.venta.iva)}"),
                    ft.Text(
                        f"Total: {formatear_monto(self.venta.total)}",
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                wrap=True,
            ),
        ]

    # ============================================================
    # Volver a la lista
    # ============================================================
    def volver(self, e):
        self.app.mostrar_lista()


# ============================================================
# Vista de nueva venta: arma la cabecera y los detalles antes de guardar
# ============================================================
class NuevaVentaView(ft.Column):
    def __init__(self, app: VentaView):
        super().__init__(expand=True, spacing=12)
        self.app = app
        self.service = app.service

        # Clientes activos y productos con stock, cargados una sola vez
        self.clientes, self.productos = self.service.obtener_opciones()
        self.clientes_por_documento = {
            cliente.documento.strip().casefold(): cliente
            for cliente in self.clientes
        }
        self.productos_por_codigo = {
            producto.codigo.strip().casefold(): producto
            for producto in self.productos
        }

        # --- Estado de la venta en curso ---
        self.cliente_seleccionado: Cliente | None = None
        # id_producto -> (producto, cantidad)
        self.lineas: dict[int, tuple[Producto, int]] = {}
        self.producto_actual: Producto | None = None

        # --- Cliente (se busca por documento al escribir) ---
        self.txt_documento_cliente = ft.TextField(
            label="Documento del cliente",
            value="Ninguno",
            on_change=self.buscar_cliente,
            expand=True,
        )
        self.txt_cliente = ft.Text(
            "Ninguno",
            expand=True,
        )

        # --- Producto (código tipeado o leído con lector de código de barras) ---
        self.txt_codigo_producto = ft.TextField(
            label="Código de producto",
            hint_text="Escriba o escanee el código",
            on_change=self.codigo_producto_cambiado,
            on_submit=self.escanear_producto,
            expand=True,
        )
        self.txt_producto = ft.Text("Ninguno", expand=True)
        self.dd_cantidad = ft.Dropdown(
            label="Cantidad",
            options=[ft.dropdown.Option(key="1", text="1")],
            value="1",
            width=110,
        )

        # --- Tabla de detalles de la venta ---
        self.tabla = ft.DataTable(
            width=float("inf"),
            columns=[
                ft.DataColumn(label=ft.Text("Código")),
                ft.DataColumn(label=ft.Text("Producto")),
                ft.DataColumn(label=ft.Text("Precio")),
                ft.DataColumn(label=ft.Text("Cantidad")),
                ft.DataColumn(label=ft.Text("Subtotal")),
                ft.DataColumn(label=ft.Text("IVA 10%")),
                ft.DataColumn(label=ft.Text("Acción")),
            ],
            rows=[],
        )

        # --- Totales ---
        self.txt_subtotal = ft.Text("Subtotal: Gs. 0")
        self.txt_descuento = ft.Text("Descuento: Gs. 0")
        self.txt_iva = ft.Text("IVA: Gs. 0")
        self.txt_total = ft.Text("Total: Gs. 0", size=22, weight=ft.FontWeight.BOLD, expand=True)

        # --- Diseño: cliente, producto, tabla, totales y botones ---
        self.controls = [
            ft.Row(
                controls=[
                    ft.Text("Nueva venta", size=22, weight=ft.FontWeight.BOLD, expand=True),
                ]
            ),
            ft.Row(
                controls=[
                    self.txt_documento_cliente,
                    ft.IconButton(
                        icon=ft.Icons.PERSON_ADD,
                        tooltip="Nuevo cliente",
                        on_click=self.abrir_nuevo_cliente,
                    ),
                    ft.Text("Cliente:", weight=ft.FontWeight.BOLD),
                    self.txt_cliente,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Text("Agregar Producto:", weight=ft.FontWeight.BOLD),
            ft.Row(
                controls=[
                    ft.Row(
                        controls=[self.txt_codigo_producto, self.txt_producto],
                        expand=True,
                    ),
                    self.dd_cantidad,
                    ft.Button(
                        "Agregar producto",
                        icon=ft.Icons.ADD,
                        on_click=self.agregar_producto,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            ft.Column(
                controls=[self.tabla],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
            self.txt_subtotal,
            self.txt_descuento,
            self.txt_iva,
            self.txt_total,
            ft.Row(
                controls=[
                    ft.Button(
                        "Guardar",
                        icon=ft.Icons.SAVE,
                        on_click=self.guardar,
                    ),
                    ft.OutlinedButton(
                        "Cancelar",
                        icon=ft.Icons.CANCEL,
                        on_click=self.confirmar_cancelacion,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]

    # ============================================================
    # Cliente: buscar por documento
    # ============================================================
    def buscar_cliente(self, e):
        documento = (self.txt_documento_cliente.value or "").strip()
        self.cliente_seleccionado = (
            self.clientes_por_documento.get(documento.casefold())
            if documento and documento.casefold() != "ninguno"
            else None
        )
        self.txt_cliente.value = (
            self.cliente_seleccionado.nombre_completo
            if self.cliente_seleccionado
            else "Ninguno"
        )
        self.update()

    # ============================================================
    # Cliente: alta rápida en un diálogo (la venta en curso no se pierde)
    # ============================================================
    def abrir_nuevo_cliente(self, e):
        documento = (self.txt_documento_cliente.value or "").strip()
        if documento.casefold() == "ninguno":
            documento = ""
        campos = {
            "nombre": ft.TextField(label="Nombre completo", autofocus=True),
            "documento": ft.TextField(label="Documento / RUC", value=documento),
            "email": ft.TextField(label="Correo electrónico"),
            "telefono": ft.TextField(label="Teléfono"),
            "direccion": ft.TextField(label="Dirección"),
        }
        txt_error = ft.Text("", color=ft.Colors.RED_400)

        def guardar_cliente(ev):
            try:
                ClienteService().crear_cliente(
                    campos["nombre"].value or "",
                    campos["documento"].value or "",
                    campos["email"].value or "",
                    campos["telefono"].value or "",
                    campos["direccion"].value or "",
                    True,
                    date.today(),
                )
            except (ValueError, SQLAlchemyError) as ex:
                txt_error.value = str(ex)
                txt_error.update()
                return
            self.page.pop_dialog()
            # Solo se recargan los clientes: las líneas de la venta no se tocan
            self.clientes, _ = self.service.obtener_opciones()
            self.clientes_por_documento = {
                cliente.documento.strip().casefold(): cliente
                for cliente in self.clientes
            }
            self.txt_documento_cliente.value = (campos["documento"].value or "").strip()
            self.buscar_cliente(None)

        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Nuevo cliente"),
                content=ft.Column(
                    controls=[*campos.values(), txt_error],
                    tight=True,
                    width=400,
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=self.cerrar_dialogo),
                    ft.Button("Guardar cliente", on_click=guardar_cliente),
                ],
            )
        )

    # ============================================================
    # Producto: previsualizar al escribir el código
    # ============================================================
    def codigo_producto_cambiado(self, e):
        codigo = (self.txt_codigo_producto.value or "").strip().casefold()
        producto = self.productos_por_codigo.get(codigo)
        if producto is None:
            self.producto_actual = None
            self.txt_producto.value = "Ninguno" if not codigo else "Código no reconocido"
            self.dd_cantidad.options = [ft.dropdown.Option(key="1", text="1")]
            self.dd_cantidad.value = "1"
            self.update()
            return

        try:
            self.configurar_producto(producto)
        except ValueError as ex:
            self.app.mostrar_error(str(ex))

    # ============================================================
    # Producto: cargar por código y limitar la cantidad al stock restante
    # ============================================================
    def cargar_producto_por_codigo(self):
        codigo = (self.txt_codigo_producto.value or "").strip().casefold()
        producto = self.productos_por_codigo.get(codigo)
        if producto is None:
            self.producto_actual = None
            self.txt_producto.value = "Producto no encontrado"
            self.dd_cantidad.options = [ft.dropdown.Option(key="1", text="1")]
            self.dd_cantidad.value = "1"
            raise ValueError(f"No se encontró un producto con el código '{codigo}'.")

        self.configurar_producto(producto)

    # Muestra el producto y deja elegir hasta el stock que aún no se agregó
    def configurar_producto(self, producto: Producto):
        self.producto_actual = producto
        self.txt_producto.value = (
            f"{producto.descripcion} — {formatear_monto(producto.precio_venta)} "
            f"(stock: {producto.stock})"
        )
        id_producto = producto.id_producto
        cantidad_agregada = self.lineas.get(id_producto, (producto, 0))[1]
        disponible = producto.stock - cantidad_agregada
        if disponible <= 0:
            self.dd_cantidad.options = []
            self.dd_cantidad.value = None
            self.update()
            raise ValueError(f"No queda stock disponible de {producto.descripcion}.")
        self.dd_cantidad.options = [
            ft.dropdown.Option(key=str(cantidad), text=str(cantidad))
            for cantidad in range(1, disponible + 1)
        ]
        self.dd_cantidad.value = "1"
        self.update()

    # Enter en el campo de código (lector de barras): agrega 1 unidad directamente
    def escanear_producto(self, e):
        try:
            self.cargar_producto_por_codigo()
            self.agregar_producto(None)
        except ValueError as ex:
            self.app.mostrar_error(str(ex))

    # ============================================================
    # Detalles: agregar / quitar productos
    # ============================================================
    def agregar_producto(self, e):
        try:
            if self.producto_actual is None:
                self.cargar_producto_por_codigo()
            if not self.dd_cantidad.value:
                raise ValueError("No hay stock disponible para agregar este producto.")
            cantidad = int(self.dd_cantidad.value)
            if cantidad <= 0:
                raise ValueError("La cantidad debe ser mayor que cero.")
            producto = self.producto_actual
            if producto is None:
                raise ValueError("Ingrese o escanee el código de un producto.")
            id_producto = producto.id_producto
            cantidad_actual = self.lineas.get(id_producto, (producto, 0))[1]
            if cantidad_actual + cantidad > producto.stock:
                raise ValueError(
                    f"Stock insuficiente para {producto.descripcion}: "
                    f"disponible {producto.stock}."
                )
            self.lineas[id_producto] = (producto, cantidad_actual + cantidad)
            self.producto_actual = None
            self.txt_codigo_producto.value = ""
            self.txt_producto.value = "Ninguno"
            self.dd_cantidad.options = [ft.dropdown.Option(key="1", text="1")]
            self.dd_cantidad.value = "1"
            self.actualizar_tabla()
        except ValueError as ex:
            self.app.mostrar_error(str(ex))

    def quitar_producto(self, id_producto: int):
        self.lineas.pop(id_producto, None)
        self.actualizar_tabla()

    # ============================================================
    # Actualizar tabla y totales (IVA 10% por línea)
    # ============================================================
    def actualizar_tabla(self):
        subtotal = Decimal("0")
        iva_total = Decimal("0")
        filas = []
        for id_producto, (producto, cantidad) in self.lineas.items():
            subtotal_linea = producto.precio_venta * cantidad
            iva_linea = calcular_iva(subtotal_linea)
            subtotal += subtotal_linea
            iva_total += iva_linea
            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(producto.codigo)),
                        ft.DataCell(ft.Text(producto.descripcion)),
                        ft.DataCell(ft.Text(formatear_monto(producto.precio_venta))),
                        ft.DataCell(ft.Text(str(cantidad))),
                        ft.DataCell(ft.Text(formatear_monto(subtotal_linea))),
                        ft.DataCell(ft.Text(formatear_monto(iva_linea))),
                        ft.DataCell(
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                tooltip="Quitar producto",
                                on_click=lambda e, pid=id_producto: self.quitar_producto(pid),
                            )
                        ),
                    ]
                )
            )
        total = subtotal + iva_total
        self.tabla.rows = filas
        self.txt_subtotal.value = f"Subtotal: {formatear_monto(subtotal)}"
        self.txt_descuento.value = "Descuento: Gs. 0"
        self.txt_iva.value = f"IVA: {formatear_monto(iva_total)}"
        self.txt_total.value = f"Total: {formatear_monto(total)}"
        self.update()

    # ============================================================
    # Guardar (crea cabecera + detalles y descuenta stock en una transacción)
    # ============================================================
    def guardar(self, e):
        try:
            self.buscar_cliente(None)
            if not self.cliente_seleccionado:
                raise ValueError("Ingrese el Documento de un cliente activo.")
            lineas = [
                (id_producto, cantidad)
                for id_producto, (_, cantidad) in self.lineas.items()
            ]
            id_venta = self.service.crear_venta(
                self.cliente_seleccionado.id_cliente,
                lineas,
            )
            self.app.txt_documento.value = ""
            self.app.txt_fecha.value = ""
            self.app.mostrar_lista()
            self.app.mostrar_error(f"Venta #{id_venta} guardada correctamente.")
        except (ValueError, SQLAlchemyError) as ex:
            self.app.mostrar_error(str(ex))

    # ============================================================
    # Cancelar (con diálogo de confirmación)
    # ============================================================
    def confirmar_cancelacion(self, e):
        self.page.show_dialog(
            ft.AlertDialog(
                modal=True,
                title=ft.Text("Cancelar nueva venta"),
                content=ft.Text(
                    "¿Está seguro de cancelar? Se perderán los productos agregados."
                ),
                actions=[
                    ft.TextButton("No continuar", on_click=self.cerrar_dialogo),
                    ft.TextButton("Sí, cancelar", on_click=self.cancelar_confirmado),
                ],
            )
        )

    def cerrar_dialogo(self, e):
        self.page.pop_dialog()

    def cancelar_confirmado(self, e):
        self.page.pop_dialog()
        self.app.mostrar_lista()
