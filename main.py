import os
import flet as ft

from database import init_db
from views.form_view import crear_form
from views.list_view import crear_lista
from views.chart_view import crear_grafico
from views.splash_view import crear_splash


def main(pag: ft.Page) -> None:
    pag.title = "Gestor de Gastos"
    pag.window.width = 1500
    pag.window.height = 950
    pag.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    pag.dark_theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)
    pag.theme_mode = ft.ThemeMode.LIGHT
    pag.bgcolor = ft.Colors.GREY_100

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

    panel_form = ft.Container(
        content=formulario,
        width=370,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
    )

    vista_transacciones = ft.Row(
        controls=[
            panel_form,
            ft.Container(content=lista, expand=True, padding=20),
        ],
        expand=True,
    )

    vista_grafico = ft.Container(
        content=grafico,
        expand=True,
        padding=20,
    )

    contenido_pendiente = [None]

    area = ft.Container(
        content=vista_transacciones,
        expand=True,
        opacity=1,
        animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),
    )

    def on_fade_out(e):
        if contenido_pendiente[0] is not None:
            area.content = contenido_pendiente[0]
            contenido_pendiente[0] = None
            area.opacity = 1
            pag.update()

    area.on_animation_end = on_fade_out

    def navegar(e):
        idx = e.control.selected_index
        if idx == 1:
            recargar_grafico()
        contenido_pendiente[0] = vista_transacciones if idx == 0 else vista_grafico
        area.opacity = 0
        pag.update()

    def _aplicar_colores():
        oscuro = pag.theme_mode == ft.ThemeMode.DARK
        pag.bgcolor = ft.Colors.GREY_900 if oscuro else ft.Colors.GREY_100
        panel_form.bgcolor = ft.Colors.GREY_800 if oscuro else ft.Colors.WHITE
        rail.bgcolor = "#212121" if oscuro else ft.Colors.GREY_200

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
        _aplicar_colores()
        pag.update()

    btn_tema = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        on_click=alternar_tema,
        tooltip="Alternar modo oscuro",
    )

    pag.appbar = ft.AppBar(
        title=ft.Text(
            "Gestor de Gastos Personales",
            theme_style=ft.TextThemeStyle.TITLE_LARGE,
            color=ft.Colors.WHITE,
        ),
        center_title=False,
        bgcolor=ft.Colors.TEAL_700,
        actions=[btn_tema],
    )

    _salir_cb = [None]

    rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        bgcolor=ft.Colors.GREY_200,
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
        trailing=ft.IconButton(
            icon=ft.Icons.LOGOUT,
            tooltip="Volver a inicio",
            on_click=lambda e: _salir_cb[0](e) if _salir_cb[0] else None,
        ),
    )

    layout_principal = ft.Row(
        controls=[
            rail,
            ft.VerticalDivider(width=1),
            area,
        ],
        expand=True,
    )

    # Envoltura para transición splash → app
    envoltura = ft.Container(
        expand=True,
        opacity=1,
        animate_opacity=ft.Animation(350, ft.AnimationCurve.EASE_IN_OUT),
    )
    pendiente_entrada = [None]

    def on_fade_entrada(e):
        if pendiente_entrada[0] is not None:
            envoltura.content = pendiente_entrada[0]
            pendiente_entrada[0] = None
            envoltura.opacity = 1
            pag.appbar.visible = True
            pag.update()

    envoltura.on_animation_end = on_fade_entrada

    def al_entrar(e):
        pendiente_entrada[0] = layout_principal
        envoltura.opacity = 0
        pag.update()

    splash_content = crear_splash(pag, al_entrar)

    def al_salir(e):
        pag.appbar.visible = False
        rail.selected_index = 0
        area.content = vista_transacciones
        pendiente_entrada[0] = splash_content
        envoltura.opacity = 0
        pag.update()

    _salir_cb[0] = al_salir

    envoltura.content = splash_content
    pag.appbar.visible = False

    pag.add(envoltura)
    pag.update()


ft.run(main, port=int(os.getenv("PORT", 8000)), assets_dir="assets")
