import flet as ft
from db import db
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_ok, mensaje_snack_bar_error, crear_tarjeta_formulario
from ui_elements.botones import boton_primario, boton_cancelar_navegacion
from rutas.Rutas import inicio, editar_contraseña , ruta_imagen


def reiniciar_clave(page: ft.Page):
    img_path = "assets/imagenes/restaura_clave.png"
    imagen_vista = ft.Image(
        src= img_path,
        height= 250,
        width= 400,
        fit= ft.ImageFit.CONTAIN
    )

    titulo_dinamico = ft.Text(
        "Recuperación de contraseña",
        size= 22,
        weight= ft.FontWeight.BOLD,
        text_align= ft.TextAlign.CENTER
    )    

    correo = ft.TextField(
        label="Correo electrónico",
        prefix_icon=ft.Icons.EMAIL_ROUNDED,
        border_radius= ft.border_radius.all(10), #Bordes redondeados        
        keyboard_type= ft.KeyboardType.EMAIL
    )
    
    snack = crea_snack_bar()
    page.snack_bar = snack
    if snack not in page.overlay:
        page.overlay.append(snack)
    
    pregunta1_texto= ft.Text(
        weight=ft.FontWeight.W_500,
        size= 15,
        visible= False
    )

    respuesta1 = ft.TextField(
        label= "Respuesta 1",
          visible= False,
          prefix_icon=ft.Icons.QUESTION_ANSWER_ROUNDED,
          border_radius= ft.border_radius.all(10) #Bordes redondeados          
    )

    pregunta2_texto= ft.Text(
        weight=ft.FontWeight.W_500,
        size= 15,
        visible= False
    )

    respuesta2 = ft.TextField(
        label= "Respuesta 2", 
        visible= False,
        prefix_icon=ft.Icons.QUESTION_ANSWER_ROUNDED,
        border_radius = ft.border_radius.all(10) #Bordes redondeados
    )
    
    def mostrar_paso_preguntas(preguntas_db):
        titulo_dinamico.value = "Preguntas de Seguridad"
        correo.visible = False
        boton_continuar.visible = False
        boton_cancelar_inicial.visible = False # Ocultar el primer botón de cancelar

        pregunta1_texto.value = preguntas_db[0]
        pregunta1_texto.visible = True
        respuesta1.visible = True
        # respuesta1.label = preguntas_db[0] # Si prefieres poner la pregunta en el label
        
        pregunta2_texto.value = preguntas_db[1]
        pregunta2_texto.visible = True
        respuesta2.visible = True
        # respuesta2.label = preguntas_db[1]

        boton_validar_respuestas.visible = True
        boton_cancelar_preguntas.visible = True
        page.update()


    def mostrar_paso_email(e):
        titulo_dinamico.value = "Recuperación de Contraseña"
        correo.visible = True
        boton_continuar.visible = True
        boton_cancelar_inicial.visible = True

        pregunta1_texto.visible = False
        respuesta1.visible = False
        respuesta1.value = "" # Limpiar campos
        respuesta1.error_text = None
        
        pregunta2_texto.visible = False
        respuesta2.visible = False
        respuesta2.value = "" # Limpiar campos
        respuesta2.error_text = None

        boton_validar_respuestas.visible = False
        boton_cancelar_preguntas.visible = False
        page.update()

    def busca_pregunta_usuario_click(e):
        email_val = correo.value.strip()
        if not email_val:
            correo.error_text = "Por favor, ingresa tu correo."
            mensaje_snack_bar_error(page, "El campo de correo no puede estar vacío.")
            page.update()
            return
        correo.error_text = None # Limpiar error si lo hay

        preguntas = db.obtiene_preguntas_por_usuario(email_val)
        if preguntas and len(preguntas) >= 2:
            mostrar_paso_preguntas(preguntas)
        else:
            mensaje_snack_bar_error(page, "Correo no encontrado o sin suficientes preguntas asociadas.")
            correo.error_text = "Correo no válido o sin preguntas."
        page.update()
    
    def valida_respuesta_click(e):
        resp1_val = respuesta1.value.strip()
        resp2_val = respuesta2.value.strip()

        if not resp1_val or not resp2_val:
            respuesta1.error_text = "Campo requerido" if not resp1_val else None
            respuesta2.error_text = "Campo requerido" if not resp2_val else None
            mensaje_snack_bar_error(page, "Ambas respuestas son requeridas.")
            page.update()
            return
        respuesta1.error_text = None
        respuesta2.error_text = None
        
        if db.validar_preguntas(correo.value, resp1_val, resp2_val):
            mensaje_snack_bar_ok(page, "Se validaron las respuestas correctamente.")
            page.email_sesion = correo.value # Guardar el email para la siguiente vista
            page.go(editar_contraseña) # Navegar a la vista de editar contraseña
        else:
            mensaje_snack_bar_error(page,"Las respuestas no son correctas. Intenta de nuevo.")
            # Podrías querer limpiar los campos o marcarlos con error aquí también
        page.update()


    boton_validar_respuestas = boton_primario(
                                            page=page,
                                            text= "Confirmar",
                                            on_click= valida_respuesta_click,
                                            visible = False,
                                            icon= ft.Icons.CHECK_CIRCLE_OUTLINE,
                                            width=180
                                            )     
    
    boton_continuar = boton_primario(
                                    page=page,
                                    text="Continuar",
                                    on_click=busca_pregunta_usuario_click,
                                    icon=ft.Icons.ARROW_FORWARD_IOS_ROUNDED,
                                    width=180
                                    )
    
    boton_cancelar_inicial = boton_cancelar_navegacion(
                                            page=page,
                                            text="Cancelar",
                                            ruta_destino= inicio,
                                            icon=ft.Icons.CANCEL_OUTLINED,
                                            width=180
                                            )
    
    boton_cancelar_preguntas = boton_cancelar_navegacion(
                                                page=page,
                                                text="Volver", 
                                                ruta_destino=inicio, 
                                                icon= ft.Icons.ARROW_BACK_IOS_ROUNDED, 
                                                visible= False,
                                                width=180
                                            )
    
    form_colum = ft.Column(
        [
            imagen_vista,
            titulo_dinamico,
            ft.Container(height=15),#Espaciador
            correo,                
            ft.Row(
                controls = [
                boton_cancelar_inicial,
                boton_continuar
                ],
                alignment= ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            pregunta1_texto,
            respuesta1,
            pregunta2_texto,
            respuesta2,
            ft.Row(
                controls = [boton_cancelar_preguntas,boton_validar_respuestas],
                alignment= ft.MainAxisAlignment.CENTER,
                spacing=10
            )               
        ],
        horizontal_alignment= ft.CrossAxisAlignment.CENTER,
        spacing=12
    )

    return crear_tarjeta_formulario(
        contenido= form_colum,
        width=450
    )