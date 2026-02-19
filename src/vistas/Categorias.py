import flet as ft
from db import db

def categorias(page : ft.Page):

    def crea_card_por_categoria(categoria_del_usuario : dict):
        id_categoria = categoria_del_usuario.get("id_categoria")
        
        acciones_categoria = []
        if categoria_del_usuario["id_usuario"] is not None:
            acciones_categoria =[
                    ft.IconButton(icon=ft.Icons.EDIT_ROUNDED, on_click= lambda e, id = id_categoria : editar_categoria(e,id), icon_size=18, tooltip= "Editar categoría",padding=4),
                    ft.IconButton(icon=ft.Icons.DELETE_ROUNDED, on_click= lambda e, id = id_categoria: eliminar_categoria(e,id), icon_size=18, tooltip="Eliminar categoria" ,icon_color= ft.Colors.ERROR)
                ]

        layout_categoria = ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(categoria_del_usuario.get("icono", "circle"), size= 16),
                        ft.Text(categoria_del_usuario["categoria"]),
                        ft.Container(expand=True),
                        ft.Row(acciones_categoria,alignment=ft.MainAxisAlignment.END)
                    ],
                    #alignment= ft.MainAxisAlignment.CENTER,
                    spacing=8
                ),
                padding= ft.padding.symmetric(vertical=8, horizontal=12),
                border_radius= ft.border_radius.all(12),
                border= ft.border.all(1, color=ft.Colors.OUTLINE_VARIANT)
            ),
            width=700
        )
        return layout_categoria

    listado_de_categorias = ft.GridView(
    expand=True,
    runs_count=2,  
    #max_child_extent=400, 
    spacing=10,
    run_spacing=10,
    padding=20
)


    def carga_categorias_en_listado():
        listado_de_categorias.clean()
        id_usuario = page.client_storage.get("login_id")

        if not id_usuario:
            listado_de_categorias.controls = [ft.Text("No se logro identificar al usuario")]
            if listado_de_categorias.page : listado_de_categorias.update()
            return
        
        categorias_del_usuario = db.obtener_categorias_por_usuario(id_usuario)

        if not categorias_del_usuario:
            listado_de_categorias.controls = [ft.Text("El usuario no tiene categorias asociadas")]
            if listado_de_categorias.page : listado_de_categorias.update()
        else:
            agrupador_actual = ""
            fila_para_agrupador = None
            for categoria in categorias_del_usuario:
                if categoria["agrupador"] != agrupador_actual:
                    agrupador_actual = categoria["agrupador"]
                    #Se agrega el titulo del agrupador
                    listado_de_categorias.controls.append(
                        ft.Text(agrupador_actual, weight=ft.FontWeight.BOLD, size= 18, color= "primary")
                    )
                    #Row para las categorias de ese agrupador
                    fila_para_agrupador = ft.Row(wrap=True, spacing= 8 , run_spacing=8)
                    #Se agrega la fila al listado
                    listado_de_categorias.controls.append(fila_para_agrupador)
                card_categoria = crea_card_por_categoria(categoria)
                if card_categoria and fila_para_agrupador is not None:
                    fila_para_agrupador.controls.append(card_categoria)

        page.update()
    
    def agregar_categoria(e):
        return None

    boton_nueva_categoria = ft.FloatingActionButton(
        text= "Nueva categoria",
        icon= ft.Icons.ADD_ROUNDED,
        on_click= agregar_categoria
    )

    def editar_categoria(e, id_categoria):
        return None
    
    def eliminar_categoria(e, id_categoria):
        return None  

    #LLAMAMOS A LA FUNCION PARA ALIMENTAR LA VISTA CON LAS CATEGORIAS
    carga_categorias_en_listado()
    return ft.Stack(
        [
            listado_de_categorias,
            ft.Container(
                content=boton_nueva_categoria,
                right=25,
                bottom=25
            )   
        ],
    )