import flet as ft
from database import get_gastos_por_categoria, get_ingresos_por_categoria
from utils.constants import COLORES, ALTURA_MAX_GRAFICO


def _construir_barras(datos: dict, max_val: float) -> ft.Row:
    """Construye una fila de barras proporcionales a max_val."""
    barras = []
    for i, (cat, val) in enumerate(datos.items()):
        altura = max(int((val / max_val) * ALTURA_MAX_GRAFICO), 4)
        color = COLORES[i % len(COLORES)]
        barras.append(
            ft.Column(
                controls=[
                    ft.Text(f"{val:.0f} €", size=11, text_align=ft.TextAlign.CENTER),
                    ft.Container(
                        width=55,
                        height=altura,
                        bgcolor=color,
                        border_radius=4,
                        tooltip=f"{cat}: {val:.2f} €",
                    ),
                    ft.Text(cat, size=11, text_align=ft.TextAlign.CENTER, width=70),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=4,
            )
        )
    return ft.Row(
        controls=barras,
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.END,
        spacing=16,
        wrap=True,
    )


def crear_grafico(pag: ft.Page) -> tuple[ft.Column, callable]:
    """Devuelve el gráfico de gastos e ingresos por categoría."""

    gastos_container = ft.Container(expand=True)
    ingresos_container = ft.Container(expand=True)

    def cargar():
        gastos = get_gastos_por_categoria()
        ingresos = get_ingresos_por_categoria()

        # --- Gastos ---
        if gastos:
            gastos_container.content = _construir_barras(gastos, max(gastos.values()))
        else:
            gastos_container.content = ft.Text("Sin datos de gastos.", size=14)

        # --- Ingresos ---
        if ingresos:
            ingresos_container.content = _construir_barras(ingresos, max(ingresos.values()))
        else:
            ingresos_container.content = ft.Text("Sin datos de ingresos.", size=14)

    cargar()

    columna = ft.Column(
        controls=[
            ft.Text("Gastos por categoría", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
            ft.Card(
                content=ft.Container(content=gastos_container, padding=20),
                elevation=2,
            ),
            ft.Text("Ingresos por categoría", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
            ft.Card(
                content=ft.Container(content=ingresos_container, padding=20),
                elevation=2,
            ),
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=True,
        spacing=16,
    )
    return columna, cargar
