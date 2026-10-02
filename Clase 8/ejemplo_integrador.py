import flet as ft

def main(page: ft.Page):
    page.title = "Datos Personales"
    page.padding = 20
    page.scroll = ft.ScrollMode.ADAPTIVE

    # -----------------------------
    # CAMPOS DEL FORMULARIO
    # -----------------------------

    # Datos personales
    nombre = ft.TextField(label="Nombre Completo", col={"xs":12, "md":6})
    fecha_nac = ft.TextField(label="Fecha de nacimiento (dd/mm/aaaa)", col={"xs":12, "md":6})

    # Datos de contacto
    email = ft.TextField(label="Email", col={"xs":12, "md":6})
    telefono = ft.TextField(label="Teléfono", col={"xs":12, "md":6})
    direccion = ft.TextField(label="Dirección", col={"xs":12})

    # Selección de género
    genero = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Masculino", label="Masculino"),
            ft.Radio(value="Femenino", label="Femenino"),
            ft.Radio(value="Otro", label="Otro"),
        ])
    )

    # Nivel de estudios
    estudios = ft.RadioGroup(
        content=ft.Column([
            ft.Radio(value="Sin estudios", label="Sin estudios"),
            ft.Radio(value="Primario", label="Primario"),
            ft.Radio(value="Secundario", label="Secundario"),
            ft.Radio(value="Universitario", label="Universitario"),
            ft.Radio(value="Postgrado", label="Postgrado"),
        ])
    )

    # Estado civil
    estado_civil = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="Soltero/a", label="Soltero/a"),
            ft.Radio(value="Casado/a", label="Casado/a"),
            ft.Radio(value="Divorciado/a", label="Divorciado/a"),
            ft.Radio(value="Viudo/a", label="Viudo/a"),
        ])
    )

    # -----------------------------
    # FUNCIONES
    # -----------------------------

    def limpiar(e):
        nombre.value = ""
        fecha_nac.value = ""
        email.value = ""
        telefono.value = ""
        direccion.value = ""
        genero.value = None
        estudios.value = None
        estado_civil.value = None
        page.update()

    def guardar(e):
        dlg = ft.AlertDialog(
            title=ft.Text("Datos ingresados"),
            content=ft.Text(
                f"Nombre: {nombre.value}\n"
                f"Fecha de nacimiento: {fecha_nac.value}\n\n"
                f"Email: {email.value}\n"
                f"Teléfono: {telefono.value}\n"
                f"Dirección: {direccion.value}\n\n"
                f"Género: {genero.value}\n"
                f"Nivel de estudios: {estudios.value}\n"
                f"Estado civil: {estado_civil.value}"
            ),
            actions=[
                ft.TextButton("OK", on_click=lambda e: cerrar_dialogo())
            ],
            modal=True
        )
        page.show_dialog(dlg)

    def cerrar_dialogo():
        page.pop_dialog()

    # -----------------------------
    # BOTONES
    # -----------------------------

    botones = ft.Row(
        controls=[
            ft.Button("Guardar", icon=ft.Icons.SAVE, on_click=guardar),
            ft.Button("Limpiar", icon=ft.Icons.CLEAR, on_click=limpiar),
        ],
        spacing=20
    )

    # -----------------------------
    # LAYOUT RESPONSIVE
    # -----------------------------

    controles: list[ft.Control] = [
            ft.Text("Datos personales", size=20, weight=ft.FontWeight.BOLD),
            ft.ResponsiveRow([nombre, fecha_nac]),

            ft.Text("Datos de contacto", size=20, weight=ft.FontWeight.BOLD),
            ft.ResponsiveRow([email, telefono, direccion]),

            ft.Text("Género", size=20, weight=ft.FontWeight.BOLD),
            genero,

            ft.Text("Nivel de estudios", size=20, weight=ft.FontWeight.BOLD),
            estudios,

            ft.Text("Estado civil", size=20, weight=ft.FontWeight.BOLD),
            estado_civil,

            botones
    ]

    formulario = ft.Column(
        controls=controles,
        spacing=25
    )

    page.add(formulario)

ft.run(main)

