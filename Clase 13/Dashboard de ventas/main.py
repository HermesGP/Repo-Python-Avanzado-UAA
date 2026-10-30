import flet as ft
from database.config import Base, engine
from views.producto_view import ProductoView
from views.cliente_view import ClienteView
from views.venta_view import VentaView
from views.dashboard_view import DashboardView

DASHBOARD_INDEX = 3

def main(page: ft.Page):
    page.title = "Flet Tienda de Informática"
    dashboard = DashboardView()

    async def al_cambiar_pestaña(e):
        # Cada vez que se abre la pestaña del dashboard se regeneran los gráficos.
        if e.control.selected_index == DASHBOARD_INDEX:
            await dashboard.actualizar()

    page.add(
        ft.Tabs(
            on_change=al_cambiar_pestaña,
            content=ft.Column(
                controls=[
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Ventas", icon=ft.Icons.RECEIPT),
                            ft.Tab(label="Clientes", icon=ft.Icons.PEOPLE),
                            ft.Tab(label="Productos", icon=ft.Icons.INVENTORY),
                            ft.Tab(label="Dashboard", icon=ft.Icons.INSERT_CHART),
                        ]
                    ),
                    ft.TabBarView(
                        controls=[VentaView(), ClienteView(), ProductoView(), dashboard],
                        expand=True,
                    ),
                ],
                expand=True,
            ),
            length=4,
            expand=True,
        )
    )

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ft.run(main)