import flet as ft
from database import delete, get_filtered
from models import TipoTransaccion, Categoria
from utils.constants import MESES


def crear_lista(pag: ft.Page, on_eliminado) -> tuple[ft.Column, callable]:
    """Devuelve la lista de transacciones con resumen como un Column."""

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Categoría")),
            ft.DataColumn(ft.Text("Descripción")),
            ft.DataColumn(ft.Text("Importe €"), numeric=True),
            ft.DataColumn(ft.Text("")),
        ],
        rows=[],
    )

    resumen = ft.Text("", size=14)

    # Refs para leer los valores desde cargar() antes de que los controles existan
    mes_ref = ft.Ref[ft.Dropdown]()
    cat_ref = ft.Ref[ft.Dropdown]()

    def cargar():
        mes_val = mes_ref.current.value if mes_ref.current else "0"
        cat_val = cat_ref.current.value if cat_ref.current else "todas"
        mes = int(mes_val) if mes_val != "0" else None
        cat = cat_val if cat_val != "todas" else None
        trans = get_filtered(mes=mes, categoria=cat)

        tabla.rows.clear()
        for t in trans:
            color = ft.Colors.RED_400 if t.tipo == TipoTransaccion.GASTO else ft.Colors.GREEN_400

            def hacer_eliminar(tran_id):
                def eliminar(e):
                    delete(tran_id)
                    on_eliminado(e)
                return eliminar

            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(t.fecha))),
                    ft.DataCell(ft.Text(t.tipo.value, color=color)),
                    ft.DataCell(ft.Text(t.categoria.value)),
                    ft.DataCell(ft.Text(t.descripcion)),
                    ft.DataCell(ft.Text(f"{t.importe:.2f}", color=color)),
                    ft.DataCell(ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED_300,
                        on_click=hacer_eliminar(t.id),
                    )),
                ])
            )

        ingresos = sum(t.importe for t in trans if t.tipo == TipoTransaccion.INGRESO)
        gastos = sum(t.importe for t in trans if t.tipo == TipoTransaccion.GASTO)
        saldo = ingresos - gastos
        resumen.value = f"Ingresos: {ingresos:.2f} €   |   Gastos: {gastos:.2f} €   |   Saldo: {saldo:.2f} €"
        resumen.color = ft.Colors.GREEN_600 if saldo >= 0 else ft.Colors.RED_600

    def al_filtrar(e):
        cargar()
        pag.update()

    cargar()  # carga inicial — refs aún None, usa defaults (sin filtros)

    columna = ft.Column(
        controls=[
            ft.Text("Transacciones", size=22, weight=ft.FontWeight.BOLD),
            ft.Row([
                ft.Dropdown(
                    ref=mes_ref,
                    label="Filtrar por mes",
                    value="0",
                    options=[ft.dropdown.Option(key=str(k), text=v) for k, v in MESES.items()],
                    width=160,
                ),
                ft.Dropdown(
                    ref=cat_ref,
                    label="Filtrar por categoría",
                    value="todas",
                    options=[ft.dropdown.Option(key="todas", text="Todas")]
                    + [ft.dropdown.Option(key=c.value, text=c.value) for c in Categoria],
                    width=200,
                ),
                ft.ElevatedButton("Filtrar", on_click=al_filtrar),
            ], spacing=12),
            ft.Divider(),
            ft.Row([resumen]),
            ft.Column(controls=[tabla], scroll=ft.ScrollMode.AUTO),
        ],
        expand=True,
        spacing=12,
    )
    return columna, cargar
