import os
import flet as ft

from database import init_db
from views.form_view import crear_form
from views.list_view import crear_lista
from views.chart_view import crear_grafico


def main(pag: ft.Page) -> None:
    pag.title = "Gestor de Gastos"
    pag.window.width = 1500
    pag.window.height = 950
    pag.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    pag.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    pag.theme_mode = ft.ThemeMode.LIGHT

    init_db()

    def refrescar(e=None):
        recargar()
        recargar_grafico()
        pag.update()

    formulario, cargar_transaccion = crear_form(pag, refrescar)

    def on_editar(t):
        cargar_transaccion(t)

    lista, recargar = crear_lista(pag, refrescar, on_editar=on_editar)
    grafico, recargar_grafico = crear_grafico(pag)

    vista_transacciones = ft.Row(
        controls=[
            ft.Container(content=formulario, width=370, padding=20),
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

    area = ft.Container(content=vista_transacciones, expand=True)

    def navegar(e):
        idx = e.control.selected_index
        if idx == 0:
            area.content = vista_transacciones
        else:
            recargar_grafico()
            area.content = vista_grafico
        pag.update()

    def alternar_tema(e):
        pag.theme_mode = (
            ft.ThemeMode.DARK
            if pag.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        btn_tema.icon = (
            ft.Icons.DARK_MODE
            if pag.theme_mode == ft.ThemeMode.LIGHT
            else ft.Icons.LIGHT_MODE
        )
        pag.update()

    btn_tema = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        on_click=alternar_tema,
        tooltip="Alternar modo oscuro",
    )

    pag.appbar = ft.AppBar(
        title=ft.Text("Gestor de Gastos Personales", theme_style=ft.TextThemeStyle.TITLE_LARGE),
        center_title=False,
        actions=[btn_tema],
    )

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
    pag.update()


ft.run(main, port=int(os.getenv("PORT", 8000)))
