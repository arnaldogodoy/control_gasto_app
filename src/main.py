
import flet as ft
from rutas.ConfiguraRutas import configurar_rutas

def main(page: ft.Page):
    page.route = "/inicio"
    configurar_rutas(page)
ft.app(target=main)