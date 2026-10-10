import flet as ft
from database.config import Base, engine
from views.producto_view import ProductoView

def main(page: ft.Page):
    page.title = "Gestión de Productos - MVC + Flet"
    page.add(ProductoView())

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    ft.run(main)