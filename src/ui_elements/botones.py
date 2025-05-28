import flet as ft


# ui_elements/botones.py

import flet as ft

def boton_primario(
    page: ft.Page, 
    text: str,
    on_click: callable, 
    visible: bool = True,
    icon: str = None, # Parámetro opcional para un icono
    width: int = None, # Permitir ancho personalizable, None para autoajuste
    height: int = 45, # Altura estándar
    tooltip: str = None # Tooltip opcional
):
    btn = ft.ElevatedButton(
        text=text,
        icon=icon,
        on_click=on_click,
        visible=visible,
        width=width,
        height=height,
        elevation=6,
        tooltip=tooltip,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8), # Bordes redondeados consistentes
            padding= ft.padding.symmetric(horizontal=20,vertical=12),
            side=ft.BorderSide(width=1,color=ft.Colors.with_opacity(0.1,ft.Colors.BLACK))
        )
    )
    return btn

# ui_elements/botones.py (continuación)

def boton_cancelar_navegacion(
    page: ft.Page,
    text: str,
    ruta_destino: str,
    visible: bool = True,
    on_click: callable = None,
    icon: str = None,
    width: int = None, 
    height: int = 45,
    tooltip: str = None
):
    color_borde = ft.Colors.ORANGE 
    color_texto = ft.Colors.ORANGE

    accion_on_click = on_click if on_click else (lambda _: page.go(ruta_destino) if ruta_destino else None)

    btn = ft.OutlinedButton(
        text=text,
        icon=icon,
        on_click=accion_on_click,
        visible=visible,
        width=width,
        height=height,
        tooltip=tooltip,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=8),
            padding= ft.padding.symmetric(horizontal=20,vertical=12)
        )
    )
    return btn