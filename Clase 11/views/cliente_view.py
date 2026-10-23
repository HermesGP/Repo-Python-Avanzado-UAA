import flet as ft
from datetime import date

from services.cliente_service import ClienteService


class ClienteView(ft.Column):
    def __init__(self):
        super().__init__(expand=True)
        self.service = ClienteService()

        # --- Campos del formulario ---
        self.txt_nombre = ft.TextField(label="Nombre completo", col={"xs": 12, "md": 6})
        self.txt_documento = ft.TextField(label="Documento", col={"xs": 12, "md": 6})
        self.txt_email = ft.TextField(label="Correo electrónico", col={"xs": 12, "md": 6})
        self.txt_telefono = ft.TextField(label="Teléfono", col={"xs": 12, "md": 6})
        self.txt_direccion = ft.TextField(label="Dirección", col={"xs": 12, "md": 6})

        # --- DatePicker (el campo es de solo lectura; al hacer clic abre el calendario) ---
        self.txt_fecha_registro = ft.TextField(
            label="Fecha de registro",
            value=date.today().isoformat(),
            read_only=True,
            col={"xs": 12, "md": 6},
        )
        self.txt_fecha_registro.on_click = self.abrir_date_picker
        self.date_picker = ft.DatePicker(on_change=self.on_date_selected)

        # --- Estado del cliente (activo/inactivo) ---
        self.chk_estado = ft.Checkbox(label="Cliente activo", value=True)

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
        self.txt_buscar = ft.TextField(
            label="Buscar por nombre, documento o contacto",
            on_change=self.buscar,
            width=float("inf"),
        )
        self.tabla = ft.DataTable(
            width=float("inf"),
            columns=[
                ft.DataColumn(label=ft.Text("ID")),
                ft.DataColumn(label=ft.Text("Nombre completo")),
                ft.DataColumn(label=ft.Text("Documento")),
                ft.DataColumn(label=ft.Text("Correo")),
                ft.DataColumn(label=ft.Text("Teléfono")),
                ft.DataColumn(label=ft.Text("Dirección")),
                ft.DataColumn(label=ft.Text("Estado")),
                ft.DataColumn(label=ft.Text("Fecha de registro")),
            ],
            rows=[],
        )

        # Cliente seleccionado en la tabla (None = se está creando uno nuevo)
        self.cliente_editando = None

        # --- Diseño de la vista: título, formulario, búsqueda y tabla ---
        self.controls = [
            ft.Text("Gestión de clientes", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.ResponsiveRow(
                    controls=[
                        self.txt_nombre,
                        self.txt_documento,
                        self.txt_email,
                        self.txt_telefono,
                        self.txt_direccion,
                        self.txt_fecha_registro,
                        self.chk_estado,
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
        if self.date_picker.value:
            self.txt_fecha_registro.value = str(self.date_picker.value)
            self.update()

    # Se ejecuta cuando la vista ya está en la página: carga todos los clientes
    def did_mount(self):
        self.cargar_tabla(self.service.buscar(""))

    # ============================================================
    # Cargar tabla (un clic en la fila carga el formulario)
    # ============================================================
    def cargar_tabla(self, clientes):
        self.tabla.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente.id_cliente))),
                    ft.DataCell(ft.Text(cliente.nombre_completo)),
                    ft.DataCell(ft.Text(cliente.documento)),
                    ft.DataCell(ft.Text(cliente.email)),
                    ft.DataCell(ft.Text(cliente.telefono)),
                    ft.DataCell(ft.Text(cliente.direccion)),
                    ft.DataCell(ft.Text("Activo" if cliente.estado else "Inactivo")),
                    ft.DataCell(ft.Text(str(cliente.fecha_registro))),
                ],
                on_select_change=lambda e, seleccionado=cliente: self.cargar_formulario(
                    seleccionado
                ),
            )
            for cliente in clientes
        ]
        self.update()

    # ============================================================
    # Cargar formulario para editar
    # ============================================================
    def cargar_formulario(self, cliente):
        self.cliente_editando = cliente
        self.txt_nombre.value = cliente.nombre_completo
        self.txt_documento.value = cliente.documento
        self.txt_email.value = cliente.email
        self.txt_telefono.value = cliente.telefono
        self.txt_direccion.value = cliente.direccion
        self.txt_fecha_registro.value = str(cliente.fecha_registro)
        self.chk_estado.value = cliente.estado
        self.update()

    # ============================================================
    # Guardar (crear o editar)
    # ============================================================
    def guardar(self, e):
        try:
            fecha_registro = date.fromisoformat(self.txt_fecha_registro.value or "")
            datos = (
                self.txt_nombre.value or "",
                self.txt_documento.value or "",
                self.txt_email.value or "",
                self.txt_telefono.value or "",
                self.txt_direccion.value or "",
                self.chk_estado.value is True,
                fecha_registro,
            )

            if self.cliente_editando:
                self.service.editar_cliente(self.cliente_editando.id_cliente, *datos)
            else:
                self.service.crear_cliente(*datos)

            self.limpiar(None)
            self.cargar_tabla(self.service.buscar(self.txt_buscar.value or ""))
        except Exception as ex:
            self.mostrar_error(str(ex))

    # ============================================================
    # Borrar
    # ============================================================
    def borrar(self, e):
        if not self.cliente_editando:
            self.mostrar_error("Seleccione un cliente para borrar.")
            return
        try:
            self.service.eliminar_cliente(self.cliente_editando.id_cliente)
            self.limpiar(None)
            self.cargar_tabla(self.service.buscar(self.txt_buscar.value or ""))
        except Exception as ex:
            self.mostrar_error(str(ex))

    # ============================================================
    # Limpiar formulario
    # ============================================================
    def limpiar(self, e):
        self.cliente_editando = None
        self.txt_nombre.value = ""
        self.txt_documento.value = ""
        self.txt_email.value = ""
        self.txt_telefono.value = ""
        self.txt_direccion.value = ""
        self.txt_fecha_registro.value = date.today().isoformat()
        self.chk_estado.value = True
        self.update()

    # ============================================================
    # Buscar
    # ============================================================
    def buscar(self, e):
        self.cargar_tabla(self.service.buscar(self.txt_buscar.value or ""))
