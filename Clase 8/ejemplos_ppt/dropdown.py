import flet as ft


def main(page: ft.Page):
    nacionalidad = ft.Dropdown(
        label="Nacionalidad",
        options=[
            ft.DropdownOption(key="Paraguay", text="Paraguay"),
            ft.DropdownOption(key="Argentina", text="Argentina"),
            ft.DropdownOption(key="Brasil", text="Brasil"),
            ft.DropdownOption(key="Uruguay", text="Uruguay"),
        ],
        on_select=lambda e: print("Elegiste:", e.control.value),
    )

    page.add(nacionalidad)


ft.run(main)
