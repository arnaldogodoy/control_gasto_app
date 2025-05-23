import flet as ft
from ui_elements.botones import boton_avanzar, boton_cancelar_go
from rutas.Rutas import inicio , ruta_imagen
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_error, mensaje_snack_bar_ok
from db import db

def editar_contraseña(page : ft.Page):
    def validar_contraseña_click(e):
        email = getattr(page, "email_sesion", None)
        nueva = nueva_contraseña.value.strip()
        confirmar = confirmar_contraseña.value.strip()

        # Valida que los campos no estén vacíos ni contengan solo espacios
        if not nueva or not confirmar:
            mensaje_snack_bar_error(page, "Los campos no pueden estar vacíos o tener solo espacios")
            return
        
        if " " in nueva or " " in confirmar:
            mensaje_snack_bar_error(page, "La contraseña no debe contener espacios")
            return

        # Valida longitud mínima
        if len(nueva) < 8:
            mensaje_snack_bar_error(page, "La contraseña debe tener al menos 8 caracteres")
            return

        # Verificar si la nueva contraseña es igual a la actual
        vieja_contraseña = db.obtiene_contraseña_por_usuario(email)
        if nueva == vieja_contraseña["password"]:
            mensaje_snack_bar_error(page, "La contraseña ingresada es igual a la actual")
            return

        # Verificar coincidencia
        if nueva != confirmar:
            mensaje_snack_bar_error(page, "Las contraseñas ingresadas no coinciden")
            return

        # Actualizar si todo es válido
        if db.actualiza_contraseña_por_usuario(nueva, email):
            mensaje_snack_bar_ok(page, "Contraseña actualizada exitosamente")
            page.go(inicio)
        else:
            mensaje_snack_bar_error(page, "Ocurrió un error, intente nuevamente")

    
    page.title = 'Editar contraseña'
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    snack_bar = crea_snack_bar()
    page.overlay.append(snack_bar)

    img_path = ruta_imagen("restaura_clave.png")
    text_contraseña = ft.Text("Cambio de contraseña", size= 20 , weight= ft.FontWeight.BOLD, color="black")
    nueva_contraseña = ft.TextField(hint_text="Ingrese su nueva contraseña", password= True, can_reveal_password= True, max_length=200, )
    confirmar_contraseña = ft.TextField(hint_text="Ingrese nueva contraseña nuevamente", password= True, can_reveal_password=True, max_length=200)
    boton_confirmar = boton_avanzar("Confirmar", validar_contraseña_click)
    boton_cancelar = boton_cancelar_go("Cancelar", inicio, page)

    return ft.Container(
        ft.Column(
            [
                ft.Image(src = img_path, width= 300, height= 300, fit = ft.ImageFit.CONTAIN),
                text_contraseña,
                nueva_contraseña,
                confirmar_contraseña,
                ft.Row(
                    controls=[boton_confirmar,boton_cancelar]
                )
            ],alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
        width= 400,
        height= 700
    )
