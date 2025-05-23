import flet as ft


def boton_avanzar(text : str, click : callable, visible = True):
    btn = ft.ElevatedButton(text,
                            width= 200, 
                            height= 50,
                            bgcolor= "#fea612",
                            color= "black",
                            visible= visible,
                            on_click=click,
                            style= ft.ButtonStyle(
                                text_style=ft.TextStyle(size=18,
                                                        weight=ft.FontWeight.BOLD) , 
                                                        ),              
                                      )
    return btn

def boton_cancelar_go(text : str, vista : str, page: ft.Page ,visible = True):
    btn = ft.ElevatedButton(text,
                            width= 200,
                            height= 50,
                            bgcolor= "grey",
                            color = "black",
                            visible= visible,
                            on_click= lambda e: page.go(vista),
                            style= ft.ButtonStyle(
                                text_style= ft.TextStyle(size= 18,
                                                         weight= ft.FontWeight.BOLD)
                            )                       
                            )
    return btn