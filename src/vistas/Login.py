import flet as ft
from db import db
from rutas.Rutas import reiniciar_clave , registro, ruta_imagen

def inicio_sesion(page: ft.Page):
    page.title = "Inicio"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    img_path = ruta_imagen("login.png") 
    correo = ft.TextField(hint_text="Correo electronico" )
    clave = ft.TextField(hint_text="Contraseña",  password=True, can_reveal_password=True)
    snack = ft.SnackBar(
        content= ft.Text(""),
        bgcolor= "green",
        duration= 3000
    )
    page.overlay.append(snack)

    def login_click(e):
        if db.logea_usuario(correo.value, clave.value):
            snack.content = ft.Text("¡Login exitoso!")
            snack.bgcolor = "green"
            #page.go("/home")  # Redirige a la página de inicio
        else:
            snack.content = ft.Text("Usuario o contraseña incorrectos")
            snack.bgcolor = "red"
        snack.open = True
        page.update()

    return ft.Container(
            ft.Column(
            [
                ft.Image(src = img_path, width = 500, height = 300, fit = ft.ImageFit.CONTAIN),
                ft.Text("Bienvenido" ,size = 30, weight = ft.FontWeight.BOLD, color = "Black"),
                correo,
                clave,
                ft.ElevatedButton("Iniciar Sesion",
                                  width= 200, 
                                  height= 50,
                                  bgcolor= "#fea612",
                                  color= "black",
                                  style= ft.ButtonStyle(
                                      text_style=ft.TextStyle(size=18,
                                                              weight=ft.FontWeight.BOLD) , 
                                                              ),
                                                              on_click=login_click
                                      ),                                
                ft.TextButton("¿Olvidaste tu contraseña?", on_click = lambda e: page.go(reiniciar_clave)),
                ft.TextButton("¿No tienes cuenta? Registrate", on_click= lambda e: page.go(registro))  
            ], 
            alignment= ft.MainAxisAlignment.CENTER,
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ) ,
        width= 400,
        height= 700
    )
