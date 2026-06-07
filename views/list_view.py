import flet as ft
from database import get_all, delete
from models import TipoTransaccion


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
    
    def cargar():
        trans = get_all()
        
        tabla.rows.clear()
        
        for t in trans:
            # El color de la fila depende del tipo de transacción: rojo para gastos, verde para ingresos
            color = ft.Colors.RED_400 if t.tipo == TipoTransaccion.GASTO else ft.Colors.GREEN_400
            
            def hacer_eliminar(tran_id):
                def eliminar(e):
                    delete(tran_id)
                    on_eliminado(tran_id)
                return eliminar
            
            tabla.rows.append(
                ft.DataRow(
                    cells=[
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
                    ]
                )
            )
            
        ingresos = sum(t.importe for t in trans if t.tipo == TipoTransaccion.INGRESO)
        gastos = sum(t.importe for t in trans if t.tipo == TipoTransaccion.GASTO)
        saldo = ingresos - gastos
        color_saldo = ft.Colors.GREEN_600 if saldo >= 0 else ft.Colors.RED_600
        
        resumen.value = f"Total Ingresos: {ingresos:.2f} €   |   Total Gastos: {gastos:.2f} €   |   Saldo: {saldo:.2f} €"
        resumen.color = color_saldo
        
    cargar()

    columna = ft.Column(
        controls=[
            ft.Text("Transacciones", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row([resumen]),
            ft.Column(
                controls=[tabla],
                scroll=ft.ScrollMode.AUTO,
            ),
        ],
        expand=True,
        spacing=12,
    )
    return columna, cargar
                    