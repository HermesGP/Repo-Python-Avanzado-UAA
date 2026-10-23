import flet as ft
from database.config import Base, engine
from views.producto_view import ProductoView
from views.cliente_view import ClienteView
from views.venta_view import VentaView

def main(page: ft.Page):
    page.title = "Flet Tienda de Informática"
    contenido = ft.Column(expand=True)

    def mostrar_vista(vista):
        contenido.controls = [vista]
        page.update()

    # Alternativa 1: mostrar las vistas una al lado de la otra.
    # page.add(
    #     ft.Row(
    #         controls=[VentaView(), ClienteView(), ProductoView()],
    #         expand=True,
    #         vertical_alignment=ft.CrossAxisAlignment.START,
    #     )
    # )

    # Alternativa 2: mostrar las vistas una debajo de otra.
    # page.add(
    #     ft.Column(
    #         controls=[VentaView(), ClienteView(), ProductoView()],
    #         expand=True,
    #         scroll=ft.ScrollMode.ADAPTIVE,
    #     )
    # )

    # Alternativa 3: agrupar las vistas en pestañas.
    # page.add(
    #     ft.Tabs(
    #         content=ft.Column(
    #             controls=[
    #                 ft.TabBar(
    #                     tabs=[
    #                         ft.Tab(label="Ventas",icon=ft.Icons.RECEIPT),
    #                         ft.Tab(label="Clientes",icon=ft.Icons.PEOPLE),
    #                         ft.Tab(label="Productos",icon=ft.Icons.INVENTORY),
    #                     ]
    #                 ),
    #                 ft.TabBarView(
    #                     controls=[VentaView(), ClienteView(), ProductoView()],
    #                     expand=True,
    #                 ),
    #             ],
    #             expand=True,
    #         ),
    #         length=3,
    #         expand=True,
    #     )
    # )

    # Alternativa 4: NavigationRail lateral y un contenedor para la vista activa.
    # vistas = [VentaView(), ClienteView(), ProductoView()]
    # contenido = ft.Column(controls=[vistas[0]], expand=True)
    #
    # def cambiar_seccion(e):
    #     contenido.controls = [vistas[e.control.selected_index]]
    #     page.update()
    #
    # page.add(
    #     ft.Row(
    #         controls=[
    #             ft.NavigationRail(
    #                 selected_index=0,
    #                 label_type=ft.NavigationRailLabelType.ALL,
    #                 destinations=[
    #                     ft.NavigationRailDestination(icon=ft.Icons.RECEIPT, label="Ventas"),
    #                     ft.NavigationRailDestination(icon=ft.Icons.PEOPLE, label="Clientes"),
    #                     ft.NavigationRailDestination(icon=ft.Icons.INVENTORY, label="Productos"),
    #                 ],
    #                 on_change=cambiar_seccion,
    #             ),
    #             ft.VerticalDivider(width=1),
    #             contenido,
    #         ],
    #         expand=True,
    #     )
    # )

    # Alternativa 5: AppBar con menú hamburguesa y NavigationDrawer.
    #vistas = [VentaView(), ClienteView(), ProductoView()]
    #contenido = ft.Column(controls=[vistas[0]], expand=True)
    
    #async def cambiar_desde_drawer(e):
    #     contenido.controls = [vistas[e.control.selected_index]]
    #     await page.close_drawer()
    #     page.update()

    #async def abrir_drawer(e):
    #     await page.show_drawer()
    
    #page.drawer = ft.NavigationDrawer(
    #     selected_index=0,
    #     on_change=cambiar_desde_drawer,
    #     controls=[
    #         ft.Container(
    #             content=ft.Text("Menú principal", size=20, weight=ft.FontWeight.BOLD),
    #             padding=20,
    #         ),
    #         ft.NavigationDrawerDestination(
    #             icon=ft.Icons.RECEIPT,
    #             label="Ventas",
    #             selected_icon=ft.Icons.RECEIPT,
    #         ),
    #         ft.NavigationDrawerDestination(
    #             icon=ft.Icons.PEOPLE,
    #             label="Clientes",
    #             selected_icon=ft.Icons.PEOPLE,
    #         ),
    #         ft.NavigationDrawerDestination(
    #             icon=ft.Icons.INVENTORY,
    #             label="Productos",
    #             selected_icon=ft.Icons.INVENTORY,
    #         ),
    #     ],
    # )
    #page.appbar = ft.AppBar(
    #     title=ft.Text("Sonic Tienda de Informática"),
    #     leading=ft.IconButton(
    #         icon=ft.Icons.MENU,
    #         tooltip="Abrir menú",
    #         on_click=abrir_drawer,
    #     ),
    # )
    #page.add(contenido)

    def cambiar_vista(e):
        vistas = {
            "ventas": VentaView,
            "clientes": ClienteView,
            "productos": ProductoView,
        }
        vista_seleccionada = e.control.value
        if vista_seleccionada:
            mostrar_vista(vistas[vista_seleccionada]())

    # Opción activa: Dropdown para elegir la vista que se mostrará.
    page.add(
        ft.Column(
            controls=[
                ft.Dropdown(
                    label="Seleccionar vista",
                    value="ventas",
                    options=[
                        ft.dropdown.Option(key="ventas", text="Ventas"),
                        ft.dropdown.Option(key="clientes", text="Clientes"),
                        ft.dropdown.Option(key="productos", text="Productos"),
                    ],
                    on_select=cambiar_vista,
                ),
                contenido,
            ],
            expand=True,
        )
    )
    mostrar_vista(VentaView())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ft.run(main)