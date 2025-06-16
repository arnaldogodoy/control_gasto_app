import flet as ft
from db import db
from db import db
from rutas.Rutas import agregar_tarjeta

def tarjetas(page : ft.Page):

    listado_tarjetas = ft.Row(
        wrap=True,
        alignment= ft.MainAxisAlignment.CENTER,
        vertical_alignment= ft.CrossAxisAlignment.CENTER,
        spacing= 20,
        run_spacing=5,
        width=1200
    )

    def ir_agregar_tarjeta(e):
        page.go(route=agregar_tarjeta)
    
    boton_nueva_tarjeta = ft.FloatingActionButton(
        icon=ft.Icons.ADD_CARD_ROUNDED,
        text="Añadir Tarjeta",
        on_click=ir_agregar_tarjeta,
    )
        
    def editar_tarjeta(id_tarjeta : int):
        print(f"El usuario quiere editar la tarjeta ID : {id_tarjeta}")
    
    def eliminar_tarjeta(id_tarjeta : int):
        print(f"El usuario quiere eliminar la tarjeta ID: {id_tarjeta}")
    
    def ver_gastos(id_tarjeta: int):
        print(f'El usuario quiere ver los gastos de su tarjeta')

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
                height=300,
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
            ft.IconButton(icon=ft.Icons.EDIT_ROUNDED, on_click= lambda e , id= id_tarjeta: accion_editar(id), tooltip="Editar tarjeta", icon_size= 30),
            ft.IconButton(icon=ft.Icons.DELETE_ROUNDED, on_click= lambda e , id= id_tarjeta: accion_eliminar(id), tooltip= "Eliminar tarjeta", icon_color= ft.Colors.ERROR, icon_size= 30)
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
                height=440
            )
        )

        return tarjeta_completa


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
                    editar_tarjeta,
                    eliminar_tarjeta,
                    ver_gastos
                )
                listado_tarjetas.controls.append(card_tarjeta)

        if listado_tarjetas.page:
            listado_tarjetas.update()

    cargar_tarjetas_en_listado()

    return ft.Stack(
        [ft.Column(
            [
                ft.Text("Mis tarjetas", size= 22 , weight= ft.FontWeight.BOLD, text_align= ft.TextAlign.START),
                ft.Divider(height=5, thickness= 0.5),
                listado_tarjetas
            ],
            expand=True,
            spacing=5,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        ft.Container(
                content=boton_nueva_tarjeta,
                right= 25,
                bottom=25,
            )
        ]
    )


