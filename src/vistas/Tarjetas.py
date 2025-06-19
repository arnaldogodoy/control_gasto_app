import flet as ft
from db import db
from rutas.Rutas import agregar_tarjeta
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_error, mensaje_snack_bar_ok

def tarjetas(page : ft.Page):

    #---- SNACK BAR ----
    
    snack= crea_snack_bar()
    page.snack_bar = snack
    if snack not in page.overlay:
        page.overlay.append(snack)

    #---- CONTENEDOR PARA LOS LAYOUTS DE TARJETAS ----

    listado_tarjetas = ft.Row(
        wrap=True,
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 20,
        run_spacing=5,
        width=1200
    )

    #---- BOTON PARA NUEVA TARJETA ----
    def ir_agregar_tarjeta(e):
        page.go(route=agregar_tarjeta)
    
    boton_nueva_tarjeta = ft.FloatingActionButton(
        icon=ft.Icons.ADD_CARD_ROUNDED,
        text="Añadir Tarjeta",
        on_click=ir_agregar_tarjeta,
    )
        
    #Variable que almacenera el id de tarjeta a eliminar / editar
    id_tarjeta_seleccionada = ft.Ref[int]()
    
    #---- EDITAR TARJETA ----

    # CAMPOS A EDITAR

    alias = ft.TextField(
        label="Alias para la tarjeta",
        hint_text="Ej : Visa viajes",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CREDIT_SCORE_ROUNDED,
    )

    limite_tarjeta = ft.TextField(
        label="Limite de credito",
        prefix= "$",
        keyboard_type= ft.KeyboardType.NUMBER,
        prefix_icon= ft.Icons.ATTACH_MONEY_ROUNDED,
        border_radius=ft.border_radius.all(10),
    )

    fecha_cierre_resumen = ft.TextField(
        label="Dia de cierre del resumen",
        hint_text= "Ej: 27",
        max_length=2,
        keyboard_type= ft.KeyboardType.NUMBER,
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CALENDAR_MONTH_OUTLINED,
    )

    fecha_vencimiento_resumen = ft.TextField(
        label="Dia de vencimiento del resumen",
        border_radius= ft.border_radius.all(10),
        prefix_icon= ft.Icons.CALENDAR_MONTH_OUTLINED,
        keyboard_type= ft.KeyboardType.NUMBER,
        max_length=2,
        hint_text="Ej: 08",
    )

    modal_editar = ft.BottomSheet(
        content= ft.Container(
            ft.Column(
                [
                    ft.Text("Editar Tarjeta", size= 18, weight= ft.FontWeight.BOLD),
                    alias,
                    limite_tarjeta,
                    fecha_cierre_resumen,
                    fecha_vencimiento_resumen,
                    ft.Row(
                        [
                            ft.FilledButton("Guardar Cambios", on_click= lambda e : editar_tarjeta(e)),
                            ft.TextButton("Cancelar", on_click= lambda e : cierra_modal_editar(e))
                        ],
                        alignment= ft.CrossAxisAlignment.END
                    )
                ],
                tight=True
            ),
            padding= 20,
        ),
        open=False
    )

    #Agregamos el boton a la pagina
    page.overlay.append(modal_editar)

    def abre_modal_editar(e,tarjeta : dict):
        id_tarjeta_seleccionada.current = tarjeta.get("id_tarjeta")
        alias.value = tarjeta.get("alias","")
        fecha_cierre_resumen.value = str(tarjeta.get("dia_cierre_resumen","0"))
        fecha_vencimiento_resumen.value = str(tarjeta.get("dia_vence_resumen","0"))
        limite_tarjeta.value = str(tarjeta.get("limite","0"))
        modal_editar.open = True
        page.update()       

    def cierra_modal_editar(e):
        modal_editar.open = False
        page.update()

    def editar_tarjeta(id_tarjeta : int):
        print(f"El usuario quiere editar la tarjeta ID : {id_tarjeta}")
    
    #---- ELIMINAR TARJETA ----
    
    modal_eliminar= ft.AlertDialog(
        modal=True,
        title= ft.Text("Confirmar Eliminación"),
        content=ft.Text("¿Estas seguro que deseas eliminar esta tarjeta?"),
        actions=[
            ft.TextButton(text="Cancelar", on_click= lambda e: cierra_modal_eliminar(e)),
            ft.TextButton(text="Eliminar", on_click= lambda e: eliminar_tarjeta(e)),
        ],
        actions_alignment= ft.MainAxisAlignment.END
    )

    def cierra_modal_eliminar(e):
        modal_eliminar.open = False
        page.update()
    
    def abre_modal_eliminar(e, id_tarjeta):
        id_tarjeta_seleccionada.current= id_tarjeta
        page.open(modal_eliminar)
    
    def actualiza_listado_tarjetas():
        listado_tarjetas.clean()
        cargar_tarjetas_en_listado()

    def eliminar_tarjeta(e):
        try:
            id_tarjeta = id_tarjeta_seleccionada.current
            id_usuario = page.client_storage.get("login_id")
            eliminar = db.deshabilita_usuario_tarjeta_id(id_tarjeta=id_tarjeta, id_usuario= id_usuario)
            if eliminar:
                mensaje_snack_bar_ok(page,"La tarjeta fue eliminada exitosamente")
                page.close(modal_eliminar)
                actualiza_listado_tarjetas()
            else:
                print(f"Error al eliminar la tarjeta {id_tarjeta}")
                mensaje_snack_bar_error(page,"Ocurrio un error intente nuevamente")
        except Exception as err:
            print(f"Ocurrio un error al eliminar la tarjeta asociada. : {err}")
            
    #---- VER GASTOS ----

    def ver_gastos(id_tarjeta: int):
        print(f'El usuario quiere ver los gastos de su tarjeta')

    
    #---- LAYOUT DE TARJETAS ----
    def crea_card_tarjeta(datos_tarjeta : dict , accion_editar , accion_eliminar, ver_gastos):
        """
        Toma un diccionar con las tarjetas de usuario y crea una card para cada una de ellas, con acciones para que el usuario interaccione
        """
        LOGOS_TARJETAS = {
            "visa" : "assets/imagenes/logos_tarjetas/visa_blanco.png",
            "mastercard" : "assets/imagenes/logos_tarjetas/mastercard.png",
            "american express" : "assets/imagenes/logos_tarjetas/american_express.png",
        }
        nombre_tipo_tarjeta= datos_tarjeta.get("tipo","").lower()
        logo_ruta_imagen = LOGOS_TARJETAS.get(nombre_tipo_tarjeta, None)
        logo = ft.Image(src=logo_ruta_imagen, width=80,height=80) if logo_ruta_imagen else ft.Container(width=40)

        id_tarjeta = datos_tarjeta.get("id_tarjeta",0)

        # --- Controles de texto para la información ---
        alias_texto = ft.Text(
            datos_tarjeta.get("alias", "Tarjeta"),
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE # Texto blanco para contrastar con el fondo oscuro
        )
        banco_texto = ft.Text(
            datos_tarjeta.get("banco", "Banco no especificado"),
            size=16,
            color=ft.Colors.WHITE70 # Un blanco menos intenso para el subtítulo
        )
        numeros_texto = ft.Text(
            f"•••• •••• •••• {datos_tarjeta.get('ultimos_numeros', 'XXXX')}",
            size=24,
            font_family="monospace", # Fuente monoespaciada para los números
            weight=ft.FontWeight.W_500,
            color=ft.Colors.WHITE
        )
        vencimiento_texto = ft.Text(
            f"Vence: {datos_tarjeta.get('fecha_vencimiento', 'MM/AA')}",
            size=18,
            color=ft.Colors.WHITE70
        )
        
        img_chip = ft.Image(src="assets/imagenes/logos_tarjetas/chip.png", width=80, height=80)

        layout_tarjeta = ft.Card(
            elevation=4,
            content= ft.Container(
                padding= ft.padding.all(15),
                width=550,
                height=280,
                border_radius= ft.border_radius.all(15),
                gradient= ft.LinearGradient(
                    begin= ft.alignment.top_left,
                    end= ft.alignment.bottom_right,
                    colors=[ft.Colors.BLUE_GREY_800, ft.Colors.BLUE_GREY_900]
                ),
                content= ft.Stack(
                    [
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Column([alias_texto,banco_texto],spacing=1),
                                        logo
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                ),
                                ft.Container(expand=True),
                                img_chip,
                                ft.Container(expand=True),
                                ft.Row([
                                    numeros_texto,
                                    vencimiento_texto
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    vertical_alignment= ft.CrossAxisAlignment.END
                                )
                            ]
                        )
                    ]
                )
            )
        )

        informacion_tarjeta = ft.Row(
            [
                ft.Column([
                    ft.Text("DIA DE CIERRE", size= 16, color= ft.Colors.ON_SURFACE_VARIANT, weight= ft.FontWeight.W_500),
                    ft.Text(str(datos_tarjeta.get("dia_cierre_resumen","--")), size= 20, weight= ft.FontWeight.W_500)
                ], alignment= ft.CrossAxisAlignment.CENTER, expand=True),
                ft.Column([
                    ft.Text("DIA DE VENCIMIENTO", size= 16, color= ft.Colors.ON_SURFACE_VARIANT, weight= ft.FontWeight.W_500),
                    ft.Text(str(datos_tarjeta.get("dia_vence_resumen","--")), size=20, weight= ft.FontWeight.W_500)
                ], alignment= ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("LIMITE", size= 16 , color= ft.Colors.ON_SURFACE_VARIANT, weight= ft.FontWeight.W_500),
                    ft.Text(f"$ {datos_tarjeta.get("limite", 0):,.0f}", size= 20, weight= ft.FontWeight.W_500)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True),
            ],
            alignment= ft.MainAxisAlignment.CENTER,
            spacing=20,
            height=60
        )

        acciones= ft.Row([
            ft.TextButton("Ver Gastos", on_click= lambda e , id= id_tarjeta: ver_gastos(id), height= 50, width= 100),
            ft.IconButton(icon=ft.Icons.EDIT_ROUNDED, on_click= lambda e , t = datos_tarjeta :accion_editar(e,t), tooltip="Editar tarjeta", icon_size= 30),
            ft.IconButton(icon=ft.Icons.DELETE_ROUNDED, on_click= lambda e , id= id_tarjeta: accion_eliminar(e,id), tooltip= "Eliminar tarjeta", icon_color= ft.Colors.ERROR, icon_size= 30)
        ], alignment= ft.MainAxisAlignment.END)

        tarjeta_completa = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        layout_tarjeta,
                        informacion_tarjeta,
                        acciones
                    ],
                    spacing=5
                ),
                padding= ft.padding.only(top=10,left=10,right=10,bottom=5),
                width=580,
                height=430
            )
        )

        return tarjeta_completa


    #---- FUNCION QUE ALIMIENTA LA VISTA DE TARJETAS ----
    def cargar_tarjetas_en_listado():
        listado_tarjetas.controls.clear()
        id_usuario = page.client_storage.get("login_id")

        if not id_usuario:
            listado_tarjetas.controls.append(ft.Text("No se logro identificar al usuario"))
            if listado_tarjetas.page: listado_tarjetas.update()
            return
        
        tarjetas_usuario = db.obtiene_tarjetas_por_usuario(id_usuario)

        if not tarjetas_usuario:
            listado_tarjetas.controls.append(ft.Text("Aun no tienes tarjetas registradas"))
        else:
            for tarjeta in tarjetas_usuario:
                card_tarjeta = crea_card_tarjeta(
                    tarjeta,
                    abre_modal_editar,
                    abre_modal_eliminar,
                    ver_gastos
                )
                listado_tarjetas.controls.append(card_tarjeta)

        if listado_tarjetas.page:
            listado_tarjetas.update()

    #---- LLAMAMOS A LA FUNCION PARA INICIALIZAR LA VISTA ----
    cargar_tarjetas_en_listado()

    #---- RETORNA LA VISTA ----
    return ft.Stack(
        [ft.ListView(
            [
                ft.Text("Mis tarjetas", size= 22 , weight= ft.FontWeight.BOLD, text_align= ft.TextAlign.START),
                ft.Divider(height=5, thickness= 0.5),
                listado_tarjetas
            ],
            spacing=10,
        ),
        ft.Container(
                content=boton_nueva_tarjeta,
                right= 25,
                bottom=25,
            )
        ]   
    )


