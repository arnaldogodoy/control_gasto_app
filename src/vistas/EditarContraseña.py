# vistas/EditarContraseña.py
import flet as ft
from ui_elements.botones import boton_primario, boton_cancelar_navegacion
from rutas.Rutas import inicio 
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_error, mensaje_snack_bar_ok, crear_tarjeta_formulario
from db import db

def editar_contraseña(page: ft.Page):
    
    snack_bar_control = crea_snack_bar() 
    if snack_bar_control not in page.overlay:
        page.overlay.append(snack_bar_control)

    def validar_contraseña_click(e):
        email = getattr(page, "email_sesion", None)
        if not email: # Importante: manejar el caso donde el email no esté en la sesión
            mensaje_snack_bar_error(page, "Error de sesión. No se pudo identificar el usuario.")
            return

        nueva = nueva_contraseña.value.strip()
        confirmar = confirmar_contraseña.value.strip()

        # Valida que los campos no estén vacíos
        if not nueva or not confirmar:
            mensaje_snack_bar_error(page, "Los campos de contraseña no pueden estar vacíos.")
            nueva_contraseña.error_text = "Este campo es requerido" if not nueva else None
            confirmar_contraseña.error_text = "Este campo es requerido" if not confirmar else None
            page.update()
            return
        else: # Limpiar errores si los campos ya están llenos
            nueva_contraseña.error_text = None
            confirmar_contraseña.error_text = None

        if " " in nueva: # No permitir espacios solo en la nueva, la confirmación se validará por igualdad
            mensaje_snack_bar_error(page, "La contraseña no debe contener espacios.")
            nueva_contraseña.error_text = "No se permiten espacios."
            page.update()
            return
        else:
            nueva_contraseña.error_text = None
        
        if len(nueva) < 8: # Caracteres obligatorios
            mensaje_snack_bar_error(page, "La contraseña debe tener al menos 8 caracteres.")
            nueva_contraseña.error_text = "Mínimo 8 caracteres."
            page.update()
            return
        else:
            nueva_contraseña.error_text = None

        vieja_contraseña_data = db.obtiene_contraseña_por_usuario(email)
        if vieja_contraseña_data and nueva == vieja_contraseña_data.get("password"): # No permitir que se introduzca la misma contraseña
            mensaje_snack_bar_error(page, "La nueva contraseña no puede ser igual a la contraseña actual.")
            nueva_contraseña.error_text = "No puede ser igual a la actual."
            page.update()
            return
        else:
            nueva_contraseña.error_text = None

        if nueva != confirmar: # Validar que las contraseñas ingresadas sean identicas
            mensaje_snack_bar_error(page, "Las contraseñas ingresadas no coinciden.")
            confirmar_contraseña.error_text = "Las contraseñas no coinciden."
            page.update()
            return
        else:
            confirmar_contraseña.error_text = None
        
        page.update() # Actualizar para limpiar cualquier error_text previo si todo está bien hasta aquí

        if db.actualiza_contraseña_por_usuario(nueva, email):
            mensaje_snack_bar_ok(page, "Contraseña actualizada exitosamente.")
            page.go(inicio)
        else:
            mensaje_snack_bar_error(page, "Ocurrió un error al actualizar. Intente nuevamente.")

    
    img_path = "assets/imagenes/restaura_clave.png" 
    imagen_vista = ft.Image(
        src=img_path,
        width=400, 
        height=250,
        fit=ft.ImageFit.CONTAIN
    )

    titulo_vista = ft.Text(
        "Cambiar Contraseña", 
        size=24, 
        weight=ft.FontWeight.BOLD,
    )

    nueva_contraseña = ft.TextField(
        label="Nueva contraseña", 
        password=True,
        can_reveal_password=True,
        max_length=200,
        prefix_icon=ft.Icons.LOCK_OUTLINE, 
        border_radius=ft.border_radius.all(10) # Bordes redondeados
    )

    confirmar_contraseña = ft.TextField(
        label="Confirmar nueva contraseña", 
        password=True,
        can_reveal_password=True,
        max_length=200,
        prefix_icon=ft.Icons.LOCK_OUTLINE, 
        border_radius=ft.border_radius.all(10) # Bordes redondeados
    )

    boton_confirmar = boton_primario(
        page=page,
        text="Confirmar",
        on_click=validar_contraseña_click,
        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        width=180
    )
    
    boton_cancelar = boton_cancelar_navegacion(
        page=page,
        text="Cancelar",
        ruta_destino=inicio,
        icon=ft.Icons.CANCEL_OUTLINED,
        width=180
    )
    
    # --- Layout de la Columna del Formulario ---
    form_column = ft.Column(
        [
            imagen_vista,
            titulo_vista,
            ft.Container(height=15), # Espaciador
            nueva_contraseña,
            confirmar_contraseña,
            ft.Container(height=20), # Espaciador
            ft.Row(
                controls=[
                    boton_cancelar,
                    boton_confirmar
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                spacing=10 # Espacio entre botones
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=15 # Espacio entre los elementos principales de la columna
    )

    # --- Contenedor Principal ---
    return crear_tarjeta_formulario(
        contenido=form_column,
        width=450
    )