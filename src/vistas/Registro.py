import flet as ft
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_error,mensaje_snack_bar_ok, crear_tarjeta_formulario
from ui_elements.botones import boton_primario, boton_cancelar_navegacion
from rutas.Rutas import ruta_imagen , inicio
from db import db
import re

def registro(page: ft.Page):
    snack = crea_snack_bar()
    page.snack_bar = snack
    if snack not in page.overlay:
        page.overlay.append(snack)    
    
    def limpiar_errores():
        nombre.error_text = None
        apellido.error_text = None
        correo.error_text = None
        contraseña.error_text = None
        confirma_contraseña.error_text = None
        dropdown1.error_text = None
        dropdown2.error_text = None
        respuesta1.error_text = None
        respuesta2.error_text = None
        page.update()    
    
    def validar_registro(e):
        limpiar_errores() # Limpiar errores previos
        error_encontrado = False

        # Validaciones individuales con error_text
        if not nombre.value.strip():
            nombre.error_text = "El nombre es requerido."
            error_encontrado = True
        if not apellido.value.strip():
            apellido.error_text = "El apellido es requerido."
            error_encontrado = True
        if not correo.value.strip():
            correo.error_text = "El correo es requerido."
            error_encontrado = True
        else:
            correo_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            if not re.match(correo_regex, correo.value.strip()):
                correo.error_text = "Formato de correo no válido."
                error_encontrado = True
            elif db.valida_email_registro(correo.value.strip()): # Validar si el correo ya existe
                correo.error_text = "Este correo ya está registrado."
                error_encontrado = True
        
        if not contraseña.value: # No usamos strip() para contraseñas
            contraseña.error_text = "La contraseña es requerida."
            error_encontrado = True
        elif len(contraseña.value) < 8:
            contraseña.error_text = "Mínimo 8 caracteres."
            error_encontrado = True
        
        if not confirma_contraseña.value:
            confirma_contraseña.error_text = "Confirmar la contraseña es requerido."
            error_encontrado = True
        elif contraseña.value != confirma_contraseña.value:
            confirma_contraseña.error_text = "Las contraseñas no coinciden."
            error_encontrado = True
        
        if not dropdown1.value:
            dropdown1.error_text = "Selecciona una pregunta."
            error_encontrado = True
        if not respuesta1.value.strip():
            respuesta1.error_text = "La respuesta es requerida."
            error_encontrado = True
        
        if not dropdown2.value:
            dropdown2.error_text = "Selecciona una pregunta."
            error_encontrado = True
        if not respuesta2.value.strip():
            respuesta2.error_text = "La respuesta es requerida."
            error_encontrado = True
        
        if dropdown1.value and dropdown2.value and dropdown1.value == dropdown2.value:
            # Podríamos poner el error en ambos dropdowns o en uno general
            dropdown2.error_text = "Las preguntas deben ser diferentes."
            # mensaje_snack_bar_error(page, "Las preguntas seleccionadas deben ser diferentes") # Ya no necesario si hay error_text
            error_encontrado = True

        if error_encontrado:
            mensaje_snack_bar_error(page, "Por favor, corrige los errores indicados.")
            page.update() # Actualizar para mostrar todos los error_text
            return

        # Si no hay errores, proceder con el registro
        try:
            registro_exitoso = db.crea_usuario(
                nombre.value.strip(),
                apellido.value.strip(),
                correo.value.strip(),
                contraseña.value, # Sin strip
                int(dropdown1.value),
                respuesta1.value.strip(),
                int(dropdown2.value),
                respuesta2.value.strip()
            )
            if registro_exitoso:
                mensaje_snack_bar_ok(page, "¡Te has registrado exitosamente!")
                page.go(route=inicio)
            else: # Caso en que db.crea_usuario devuelva False o None sin una excepción
                mensaje_snack_bar_error(page, "No se pudo completar el registro. Intenta nuevamente.")
        except Exception as err:
            print(f"Error al crear el usuario: {err}") # Mantener log para depuración
            mensaje_snack_bar_error(page, "Ocurrió un error inesperado. Intenta nuevamente.")

    preguntas_bd = db.obtiene_preguntas_seguridad_registro()
    preguntas_opciones = [
        ft.dropdown.Option(str(p["id"]), text= p["pregunta"]) for p in preguntas_bd
                          ]
    
    dropdown1 = ft.Dropdown(
        label = "Primera pregunta de seguridad",
        options = preguntas_opciones,
        border_radius=ft.border_radius.all(10),#bordes
        prefix_icon= ft.Icons.QUESTION_MARK_ROUNDED,
        width=440
    )

    dropdown2 = ft.Dropdown(
        label = "Segunda pregunta de seguridad",
        options = preguntas_opciones,
        border_radius= ft.border_radius.all(10),#Bordes
        prefix_icon= ft.Icons.QUESTION_MARK_ROUNDED,
        width= 440
    )

    img_path = "assets/imagenes/registro.png"
    imagen_vista = ft.Image(
        src=img_path,
        width=450,
        height=250,
        fit = ft.ImageFit.CONTAIN
    )



    text_registro = ft.Text(
        "Crea tu cuenta", 
        size= 26, 
        weight= ft.FontWeight.BOLD, 
        text_align=ft.TextAlign.CENTER
        )
    
    text_info = ft.Text("Por favor complete los siguientes datos para continuar", 
                        size= 16, 
                        text_align= ft.TextAlign.CENTER,
                        italic=True
                        )

    nombre = ft.TextField(
        label="Nombre",
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius= ft.border_radius.all(10),#Bordes redondeados
        capitalization= ft.TextCapitalization.WORDS
        )

    apellido = ft.TextField(
        label="Apellido", 
        prefix_icon=ft.Icons.PERSON_OUTLINE,
        border_radius=ft.border_radius.all(10),#Bordes redondeados
        capitalization= ft.TextCapitalization.WORDS
        )
    
    correo = ft.TextField(
        label="Correo electronico",
        prefix_icon= ft.Icons.EMAIL_OUTLINED,
        capitalization=ft.TextCapitalization.WORDS,
        border_radius=ft.border_radius.all(10)#Bordes redondeados
        )

    contraseña = ft.TextField(
        label="Ingrese su contraseña", 
        password= True, 
        can_reveal_password=True,
        prefix_icon=ft.Icons.LOCK_OUTLINE,
        border_radius=ft.border_radius.all(10)#Bordes redondeados
        )

    confirma_contraseña = ft.TextField(label="Confirme su contraseña", 
                                       password=True, 
                                       can_reveal_password=True,
                                       prefix_icon=ft.Icons.LOCK_OUTLINE,
                                       border_radius=ft.border_radius.all(10)#Bordes redondeados
                                       )
    
    preguntas_seguridad = ft.Text(
                                "Preguntas de seguridad", 
                                size= 18, 
                                weight= ft.FontWeight.BOLD, 
                                )
    
    respuesta1 = ft.TextField(
        label="Respuesta a la primera pregunta de seguridad",
        prefix_icon=ft.Icons.QUESTION_ANSWER_ROUNDED,
        border_radius= ft.border_radius.all(10),#Bordes redondeados
        )
    respuesta2 = ft.TextField(
        label="Respuesta a la segunda pregunta de seguridad",
        prefix_icon=ft.Icons.QUESTION_ANSWER_ROUNDED,
        border_radius= ft.border_radius.all(10),#Bordes redondeados
        )

    boton_avanzar = boton_primario(
        page=page,
        text="Confirmar", 
        on_click=validar_registro,
        icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
        width=180
    )
    
    boton_cancelar = boton_cancelar_navegacion(
        text="Cancelar",
        ruta_destino=inicio, 
        page=page,
        icon=ft.Icons.CANCEL_OUTLINED,
        width=180)

    form_colum = ft.Column(
            [
            imagen_vista,
            text_registro,
            text_info,
            ft.Divider(height=10, color=ft.Colors.TRANSPARENT),#Espaciador
            nombre,
            apellido,
            correo,
            contraseña,
            confirma_contraseña,
            ft.Divider(height=10, color= ft.Colors.TRANSPARENT),#Espaciador
            preguntas_seguridad,
            dropdown1,
            respuesta1,
            dropdown2,
            respuesta2,
            ft.Divider(height=20, color = ft.Colors.TRANSPARENT),#Espaciador
            ft.Row(
                controls=[
                    boton_cancelar,
                    boton_avanzar,
                ],
                alignment = ft.MainAxisAlignment.CENTER,
                spacing=10
            ),
            ],
            spacing=12,
            scroll= ft.ScrollMode.ADAPTIVE,
            expand=True   
        )
    
    return crear_tarjeta_formulario(
        contenido=form_colum,
        width=500,
        height=850
    )
