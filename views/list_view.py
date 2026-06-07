import base64
import csv
import io
from datetime import date
from pathlib import Path
import flet as ft
from database import delete, get_filtered
from models import TipoTransaccion, Categoria
from utils.constants import MESES


def crear_lista(pag: ft.Page, on_eliminado, on_editar=None) -> tuple[ft.Column, callable]:
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
        column_spacing=20,
    )

    resumen = ft.Text("", size=14)
    trans_actual = []  # transacciones del último cargar(), usadas para exportar

    mes_ref = ft.Ref[ft.Dropdown]()
    cat_ref = ft.Ref[ft.Dropdown]()

    def cargar():
        mes_val = mes_ref.current.value if mes_ref.current else "0"
        cat_val = cat_ref.current.value if cat_ref.current else "todas"
        mes = int(mes_val) if mes_val != "0" else None
        cat = cat_val if cat_val != "todas" else None
        trans = get_filtered(mes=mes, categoria=cat)

        trans_actual.clear()
        trans_actual.extend(trans)

        tabla.rows.clear()
        for t in trans:
            color = ft.Colors.RED_400 if t.tipo == TipoTransaccion.GASTO else ft.Colors.GREEN_400

            def hacer_eliminar(tran_id):
                def eliminar(e):
                    delete(tran_id)
                    on_eliminado(e)
                return eliminar

            def hacer_editar(tran):
                def editar(e):
                    if on_editar:
                        on_editar(tran)
                return editar

            tabla.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(str(t.fecha))),
                    ft.DataCell(ft.Text(t.tipo.value, color=color)),
                    ft.DataCell(ft.Text(t.categoria.value)),
                    ft.DataCell(ft.Text(t.descripcion)),
                    ft.DataCell(ft.Text(f"{t.importe:.2f}", color=color)),
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=ft.Colors.BLUE_300,
                                on_click=hacer_editar(t),
                                tooltip="Editar",
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE,
                                icon_color=ft.Colors.RED_300,
                                on_click=hacer_eliminar(t.id),
                                tooltip="Eliminar",
                            ),
                        ], spacing=0)
                    ),
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

    # --- Exportar CSV ---
    msg_export = ft.Text("", size=12, color=ft.Colors.GREEN_600)

    def _generar_csv() -> str:
        """Genera el contenido CSV como string."""
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["ID", "Fecha", "Tipo", "Categoría", "Descripción", "Importe"])
        for t in trans_actual:
            writer.writerow([t.id, t.fecha, t.tipo.value, t.categoria.value, t.descripcion, t.importe])
        return buf.getvalue()

    def al_exportar(e):
        nombre = f"transacciones_{date.today()}.csv"
        en_escritorio = False

        try:
            import tkinter as tk
            from tkinter import filedialog
            root = tk.Tk()
            root.withdraw()
            root.wm_attributes("-topmost", True)
            ruta = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                initialfile=nombre,
                title="Guardar transacciones como CSV",
            )
            root.destroy()
            if ruta:
                with open(ruta, "w", newline="", encoding="utf-8") as f:
                    f.write(_generar_csv())
                msg_export.value = f"Guardado: {Path(ruta).name}"
                en_escritorio = True
        except Exception:
            pass

        if not en_escritorio:
            # Web: descarga via data URI en el navegador
            b64 = base64.b64encode(_generar_csv().encode("utf-8")).decode()
            pag.launch_url(f"data:text/csv;base64,{b64}")
            msg_export.value = f"Descargando {nombre}..."

        pag.update()

    cargar()

    columna = ft.Column(
        controls=[
            ft.Text("Transacciones", theme_style=ft.TextThemeStyle.HEADLINE_SMALL),
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
                ft.Button("Filtrar", on_click=al_filtrar),
                ft.IconButton(
                    icon=ft.Icons.DOWNLOAD_OUTLINED,
                    tooltip="Exportar CSV",
                    on_click=al_exportar,
                ),
                msg_export,
            ], spacing=12),
            ft.Divider(),
            ft.Card(
                content=ft.Container(content=resumen, padding=12),
                elevation=1,
            ),
            ft.Column(controls=[tabla], scroll=ft.ScrollMode.AUTO),
        ],
        expand=True,
        spacing=12,
    )
    return columna, cargar
