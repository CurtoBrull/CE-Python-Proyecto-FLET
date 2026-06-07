import flet as ft

from database import init_db
from views.form_view import create_form


def main(page: ft.Page) -> None:
    # Config de la ventana
    page.title = "Gestor de Gastos"
    page.window_width = 900
    page.window_height = 650
    page.theme_mode = ft.ThemeMode.LIGHT  # Se puede cambiar a DARK para modo oscuro

    init_db()  # Inicializa la base de datos (crea tablas si no existen)

    def on_save(e):
        # Aquí se actualizaría la lista de transacciones después de guardar una nueva, por ejemplo recargando los datos desde la base de datos
        pass

    page.add(
        create_form(page, on_save)
    )  # Agrega el formulario a la página, pasando la función on_save para que se llame después de guardar una transacción.


ft.app(
    target=main
)  # Inicia la aplicación, llamando a la función main para configurar la ventana y mostrar los controles.
