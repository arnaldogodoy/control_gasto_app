import flet as ft
from db import db
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_ok, mensaje_snack_bar_error, crear_tarjeta_formulario
from ui_elements.botones import boton_primario, boton_cancelar_navegacion
from db import db
from rutas.Rutas import home

def agregar_tarjeta(page : ft.Page):
    snack = crea_snack_bar()
    page.snack_bar = snack
    if snack not in page.overlay:
        page.overlay.append(snack)  

    ancho_max_campos = 900

    def guarda_tarjeta_credito(e):
        try: 
            guardar_tarjeta = db.crea_tarjeta_credito(
                id_usuario=page.client_storage.get("login_id"),
                ultimos_numeros= int(ultimos_numeros.value),
                id_tipo= int(tipo_tarjeta.value),
                id_banco= int(banco_tarjeta.value),
                fecha_vencimiento_tarjeta= fecha_vencimiento_tarjeta.value.strip(),
                dia_cierre_resumen = int(fecha_cierre_resumen.value),
                dia_vencimiento_resumen = int(fecha_vencimiento_resumen.value),
                limite_credito= int(limite_tarjeta.value),
                alias = alias.value.strip()
            )
            if guardar_tarjeta:
                mensaje_snack_bar_ok(page,"Se agrego la tarjeta de credito correctamente")
            else:
                mensaje_snack_bar_error(page,"No se puedo agregar la tarjeta de credito, intente nuevamente")
        except Exception as er:
            print(f"Error al agregar tarjeta: {er}")
            mensaje_snack_bar_error(page,"Ocurrio un error intente nuevamente")

    ultimos_numeros = ft.TextField(
        label="Ultimos 4 digitos",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.NUMBERS_ROUNDED,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=4,
        width= ancho_max_campos
    )

    fecha_vencimiento_tarjeta = ft.TextField(
        label="Fecha de vencimiento de la tarjeta",
        hint_text= "Ej : 12-31",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CALENDAR_MONTH_OUTLINED,
        width= ancho_max_campos,
        max_length=5
    )

    alias = ft.TextField(
        label="Alias para la tarjeta",
        hint_text="Ej : Visa viajes",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CREDIT_SCORE_ROUNDED,
        width= ancho_max_campos
    )
    
    limite_tarjeta = ft.TextField(
        label="Limite de credito",
        prefix= "$",
        keyboard_type= ft.KeyboardType.NUMBER,
        prefix_icon= ft.Icons.ATTACH_MONEY_ROUNDED,
        border_radius=ft.border_radius.all(10),
        width= ancho_max_campos
    )

    fecha_cierre_resumen = ft.TextField(
        label="Dia de cierre del resumen",
        hint_text= "Ej: 27",
        max_length=2,
        keyboard_type= ft.KeyboardType.NUMBER,
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CALENDAR_MONTH_OUTLINED,
        width= ancho_max_campos
    )

    fecha_vencimiento_resumen = ft.TextField(
        label="Dia de vencimiento del resumen",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CALENDAR_MONTH_OUTLINED,
        width= ancho_max_campos,
        keyboard_type= ft.KeyboardType.NUMBER,
        max_length=2,
        hint_text="Ej: 08"
    )

    vista_titulo = ft.Text(
        "Añadir una nueva tarjeta",
        size=28,
        weight=ft.FontWeight.BOLD 
    )

    def obtiene_tipos_tarjetas():
        tipos = db.obtiene_tipos_tarjetas()
        if not tipos :
            return [ft.dropdown.Option(key="NO_KEY",text="No hay tipos disponibles")]
        else:
            return [ft.dropdown.Option(key=str(t["id"]),text=(t["tipo"])) for t in tipos]

    tipo_tarjeta= ft.Dropdown(
        label= "Tipo",
        options= obtiene_tipos_tarjetas(),
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CREDIT_CARD_OUTLINED,
        width= ancho_max_campos               
    )
    
    def obtiene_bancos():
        bancos = db.obtiene_bancos()
        if not bancos:
            return [ft.dropdown.Option(key="NO_KEY",text="No hay bancos disponibles")]
        else:
            return [ft.dropdown.Option(key=str(b["id"]),text=(b["banco"])) for b in bancos]
        
    banco_tarjeta = ft.Dropdown(
        label= "Banco",
        options= obtiene_bancos(),
        border_radius= ft.border_radius.all(10),

        leading_icon=ft.Icons.SEARCH,
        editable=True,
        enable_filter=True,
        menu_height=250,
        width= ancho_max_campos        
    )


    boton_agregar_tarjeta = boton_primario(
        page=page,
        text="Guardar tarjeta",
        icon= ft.Icons.SAVE_OUTLINED,
        on_click= guarda_tarjeta_credito,
        disabled=True
    )

    boton_cancelar = boton_cancelar_navegacion(
        page=page,
        text="Cancelar",
        ruta_destino= home ,
        icon= ft.Icons.CANCEL_OUTLINED,   
    )

    def validar_datos_registro(e = None):
        valido_ultimos_numeros = ultimos_numeros.value and len(ultimos_numeros.value) == 4 and ultimos_numeros.value.strip().isdigit()
        valido_limite_tarjeta = limite_tarjeta.value and limite_tarjeta.value.strip().isdigit()
        valido_alias = alias.value
        valido_banco = banco_tarjeta.value is not None and banco_tarjeta.value != "NO_KEY"
        valido_fecha_vencimiento_tarjeta = fecha_vencimiento_tarjeta.value and len(fecha_vencimiento_tarjeta.value) == 5
        valido_limite_tarjeta = limite_tarjeta.value and limite_tarjeta.value.strip().replace(".",",",1).isdigit()
        try:
            dia_cierre = int(fecha_cierre_resumen.value.strip()) if fecha_cierre_resumen.value else 0
            valido_cierre = 1 <= dia_cierre <= 31
        except ValueError:
            valido_cierre = False
        try:
            dia_vence = int(fecha_vencimiento_resumen.value.strip()) if fecha_vencimiento_resumen.value else 0
            valido_vence = 1 <= dia_vence <= 31
        except ValueError:
            valido_vence = False
        
        todos_completos_validos = all([
            valido_banco,
            valido_alias,
            valido_cierre,
            valido_fecha_vencimiento_tarjeta,
            valido_cierre,
            valido_limite_tarjeta,
            valido_ultimos_numeros,
            valido_vence
        ])
        
        boton_agregar_tarjeta.disabled = not todos_completos_validos
        if boton_agregar_tarjeta.page:
            boton_agregar_tarjeta.update()

    ultimos_numeros.on_change = validar_datos_registro
    tipo_tarjeta.on_change = validar_datos_registro
    banco_tarjeta.on_change = validar_datos_registro
    fecha_cierre_resumen.on_change = validar_datos_registro
    fecha_vencimiento_resumen.on_change = validar_datos_registro
    fecha_vencimiento_tarjeta.on_change = validar_datos_registro
    limite_tarjeta.on_change=validar_datos_registro
    alias.on_change = validar_datos_registro

    form_colum_nueva_tarjeta = ft.Column(
        [
            vista_titulo,
            tipo_tarjeta,
            banco_tarjeta,
            alias,
            ultimos_numeros,
            limite_tarjeta,
            fecha_vencimiento_tarjeta,
            fecha_vencimiento_resumen,
            fecha_cierre_resumen,
            ft.Row(
                [boton_cancelar, boton_agregar_tarjeta],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=10
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    return crear_tarjeta_formulario(
        contenido= form_colum_nueva_tarjeta,
        width= 900
    )