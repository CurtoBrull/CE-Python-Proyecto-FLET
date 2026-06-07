import flet as ft

from database import init_db
from views.form_view import crear_form
from views.list_view import crear_lista


def main(pag: ft.Page) -> None:
    # Config de la ventana
    pag.title = "Gestor de Gastos"
    pag.window_width = 900
    pag.window_height = 650
    pag.theme_mode = ft.ThemeMode.LIGHT  # Se puede cambiar a DARK para modo oscuro

    init_db()

    def refrescar(e=None):
        recargar()
        pag.update()

    formulario = crear_form(pag, refrescar)
    lista, recargar = crear_lista(pag, refrescar)

    pag.add(
        ft.Row(
            controls=[
                ft.Container(content=formulario, width=350, padding=20),
                ft.VerticalDivider(),
                ft.Container(content=lista, expand=True, padding=20),
            ],
            expand=True,
        )
    )


# Inicia la aplicación, llamando a la función main para configurar la ventana y mostrar los controles.
ft.run(main)
