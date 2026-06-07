import flet as ft
from database import insert
from models import Transaccion, TipoTransaccion, Categoria


def create_form(page: ft.Page, on_save) -> ft.Column:
    """Devuelve el formulario de nueva transacción como un Column."""

    tipo_ref = ft.Ref[ft.Dropdown]()
    importe_ref = ft.Ref[ft.TextField]()
    categoria_ref = ft.Ref[ft.Dropdown]()
    descripcion_ref = ft.Ref[ft.TextField]()

    def save(e):
        # Validaciones básicas
        if not importe_ref.current.value:
            # SnackBar es un mensaje temporal que aparece en la parte inferior de la pantalla
            page.snack_bar = ft.SnackBar(ft.Text("El importe es obligatorio"))
            page.snack_bar.open = True
            page.update()
            return

        try:
            importe = float(importe_ref.current.value.replace(",", "."))
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("El importe debe ser un número"))
            page.snack_bar.open = True
            page.update()
            return

        tran = Transaccion(
            tipo=TipoTransaccion(tipo_ref.current.value),
            importe=importe,
            categoria=Categoria(categoria_ref.current.value),
            descripcion=descripcion_ref.current.value or "",
        )

        insert(tran)  # Guarda en la base de datos

        # Limpia el formulario
        importe_ref.current.value = ""
        descripcion_ref.current.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Transacción guardada"))
        page.snack_bar.open = True
        on_save(
            e
        )  # avisa al exterior antes de update para que sus cambios entren en el mismo refresco
        page.update()

    return ft.Column(
        controls=[
            ft.Text("Nueva Transacción", size=22, weight=ft.FontWeight.BOLD),
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
            ft.ElevatedButton(
                "Guardar", on_click=save, width=300
            ),  # ElevatedButton es un botón con sombra, se puede usar TextButton o OutlinedButton para otros estilos
        ],
        spacing=16,
    )
