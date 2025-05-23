import flet as ft
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_error,mensaje_snack_bar_ok
from ui_elements.botones import boton_avanzar, boton_cancelar_go
from rutas.Rutas import ruta_imagen , inicio
from db import db
import re

def registro(page: ft.Page):
    def validar_registro(e):
        
        if dropdown1.value == dropdown2.value:
            mensaje_snack_bar_error(page, "Las preguntas seleccionadas deben ser diferentes")
            return
        if not apellido.value:
            mensaje_snack_bar_error(page, "Debe ingresar un apellido para continuar")
            return
        if not nombre.value:
            mensaje_snack_bar_error(page, "Debe ingresar un nombre para continuar")
            return
        if not correo.value:
            mensaje_snack_bar_error(page, "Debe ingresar un correco para continuar")
            return
        correo_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(correo_regex, correo.value):
            mensaje_snack_bar_error(page, "El correo ingresado no tiene un formato válido")
            return
        if not contraseña.value or not confirma_contraseña.value:
            mensaje_snack_bar_error(page, "Debe completar todas las contraseñas para continuar")
            return
        if contraseña.value != confirma_contraseña.value:
            mensaje_snack_bar_error(page, "Las contraseñas ingresadas no coinciden")
            return
        if len(contraseña.value) <8:
            mensaje_snack_bar_error(page, "La contraseña debe tener al menos 8 caracteres")
            return
        if not respuesta1.value or not respuesta2.value:
            mensaje_snack_bar_error(page, "Debe responder todas las preguntas de seguridad")
            return
    
        correo_ok = db.valida_email_registro(correo.value)
        if correo_ok:
            mensaje_snack_bar_error(page,"El correo ya se encuentra registrado")
            return
        try:
            registro = db.crea_usuario(nombre.value,
                            apellido.value,
                            correo.value,
                            contraseña.value,
                            int(dropdown1.value),
                            respuesta1.value,
                            int(dropdown2.value),
                            respuesta2.value)
            if registro:
                mensaje_snack_bar_ok(page, "Te has registrado exitosamente")
                page.go(route=inicio)
        except Exception as err:
            print(f"Error al crear el usuario {err}")
            mensaje_snack_bar_error(page,"Ocurrio un error intente nuevamente")
    
    page.title= "Registro"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    snack_bar = crea_snack_bar()
    page.snack_bar = snack_bar
    page.overlay.append(snack_bar)
    preguntas_bd = db.obtiene_preguntas_seguridad_registro()
    preguntas_opciones = [
        ft.dropdown.Option(str(p["id"]), text= p["pregunta"]) for p in preguntas_bd
                          ]
    dropdown1 = ft.Dropdown(
        label = "Primera pregunta de seguridad",
        #color = "black",
        options = preguntas_opciones,
        width = 400
    )

    dropdown2 = ft.Dropdown(
        label = "Segunda pregunta de seguridad",
        #color = "black",
        options = preguntas_opciones,
        width = 400
    )

    img_path = ruta_imagen("registro.png")
    text_registro = ft.Text("Crea tu cuenta", size= 30, weight= ft.FontWeight.BOLD, color= "black")
    text_info = ft.Text("Por favor complete los siguientes datos para continuar", size= 15, weight= ft.FontWeight.BOLD, color="black")
    nombre = ft.TextField(hint_text="Ingrese su nombre", color="black")
    apellido = ft.TextField(hint_text="Ingrese su apellido", color = "black")
    correo = ft.TextField(hint_text="Ingrese su correo electronico", color = "black")
    contraseña = ft.TextField(hint_text="Ingrese su contraseña", password= True, can_reveal_password=True)
    confirma_contraseña = ft.TextField(hint_text="Confirme su contraseña", password=True, can_reveal_password=True)
    preguntas_seguridad = ft.Text("Preguntas de seguridad", size= 15, weight= ft.FontWeight.BOLD, color= "black")
    respuesta1 = ft.TextField(hint_text="Ingrese su respuesta", color= "black")
    respuesta2 = ft.TextField(hint_text="Ingrese su respuesta", color= "black")

    return ft.Container(
        ft.Column(
            [
            ft.Image(src=img_path, fit= ft.ImageFit.CONTAIN, height= 300, width=300 ),
            text_registro,
            text_info,
            nombre,
            apellido,
            correo,
            contraseña,
            confirma_contraseña,
            preguntas_seguridad,
            ft.Row(
                controls=[
                    ft.Container(dropdown1,width=450),
                    ft.Container(respuesta1,width=330)
                          ],
                          alignment=ft.MainAxisAlignment.CENTER,
                          spacing=20        
            ),
            ft.Row(
                controls=[
                    ft.Container(dropdown2,width=450),
                    ft.Container(respuesta2,width=330)
                    ],
                    alignment= ft.MainAxisAlignment.CENTER,
                    spacing=20
            ),
            ft.Row(
                controls=[
                    boton_avanzar("Confirmar", validar_registro),
                    boton_cancelar_go("Cancelar",inicio, page)
                ],
                alignment = ft.MainAxisAlignment.CENTER                         
            ),
            ],
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
        width= 800,
        height= 900
    )