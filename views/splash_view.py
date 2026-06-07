import flet as ft


def crear_splash(pag: ft.Page, on_entrar) -> ft.Container:
    """Pantalla de presentación a pantalla completa."""

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=0,
            controls=[
                ft.Icon(
                    ft.Icons.ACCOUNT_BALANCE_WALLET,
                    size=90,
                    color=ft.Colors.TEAL_400,
                ),
                ft.Container(height=24),
                ft.Text(
                    "Gestor de Gastos",
                    size=42,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    "Personales",
                    size=42,
                    weight=ft.FontWeight.W_300,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.TEAL_400,
                ),
                ft.Container(height=16),
                ft.Text(
                    "Registra, analiza y controla tus finanzas personales.",
                    size=16,
                    text_align=ft.TextAlign.CENTER,
                    color=ft.Colors.GREY_500,
                ),
                ft.Container(height=8),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=24,
                    controls=[
                        _chip(ft.Icons.STORAGE, "PostgreSQL · Neon"),
                        _chip(ft.Icons.SMARTPHONE, "Flet · Flutter"),
                        _chip(ft.Icons.CLOUD, "Render"),
                    ],
                ),
                ft.Container(height=48),
                ft.Button(
                    "Entrar a la aplicación",
                    on_click=on_entrar,
                    width=260,
                    style=ft.ButtonStyle(
                        bgcolor=ft.Colors.TEAL_700,
                        color=ft.Colors.WHITE,
                        padding=16,
                    ),
                ),
                ft.Container(height=12),
                ft.Text(
                    "Proyecto final · CE Desarrollo de Aplicaciones en Python",
                    size=11,
                    color=ft.Colors.GREY_400,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
        ),
    )


def _chip(icono, texto: str) -> ft.Row:
    return ft.Row(
        spacing=6,
        tight=True,
        controls=[
            ft.Icon(icono, size=14, color=ft.Colors.GREY_500),
            ft.Text(texto, size=12, color=ft.Colors.GREY_500),
        ],
    )
