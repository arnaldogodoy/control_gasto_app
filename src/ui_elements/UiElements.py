import flet as ft

def crea_snack_bar():
    return ft.SnackBar(content = ft.Text(""), bgcolor = "green", duration = 3000)


def mensaje_snack_bar_ok(page: ft.Page, mensaje: str, color: str = 'green'):
    page.snack_bar.content = ft.Text(mensaje)
    page.snack_bar.bgcolor = color
    page.snack_bar.open = True
    page.update()

def mensaje_snack_bar_error(page: ft.Page, mensaje: str):
    page.snack_bar.content = ft.Text(mensaje)
    page.snack_bar.bgcolor = "red"
    page.snack_bar.open = True
    page.update()