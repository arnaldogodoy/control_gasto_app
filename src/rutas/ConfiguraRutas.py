import flet as ft
from vistas.Login import inicio_sesion
from vistas.ReiniciarClave import reiniciar_clave
from vistas.EditarContraseña import editar_contraseña
from vistas.Registro import registro
from vistas.Home import home
from rutas import Rutas



def configurar_rutas(page: ft.Page):
    def cambiar_ruta(e):
        page.views.clear()
        route = page.route

        if page.route == Rutas.inicio:
            page.views.append(ft.View(route= Rutas.inicio,
                                      controls=[inicio_sesion(page)],
                                      vertical_alignment= ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment= ft.CrossAxisAlignment.CENTER
                                      ))
        elif page.route == Rutas.reiniciar_clave:
            page.views.append(ft.View(route=Rutas.reiniciar_clave, 
                                      controls=[reiniciar_clave(page)],
                                      vertical_alignment= ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment= ft.CrossAxisAlignment.CENTER
                                      ))
        elif page.route == Rutas.editar_contraseña:
            page.views.append(ft.View(route= Rutas.editar_contraseña, 
                                      controls = [editar_contraseña(page)],
                                     vertical_alignment = ft.MainAxisAlignment.CENTER,
                                     horizontal_alignment = ft.CrossAxisAlignment.CENTER))
        elif page.route == Rutas.registro:
            page.views.append(ft.View(route= Rutas.registro, 
                                      controls=[registro(page)],
                                      vertical_alignment= ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment= ft.CrossAxisAlignment.CENTER))
        elif page.route == Rutas.home:
            page.views.append(ft.View(route= Rutas.home, 
                                      controls=[home(page)],
                                      vertical_alignment= ft.MainAxisAlignment.CENTER,
                                      horizontal_alignment= ft.CrossAxisAlignment.CENTER))
        else:
            page.views.append(ft.View("/", [ft.Text("Página no encontrada")]))  # fallback
        page.update()
    page.on_route_change = cambiar_ruta
    page.go(page.route)