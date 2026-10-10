import flet as ft
from datetime import date
from decimal import Decimal
from services.producto_service import ProductoService

class ProductoView(ft.Column):

    def __init__(self):
        super().__init__(expand=True)
        self.service = ProductoService()

        # --- Campos del formulario ---
        self.txt_codigo = ft.TextField(label="Código", col={"xs":12, "md":6})
        self.txt_descripcion = ft.TextField(label="Descripción", col={"xs":12, "md":6})
        self.txt_precio_compra = ft.TextField(label="Precio compra", col={"xs":12, "md":6})
        self.txt_precio_venta = ft.TextField(label="Precio venta", col={"xs":12, "md":6})
        self.txt_stock = ft.TextField(label="Stock", col={"xs":12, "md":6})

        # --- DatePicker ---
        self.txt_fecha = ft.TextField(label="Fecha registro", read_only=True, col={"xs":12, "md":6})
        self.date_picker = ft.DatePicker(on_change=self.on_date_selected)
        self.txt_fecha.on_click = self.abrir_date_picker

        # --- Botones ---
        self.btn_guardar = ft.Button(
            "Guardar", 
            on_click=self.guardar,
            bgcolor=ft.Colors.BLUE_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.SAVE,
        )
        self.btn_limpiar = ft.OutlinedButton(
            "Limpiar", 
            on_click=self.limpiar,
            icon=ft.Icons.CLEAR,
        )
        self.btn_borrar = ft.Button(
            "Borrar",
            on_click=self.borrar,
            bgcolor=ft.Colors.RED_600,
            color=ft.Colors.WHITE,
            icon=ft.Icons.DELETE,
        )

        # --- Búsqueda + tabla ---
        self.txt_buscar = ft.TextField(label="Buscar", on_change=self.buscar, width=float("inf"))

        self.tabla = ft.DataTable(
            width=float("inf"),
            columns=[
                ft.DataColumn(label=ft.Text("Código")),
                ft.DataColumn(label=ft.Text("Descripción")),
                ft.DataColumn(label=ft.Text("Precio Venta")),
                ft.DataColumn(label=ft.Text("Stock")),
                ft.DataColumn(label=ft.Text("Fecha")),
            ],
            rows=[]
        )

        self.producto_editando = None
        self.controls = [
            ft.Container(
                content=ft.ResponsiveRow(
                    controls=[
                        self.txt_codigo,
                        self.txt_descripcion,
                        self.txt_precio_compra,
                        self.txt_precio_venta,
                        self.txt_stock,
                        self.txt_fecha,
                        ft.Row(
                            controls=[self.btn_guardar, self.btn_limpiar, self.btn_borrar],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ]
                ),
                padding=10,
                bgcolor=ft.Colors.SURFACE_CONTAINER,
                border_radius=10,
            ),
            self.txt_buscar,
            ft.Column(
                controls=[self.tabla],
                scroll=ft.ScrollMode.ADAPTIVE,
                expand=True,
            ),
        ]

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
    # DatePicker
    # ============================================================
    def abrir_date_picker(self, e):
        self.page.show_dialog(self.date_picker)

    def on_date_selected(self, e):
        self.txt_fecha.value = str(self.date_picker.value)
        self.update()

    def did_mount(self):
        self.cargar_tabla(self.service.buscar(""))

    # ============================================================
    # Cargar tabla
    # ============================================================
    def cargar_tabla(self, productos):
        self.tabla.rows = []
        for p in productos:
            self.tabla.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.codigo)),
                        ft.DataCell(ft.Text(p.descripcion)),
                        ft.DataCell(ft.Text(str(p.precio_venta))),
                        ft.DataCell(ft.Text(str(p.stock))),
                        ft.DataCell(ft.Text(str(p.fecha_registro))),
                    ],
                    on_select_change=lambda e, prod=p: self.cargar_formulario(prod)
                )
            )
        self.update()

    # ============================================================
    # Cargar formulario para editar
    # ============================================================
    def cargar_formulario(self, producto):
        self.producto_editando = producto
        self.txt_codigo.value = producto.codigo
        self.txt_descripcion.value = producto.descripcion
        self.txt_precio_compra.value = str(producto.precio_compra)
        self.txt_precio_venta.value = str(producto.precio_venta)
        self.txt_stock.value = str(producto.stock)
        self.txt_fecha.value = str(producto.fecha_registro)
        self.update()

    # ============================================================
    # Guardar (crear o editar)
    # ============================================================
    def guardar(self, e):
        try:
            codigo = self.txt_codigo.value
            descripcion = self.txt_descripcion.value
            precio_compra = Decimal(self.txt_precio_compra.value)
            precio_venta = Decimal(self.txt_precio_venta.value)
            stock = int(self.txt_stock.value)
            fecha = date.fromisoformat(self.txt_fecha.value)

            if self.producto_editando:
                self.service.editar_producto(
                    self.producto_editando.id_producto,
                    codigo,
                    descripcion,
                    precio_compra,
                    precio_venta,
                    stock,
                    fecha
                )
            else:
                self.service.crear_producto(
                    codigo,
                    descripcion,
                    precio_compra,
                    precio_venta,
                    stock,
                    fecha
                )

            self.limpiar(None)
            self.cargar_tabla(self.service.buscar(""))

        except Exception as ex:
            self.mostrar_error(str(ex))

    # ============================================================
    # Borrar
    # ============================================================

    def borrar(self, e):
        if not self.producto_editando:
            self.mostrar_error("Seleccione un producto para borrar.")
            return
        try:
            self.service.eliminar_producto(self.producto_editando.id_producto)
            self.limpiar(None)
            self.cargar_tabla(self.service.buscar(""))
        except Exception as ex:
            self.mostrar_error(str(ex))

    # ============================================================
    # Limpiar formulario
    # ============================================================
    def limpiar(self, e):
        self.producto_editando = None
        self.txt_codigo.value = ""
        self.txt_descripcion.value = ""
        self.txt_precio_compra.value = ""
        self.txt_precio_venta.value = ""
        self.txt_stock.value = ""
        self.txt_fecha.value = ""
        self.update()

    # ============================================================
    # Buscar
    # ============================================================
    def buscar(self, e):
        texto = self.txt_buscar.value
        productos = self.service.buscar(texto)
        self.cargar_tabla(productos)


