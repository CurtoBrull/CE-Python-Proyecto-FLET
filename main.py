import flet as ft

def main(page: ft.Page) -> None:
    # Config de la ventana
    page.title = "Gestor de Gastos"
    page.window_width = 900
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT # Se puede cambiar a DARK para modo oscuro
    
    # Contador simple para eventos de prueba
    contador = ft.Text("Clicks: 0", size=20)
    clicks = 0
    
    def on_click(e):
        nonlocal clicks # Permite modificar la variable clicks dentro de la función
        clicks += 1
        contador.value = f"Clicks: {clicks}"
        page.update()
        
    # Layout inicial
    page.add(
        ft.Column(
            controls=[
                ft.Text("Gestor de Gastos Personales", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Bienvenido. La app está en construcción.", size=16),
                ft.ElevatedButton("Pulsa aquí para probar", on_click=on_click), # EvelatedButton es un botón con sombra, se puede usar TextButton o OutlinedButton para otros estilos
                contador,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER, # Centra los controles horizontalmente
            spacing=20, # Espacio entre controles
        )
    )
    
ft.app(target=main) # Inicia la aplicación, llamando a la función main para configurar la ventana y mostrar los controles.
    