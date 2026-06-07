import flet as ft

from database import init_db
from views.form_view import crear_form
from views.list_view import crear_lista
from views.chart_view import crear_grafico


def main(pag: ft.Page) -> None:
    pag.title = "Gestor de Gastos"
    pag.window.width = 1300
    pag.window.height = 850
    pag.theme_mode = ft.ThemeMode.LIGHT

    init_db()

    def refrescar(e=None):
        recargar()
        recargar_grafico()
        pag.update()

    formulario = crear_form(pag, refrescar)
    lista, recargar = crear_lista(pag, refrescar)
    grafico, recargar_grafico = crear_grafico(pag)

    vista_transacciones = ft.Row(
        controls=[
            ft.Container(content=formulario, width=350, padding=20),
            ft.VerticalDivider(),
            ft.Container(content=lista, expand=True, padding=20),
        ],
        expand=True,
    )

    vista_grafico = ft.Container(
        content=grafico,
        expand=True,
        padding=20,
    )

    # Un único contenedor que intercambia la vista activa
    area = ft.Container(content=vista_transacciones, expand=True)

    def navegar(e):
        idx = e.control.selected_index
        if idx == 0:
            area.content = vista_transacciones
        else:
            recargar_grafico()
            area.content = vista_grafico
        pag.update()

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                selected_icon=ft.Icons.LIST_ALT,
                label="Transacciones",
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.BAR_CHART_OUTLINED,
                selected_icon=ft.Icons.BAR_CHART,
                label="Gráfico",
            ),
        ],
        on_change=navegar,
    )

    pag.add(
        ft.Row(
            controls=[
                rail,
                ft.VerticalDivider(width=1),
                area,
            ],
            expand=True,
        )
    )
    pag.update()  # aplica dimensiones de ventana


ft.run(main)
