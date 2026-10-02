import flet as ft

def main(page):
    nombre = ft.TextField(label="Nombre")

    chk_news = ft.Checkbox(label="Deseo recibir noticias", value=False)

    genero = ft.RadioGroup(
        content=ft.Row([
            ft.Radio(value="M", label="Masculino"),
            ft.Radio(value="F", label="Femenino"),
            ft.Radio(value="X", label="Otro"),
        ])
    )

    def enviar(e):
        page.add(ft.Text(
            f"Nombre: {nombre.value}\n"
            f"Noticias: {chk_news.value}\n"
            f"Género: {genero.value}"
        ))

    page.add(
        nombre,
        chk_news,
        genero,
        ft.Button("Enviar", on_click=enviar)
    )

ft.run(main)

