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

def crear_tarjeta_formulario(
    contenido: ft.Control,
    width: int = 450,
    height: int | None = None,

):
       
    tarjeta = ft.Card(
        content=ft.Container( # Contenedor interno para el padding del contenido
            content=contenido,
            padding=ft.padding.symmetric(vertical=25, horizontal=25) # Ajusta este padding según necesites
        ),
        width=width,
        height=height,
        elevation=4,  # Un valor típico para la elevación de una tarjeta. Experimenta.
        # margin=ft.margin.all(5) # Margen opcional alrededor de la tarjeta
    )

    return tarjeta