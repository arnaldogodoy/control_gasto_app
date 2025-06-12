
import flet as ft
from rutas.ConfiguraRutas import configurar_rutas

def main(page: ft.Page):
    page.title = "Control de gastos"
    page.theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE,
                          elevated_button_theme=ft.ElevatedButtonTheme(
                              disabled_bgcolor= ft.Colors.GREY_300)# Color gris para botones Elevated deshabilitados.
                          )
    page.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.ORANGE ) 
    page.theme_mode = ft.ThemeMode.LIGHT # O ft.ThemeMode.SYSTEM

    page.window.width = 1920  # Ancho inicial de la ventana (opcional)
    page.window.height = 1080 # Alto inicial de la ventana (opcional)
    page.window.min_height = 800
    page.window.min_width = 700
    page.window.resizable =True
    page.update() 

    # Configuración de rutas
    page.route = "/inicio" # Ruta inicial
    configurar_rutas(page)
ft.app(target=main)