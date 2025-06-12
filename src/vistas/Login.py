
import flet as ft
from db import db 
from rutas.Rutas import reiniciar_clave, registro
from ui_elements.UiElements import crear_tarjeta_formulario
from ui_elements.botones import boton_primario
from rutas.Rutas import home

def inicio_sesion(page: ft.Page):

    
    correo = ft.TextField(
        label="Correo electrónico", 
        prefix_icon=ft.Icons.EMAIL_OUTLINED,
        border_radius=ft.border_radius.all(10), # Bordes redondeados
        keyboard_type=ft.KeyboardType.EMAIL,
        value=page.client_storage.get("login_email") if page.client_storage else "", # Recordar email (opcional)
        width=350
    )
    clave = ft.TextField(
        label="Contraseña",
        prefix_icon=ft.Icons.LOCK_OUTLINE, 
        password=True,
        can_reveal_password=True,
        border_radius=ft.border_radius.all(10), # Bordes redondeados
        width=350
    )
    snack = ft.SnackBar(
        content=ft.Text(""),
        duration=3000
    )
    if snack not in page.overlay:
        page.overlay.append(snack)

    def login_click(e):
        email_val = correo.value.strip()
        clave_val = clave.value

        if not email_val or not clave_val:
            snack.content = ft.Text("Por favor, completa todos los campos.")
            snack.bgcolor = ft.Colors.AMBER_ACCENT_700 
            snack.open = True
            page.update()
            return

        es_valido, user_id = db.logea_usuario(email_val, clave_val)
        if es_valido:
            id_usuario = user_id[0]
            snack.content = ft.Text("¡Login exitoso!")
            snack.bgcolor = ft.Colors.GREEN_ACCENT_700
            if page.client_storage:
                page.client_storage.set("login_email", email_val)
                page.client_storage.set("login_id",id_usuario)
            page.go(home)
        else:
            snack.content = ft.Text("Usuario o contraseña incorrectos.")
            snack.bgcolor = ft.Colors.RED_ACCENT_700 
        snack.open = True
        page.update()


    # Logo o Imagen 
    img_path = "assets/imagenes/login.png"
    imagen_vista = ft.Image(
        src=img_path,
        width=400, # Ajusta el tamaño según tu imagen
        height=250,
        fit=ft.ImageFit.CONTAIN
    )

    titulo_bienvenida = ft.Text(
        "Bienvenido",
        size=28,
        weight=ft.FontWeight.BOLD,
    )

    boton_iniciar_sesion = boton_primario(
        page=page,
        text="Iniciar Sesión",
        icon=ft.Icons.LOGIN, # Icono para el botón
        width=350, 
        height=50,
        on_click=login_click
    )

    link_olvidaste_clave = ft.TextButton(
        "¿Olvidaste tu contraseña?",
        on_click=lambda _: page.go(reiniciar_clave),
    )

    link_registrate = ft.TextButton(
        "¿No tienes cuenta? Regístrate",
        on_click=lambda _: page.go(registro),
    )

    # Columna con todos los elementos del formulario
    form_column = ft.Column(
        [
            imagen_vista,
            titulo_bienvenida,
            ft.Container(height=20), # Pequeño espaciador
            correo,
            clave,
            ft.Container(height=20), # Pequeño espaciador
            boton_iniciar_sesion,
            link_olvidaste_clave,
            link_registrate     
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20 # Espacio entre los elementos de la columna
    )

    # Contenedor principal de la vista de login
    return crear_tarjeta_formulario(
        contenido=form_column,
        width=450
    )