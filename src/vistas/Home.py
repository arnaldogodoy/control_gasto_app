import flet as ft
from ui_elements.UiElements import crea_snack_bar
from vistas.Tarjetas import tarjetas

def vista_dashboard(page : ft.Page):
    return ft.Column([ft.Text("Dashboard", size=20)])
    
def vista_gastos(page : ft.Page):
        return ft.Column([ft.Text("Gastos" , size=20)])
    
def vista_categorias(page : ft.Page):
        return ft.Column([ft.Text("Categorias", size=20)])
    
mapa_contenidos ={
    0 : vista_dashboard,  
    1 : tarjetas,
    2 : vista_gastos,
    3 : vista_categorias,
}


def home(page : ft.Page):
      snack = crea_snack_bar()
      page.snack_bar = snack
      if snack not in page.overlay:
            page.overlay.append(snack)
    
      indice_inicial =  page.client_storage.get("home_vista.selectec_index") or 0
      try:
          indice_inicial = int(indice_inicial)
      except (ValueError,TypeError):
            indice_inicial = 0 

      area_contenido_principal = ft.Container(
      content=mapa_contenidos[indice_inicial](page),
      expand=True,
      padding=ft.padding.all(20)
      )     

      def cambiar_seccion(e : ft.ControlEvent):
            indice_seleccionado = e.control.selected_index
            area_contenido_principal.content = mapa_contenidos[indice_seleccionado](page)
            page.client_storage.set("home_vista.selectec_index", indice_seleccionado)
            area_contenido_principal.update()

      rail = ft.NavigationRail(
            selected_index= indice_inicial,
            label_type= ft.NavigationRailLabelType.ALL,
            min_width= 100,
            min_extended_width= 250,
            on_change= cambiar_seccion,
            elevation= 6,
            indicator_color= ft.Colors.ORANGE_200,
            destinations=[
                  ft.NavigationRailDestination(
                        icon=ft.Icons.DASHBOARD_OUTLINED,
                        selected_icon= ft.Icons.DASHBOARD_ROUNDED,
                        label="Dashboard"
                  ),
                  ft.NavigationRailDestination(
                        icon=ft.Icons.CREDIT_CARD_OUTLINED,
                        selected_icon= ft.Icons.CREDIT_CARD,
                        label="Tarjetas"
                  ),
                  ft.NavigationRailDestination(
                        icon=ft.Icons.PAYMENTS_OUTLINED,
                        selected_icon= ft.Icons.PAYMENTS_ROUNDED,
                        label="Gastos"
                  ),
                  ft.NavigationRailDestination(
                        icon=ft.Icons.CATEGORY_OUTLINED,
                        selected_icon=ft.Icons.CATEGORY_ROUNDED,
                        label="Categorias"
                  )
            ],
      )

      layout_home = ft.Row(
            [
                  rail,
                  area_contenido_principal,
            ],
            expand=True,
            vertical_alignment= ft.CrossAxisAlignment.CENTER,
            
      )
      
      return layout_home
