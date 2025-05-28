
import flet as ft
from rutas.ConfiguraRutas import configurar_rutas

def main(page: ft.Page):
    page.title = "Control de gastos"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE )
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE ) 
    page.theme_mode = ft.ThemeMode.LIGHT # O ft.ThemeMode.SYSTEM

    page.window_width = 800  # Ancho inicial de la ventana (opcional)
    page.window_height = 600 # Alto inicial de la ventana (opcional)
    page.window_min_height = 700
    page.window_min_width = 500
    page.window.resizable =True
    page.update() 

    # Configuración de rutas
    page.route = "/inicio" # Ruta inicial
    configurar_rutas(page)
ft.app(target=main)