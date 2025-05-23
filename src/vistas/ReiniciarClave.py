import flet as ft
from db import db
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_ok, mensaje_snack_bar_error
from ui_elements.botones import boton_avanzar, boton_cancelar_go
from rutas.Rutas import inicio, editar_contraseña , ruta_imagen


def reiniciar_clave(page: ft.Page):
    page.title = "Reiniciar Contraseña"    
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    img_path = ruta_imagen("restaura_clave.png")
    correo = ft.TextField(hint_text = "Ingrese su correo electronico")
    page.snack_bar = crea_snack_bar()
    page.overlay.append(page.snack_bar)

    recuperacion = ft.Text("Recuperación de contraseña", size = 20 , weight = ft.FontWeight.BOLD, color = "Black")
    respuesta1 = ft.TextField(hint_text = "Respuesta 1", visible= False, )
    respuesta2 = ft.TextField(hint_text = "Respuesta 2", visible= False, )
    responder = ft.Text("Preguntas de seguridad", size= 20 , weight=  ft.FontWeight.BOLD, visible= False, color = "Black")

    def busca_pregunta_usuario_click(e):
        preguntas = db.obtiene_preguntas_por_usuario(correo.value)
        if preguntas:
            respuesta1.hint_text = preguntas[0]
            respuesta1.visible = True
            respuesta2.hint_text = preguntas[1]
            respuesta2.visible = True
            boton_continuar.visible = False
            responder.visible = True
            recuperacion.visible = False
            correo.visible = False
            boton_validar_respuesta.visible = True
            boton_cancelar2.visible = True
            boton_cancelar.visible = False
            page.update()
        else:
            mensaje_snack_bar_error(page, "Correo no encontrado o sin preguntas asociadas")
    
    def valida_respuesta_click(e):
        if db.validar_preguntas(correo.value, respuesta1.value, respuesta2.value):
            mensaje_snack_bar_ok(page, "Se validaron las respuestas correctamente")
            page.email_sesion = correo.value
            page.go(editar_contraseña)
        else:
            mensaje_snack_bar_error(page,"Las respuestas no son correctas")


    boton_validar_respuesta = boton_avanzar(text= "Confirmar", click = valida_respuesta_click, visible = False)     
    boton_continuar = boton_avanzar("Continuar", busca_pregunta_usuario_click)
    boton_cancelar = boton_cancelar_go("Cancelar", inicio, page)
    boton_cancelar2 = boton_cancelar_go("Cancelar", inicio, page , visible= False)
    

    return ft.Container(
        ft.Column(
            [
                ft.Image(src = img_path, width= 300, height= 300, fit= ft.ImageFit.CONTAIN),
                recuperacion,
                correo,                
                ft.Row(
                    controls = [
                    boton_continuar,
                    boton_cancelar
                    ]
                ),
                responder,
                respuesta1,
                respuesta2,
                ft.Row(
                    controls = [boton_validar_respuesta,boton_cancelar2]
                )               
            ],
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
        width= 400,
        height= 700
    )