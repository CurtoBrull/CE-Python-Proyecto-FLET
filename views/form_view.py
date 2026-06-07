import flet as ft
from database import insert
from models import Transaccion, TipoTransaccion, Categoria


def crear_form(pag: ft.Page, on_guardado) -> ft.Column:
    """Devuelve el formulario de nueva transacción como un Column."""

    tipo_ref = ft.Ref[ft.Dropdown]()
    importe_ref = ft.Ref[ft.TextField]()
    categoria_ref = ft.Ref[ft.Dropdown]()
    descripcion_ref = ft.Ref[ft.TextField]()

    estado = ft.Text("", size=13, color=ft.Colors.GREEN_600)

    def guardar(e):
        if not importe_ref.current.value:
            estado.value = "El importe es obligatorio"
            estado.color = ft.Colors.RED_600
            pag.update()
            return

        try:
            importe = float(importe_ref.current.value.replace(",", "."))
        except ValueError:
            estado.value = "El importe debe ser un número"
            estado.color = ft.Colors.RED_600
            pag.update()
            return

        tran = Transaccion(
            tipo=TipoTransaccion(tipo_ref.current.value),
            importe=importe,
            categoria=Categoria(categoria_ref.current.value),
            descripcion=descripcion_ref.current.value or "",
        )

        insert(tran)

        importe_ref.current.value = ""
        descripcion_ref.current.value = ""
        estado.value = "Transacción guardada"
        estado.color = ft.Colors.GREEN_600
        on_guardado(e)
        pag.update()

    return ft.Column(
        controls=[
            ft.Text("Nueva Transacción", size=22, weight=ft.FontWeight.BOLD),
            # Dropdown es un control de selección, TextField es un campo de texto, ElevatedButton es un botón con sombra
            ft.Dropdown(
                ref=tipo_ref,
                label="Tipo",
                value=TipoTransaccion.GASTO.value,  # Valor por defecto
                options=[
                    ft.dropdown.Option(
                        key=TipoTransaccion.INGRESO.value, text="Ingreso"
                    ),
                    ft.dropdown.Option(key=TipoTransaccion.GASTO.value, text="Gasto"),
                ],
                width=300,
            ),
            ft.TextField(
                ref=importe_ref,
                label="Importe (€)",
                keyboard_type=ft.KeyboardType.NUMBER,
                width=300,
            ),
            ft.Dropdown(
                ref=categoria_ref,
                label="Categoría",
                value=Categoria.ALIMENTACION.value,
                options=[ft.dropdown.Option(c.value) for c in Categoria],
                width=300,
            ),
            ft.TextField(
                ref=descripcion_ref,
                label="Descripción (opcional)",
                width=300,
            ),
            # ElevatedButton es un botón con sombra, se puede usar TextButton o OutlinedButton para otros estilos
            ft.Button(
                "Guardar", on_click=guardar, width=300
            ),
            estado,
        ],
        spacing=16,
    )
