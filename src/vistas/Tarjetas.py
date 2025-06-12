import flet as ft
from db import db
from ui_elements.UiElements import crea_snack_bar, mensaje_snack_bar_ok, mensaje_snack_bar_error, crear_tarjeta_formulario
from ui_elements.botones import boton_primario, boton_cancelar_navegacion
from db import db
from rutas.Rutas import agregar_tarjeta

def tarjetas(page : ft.Page):

    listado_tarjetas = ft.ListView(expand=True,auto_scroll=True,spacing=10, padding= ft.padding.only(top=10))

    def ir_agregar_tarjeta(e):
        page.go(route=agregar_tarjeta)

    boton_nueva_tarjeta = ft.FloatingActionButton(
        icon= ft.Icons.ADD_CARD_ROUNDED,
        text= "Añadir Tarjeta",
        on_click= ir_agregar_tarjeta,
    )

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
                card_tarjeta = ft.Card(
                    content= ft.Container(
                        content= ft.Column(
                            [
                            ft.ListTile(
                                leading= ft.Icon(ft.Icons.CREDIT_CARD_ROUNDED, color= ft.Colors.PRIMARY if hasattr(ft.Colors, "PRIMARY") else ft.Colors.BLUE), 
                                title= ft.Text(f"{tarjeta.get('alias','tarjeta')}", weight=ft.FontWeight.BOLD),
                                subtitle= ft.Text(
                                    f"{tarjeta.get('banco', 'N/A')} - {tarjeta.get('tipo', 'N/A')}\n"
                                    f"Termina {tarjeta.get('ultimos_numeros', 'XXXX')} Vence: {tarjeta.get('fecha_vencimiento_tarjeta', 'MM/AA')}"
                            ),
                            on_click= lambda e , tid = tarjeta.get('id_tarjeta'): print(f"Click en tarjeta ID :{tid}")
                                )
                            ]
                        ),
                        width= 500,
                        padding=10
                    ),
                    shadow_color= ft.Colors.ON_SURFACE_VARIANT,
                )
                listado_tarjetas.controls.append(card_tarjeta)

        if listado_tarjetas.page:
            listado_tarjetas.update()

    cargar_tarjetas_en_listado()

    return ft.Stack(
        [
            ft.Column(
                [
                    ft.Text("Mis tarjetas", size= 22 , weight= ft.FontWeight.BOLD, text_align= ft.TextAlign.START),
                    ft.Divider(height=5, thickness= 0.5),
                    ft.Container(
                        content=listado_tarjetas,
                        expand=True
                    ),
                ],
                expand=True,
                spacing=10,
            ),
            ft.Container(
                content= boton_nueva_tarjeta,
                right=20,
                bottom=20
            )
        ]
    )



