import flet as ft
def main(page):

    def confirmar(e):
        dlg = ft.AlertDialog(
            title=ft.Text("Confirmación"),
            content=ft.Text("¿Desea eliminar este registro?"),
            actions=[
                ft.TextButton("Sí", on_click=lambda e: elegir("sí")),
                ft.TextButton("No", on_click=lambda e: elegir("no")),
            ]
        )
        page.show_dialog(dlg)

    def elegir(opcion):
        page.pop_dialog()
        page.add(ft.Text(f"Elegiste: {opcion}"))

    page.add(ft.Button("Eliminar", on_click=confirmar))

ft.run(main)
