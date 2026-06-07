import flet as ft
from database import insert, update_transaccion
from models import Transaccion, TipoTransaccion, Categoria


def crear_form(pag: ft.Page, on_guardado) -> tuple[ft.Card, callable]:
    """Devuelve el formulario y una función para cargar una transacción a editar."""

    tipo_ref = ft.Ref[ft.Dropdown]()
    importe_ref = ft.Ref[ft.TextField]()
    categoria_ref = ft.Ref[ft.Dropdown]()
    descripcion_ref = ft.Ref[ft.TextField]()
    btn_ref = ft.Ref[ft.Button]()
    btn_cancelar_ref = ft.Ref[ft.Button]()
    titulo_ref = ft.Ref[ft.Text]()

    estado = ft.Text("", size=13, color=ft.Colors.GREEN_600)
    tran_editando = [None]  # lista mutable para modificar desde closures anidadas

    def _resetear_form():
        tran_editando[0] = None
        btn_ref.current.text = "Guardar"
        btn_cancelar_ref.current.visible = False
        titulo_ref.current.value = "Nueva Transacción"
        estado.value = ""
        importe_ref.current.value = ""
        descripcion_ref.current.value = ""
        tipo_ref.current.value = TipoTransaccion.GASTO.value
        categoria_ref.current.value = Categoria.ALIMENTACION.value

    def cancelar(e):
        _resetear_form()
        pag.update()

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

        if tran_editando[0] is None:
            insert(tran)
            importe_ref.current.value = ""
            descripcion_ref.current.value = ""
            estado.value = "Transacción guardada"
            estado.color = ft.Colors.GREEN_600
        else:
            tran.id = tran_editando[0].id
            tran.fecha = tran_editando[0].fecha
            update_transaccion(tran)
            _resetear_form()
            estado.value = "Transacción actualizada"
            estado.color = ft.Colors.GREEN_600

        on_guardado(e)
        pag.update()

    def cargar_transaccion(t: Transaccion) -> None:
        """Pre-rellena el formulario con los datos de t para editarla."""
        tran_editando[0] = t
        tipo_ref.current.value = t.tipo.value
        importe_ref.current.value = str(t.importe)
        categoria_ref.current.value = t.categoria.value
        descripcion_ref.current.value = t.descripcion
        btn_ref.current.text = "Actualizar"
        btn_cancelar_ref.current.visible = True
        titulo_ref.current.value = "Editar Transacción"
        label = t.descripcion.strip() if t.descripcion and t.descripcion.strip() else t.categoria.value
        estado.value = f"Editando: {label}"
        estado.color = ft.Colors.BLUE_600
        pag.update()

    contenedor = ft.Container(
        padding=24,
        content=ft.Column(
                controls=[
                    ft.Text(
                        "Nueva Transacción",
                        ref=titulo_ref,
                        theme_style=ft.TextThemeStyle.HEADLINE_SMALL,
                    ),
                    ft.Dropdown(
                        ref=tipo_ref,
                        label="Tipo",
                        value=TipoTransaccion.GASTO.value,
                        options=[
                            ft.dropdown.Option(key=TipoTransaccion.INGRESO.value, text="Ingreso"),
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
                    ft.Button("Guardar", ref=btn_ref, on_click=guardar, width=300),
                    ft.Button(
                        "Cancelar",
                        ref=btn_cancelar_ref,
                        on_click=cancelar,
                        width=300,
                        visible=False,
                        style=ft.ButtonStyle(color=ft.Colors.RED_400),
                    ),
                    estado,
                ],
                spacing=16,
            ),
        )

    card = ft.Card(content=contenedor, elevation=2)
    return card, cargar_transaccion
