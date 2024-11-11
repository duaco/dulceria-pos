import flet as ft
from src.views.sales_view import SalesView

def main(page: ft.Page):
    # Configuración inicial de la página
    page.window_width = 1200
    page.window_height = 800
    page.window_resizable = True
    page.window_maximized = True
    page.padding = 0
    page.bgcolor = "#E0E0E0"
    page.window_title_bar_hidden = True
    page.window_frameless = False

    # Crear la vista de ventas
    sales_view = SalesView(page)
    # Agregar el contenido a la página
    page.add(sales_view.build())
    # Actualizar la página
    page.update()

ft.app(target=main)
