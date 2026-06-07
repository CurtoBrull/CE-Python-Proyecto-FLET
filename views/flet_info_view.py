import flet as ft

SECCIONES = [
    ("¿Qué es Flet?", ft.Icons.INFO_OUTLINE),
    ("Page", ft.Icons.COMPUTER),
    ("Container", ft.Icons.CROP_SQUARE),
    ("Column y Row", ft.Icons.VIEW_COLUMN),
    ("NavigationRail", ft.Icons.MENU),
    ("DataTable", ft.Icons.TABLE_CHART),
    ("Dropdown", ft.Icons.ARROW_DROP_DOWN_CIRCLE),
    ("TextField y Button", ft.Icons.TEXT_FIELDS),
    ("Animaciones", ft.Icons.PLAY_ARROW),
]


def crear_flet_info(pag: ft.Page, on_volver=None) -> ft.Column:
    """Vista informativa sobre Flet con subpáginas explicativas."""

    def _titulo(icono, texto):
        return ft.Row(
            [ft.Icon(icono, color=ft.Colors.TEAL_400, size=28), ft.Text(texto, size=24, weight=ft.FontWeight.BOLD)],
            spacing=12,
        )

    def _subtitulo(texto):
        return ft.Text(texto, size=15, weight=ft.FontWeight.W_600, color=ft.Colors.TEAL_400)

    def _desc(texto):
        return ft.Text(texto, size=14)

    def _codigo(texto):
        return ft.Container(
            content=ft.Text(texto, size=12, font_family="monospace", selectable=True, color=ft.Colors.GREEN_300),
            bgcolor="#1A1A2E",
            padding=14,
            border_radius=8,
        )

    def _prop(nombre, desc):
        return ft.Column(
            [
                ft.Text(f"• {nombre}", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_300),
                ft.Container(ft.Text(desc, size=12), padding=6),
            ],
            spacing=2,
        )

    def _nota(texto):
        return ft.Row(
            [
                ft.Icon(ft.Icons.WARNING, size=15, color=ft.Colors.ORANGE_600),
                ft.Text(f"Nota: {texto}", size=12, color=ft.Colors.ORANGE_600, italic=True),
            ],
            spacing=8,
        )

    def _sep():
        return ft.Divider(height=1)

    # ── Secciones ──────────────────────────────────────────────────────────────

    def s_que_es():
        return [
            _titulo(ft.Icons.INFO_OUTLINE, "¿Qué es Flet?"),
            _sep(),
            _desc(
                "Flet es un framework open-source que permite crear aplicaciones "
                "multiplataforma (web, escritorio y móvil) usando únicamente Python. "
                "Internamente usa Flutter de Google como motor de renderizado, por lo que "
                "las apps tienen aspecto nativo sin necesidad de conocer HTML, CSS ni JavaScript."
            ),
            _subtitulo("Características principales"),
            _prop("Multiplataforma", "Un solo código funciona en Windows, macOS, Linux, Android, iOS y navegador web."),
            _prop("Python puro", "No se requiere conocimiento de Flutter/Dart ni de tecnologías web."),
            _prop("Material Design", "Controles integrados siguiendo el sistema de diseño de Google."),
            _prop("Tiempo real", "Las actualizaciones de UI se envían al cliente Flutter mediante WebSocket."),
            _subtitulo("Versión utilizada en esta app"),
            _codigo("import flet as ft\nprint(ft.__version__)  # 0.85.2"),
            _subtitulo("Punto de entrada"),
            _desc("La app arranca con ft.run(), que lanza un servidor web o ventana nativa:"),
            _codigo(
                "import flet as ft\n\ndef main(pag: ft.Page):\n"
                "    pag.title = \"Mi App\"\n"
                "    pag.add(ft.Text(\"Hola Flet\"))\n\n"
                "ft.run(main, port=8000, assets_dir=\"assets\")"
            ),
        ]

    def s_page():
        return [
            _titulo(ft.Icons.COMPUTER, "Page"),
            _sep(),
            _desc(
                "ft.Page es el contenedor raíz de cada sesión de usuario. Se crea "
                "automáticamente al conectarse un cliente y se recibe como parámetro "
                "en la función principal. Es el punto de configuración global de la app."
            ),
            _subtitulo("Propiedades de configuración"),
            _prop("title", "Título de la ventana de escritorio o pestaña del navegador."),
            _prop("bgcolor", "Color de fondo de la página (ft.Colors.GREY_100, etc.)."),
            _prop("theme / dark_theme", "Temas Material para modo claro y oscuro. Se configuran con ft.Theme(color_scheme_seed=...)."),
            _prop("theme_mode", "Modo activo: ft.ThemeMode.LIGHT, DARK o SYSTEM."),
            _prop("appbar", "Barra superior (ft.AppBar) con título, acciones y color de fondo."),
            _prop("favicon", "Icono de pestaña web (nombre del fichero en assets/)."),
            _prop("window.width / window.height", "Tamaño inicial de la ventana en escritorio (Flet 0.85 usa notación de punto)."),
            _prop("overlay", "Lista para añadir controles flotantes como AlertDialog."),
            _subtitulo("Métodos clave"),
            _prop("pag.update()", "Envía todos los cambios pendientes al cliente Flutter. Obligatorio tras modificar controles."),
            _prop("pag.add(control)", "Añade un control a la página."),
            _subtitulo("Uso en esta app"),
            _codigo(
                "def main(pag: ft.Page):\n"
                "    pag.title = \"Gestor de Gastos\"\n"
                "    pag.bgcolor = ft.Colors.GREY_100\n"
                "    pag.theme = ft.Theme(color_scheme_seed=ft.Colors.TEAL)\n"
                "    pag.theme_mode = ft.ThemeMode.LIGHT\n"
                "    pag.favicon = \"favicon.png\"\n"
                "    pag.window.width = 1500\n"
                "    pag.window.height = 950"
            ),
        ]

    def s_container():
        return [
            _titulo(ft.Icons.CROP_SQUARE, "Container"),
            _sep(),
            _desc(
                "Container es el control más versátil de Flet. Actúa como caja decorativa "
                "alrededor de otro control, permitiendo añadir colores, bordes, relleno, "
                "animaciones e interactividad."
            ),
            _subtitulo("Propiedades principales"),
            _prop("content", "El control hijo que contiene."),
            _prop("bgcolor", "Color de fondo sólido."),
            _prop("padding", "Espacio interior entre el borde y el contenido. Acepta entero o ft.Padding."),
            _prop("border_radius", "Radio de esquinas redondeadas en píxeles."),
            _prop("width / height", "Dimensiones fijas. Si se omiten, se adaptan al contenido."),
            _prop("expand", "Si True, ocupa todo el espacio disponible en el contenedor padre."),
            _prop("alignment", "Posición del contenido. Usa ft.Alignment(x, y) donde (-1,-1) es arriba-izquierda y (1,1) es abajo-derecha. (0,0) = centro."),
            _prop("opacity", "Transparencia: 0.0 = invisible, 1.0 = visible."),
            _prop("animate_opacity", "Activa animación de opacity. Recibe ft.Animation(duración_ms, curva)."),
            _prop("on_animation_end", "Callback ejecutado cuando termina una animación."),
            _subtitulo("Uso en esta app — transición fade"),
            _codigo(
                "area = ft.Container(\n"
                "    content=vista_inicial,\n"
                "    expand=True,\n"
                "    opacity=1,\n"
                "    animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),\n"
                ")\n\n"
                "# Disparar fade-out:\n"
                "area.opacity = 0\n"
                "pag.update()"
            ),
        ]

    def s_column_row():
        return [
            _titulo(ft.Icons.VIEW_COLUMN, "Column y Row"),
            _sep(),
            _desc(
                "Column y Row son los controles de layout fundamentales. Column organiza "
                "sus hijos verticalmente y Row horizontalmente."
            ),
            _subtitulo("Propiedades compartidas"),
            _prop("controls", "Lista de controles hijos."),
            _prop("spacing", "Separación en píxeles entre controles. Por defecto 10."),
            _prop("expand", "Ocupa todo el espacio disponible en el padre."),
            _prop("scroll", "Activa scroll si el contenido desborda. Valor: ft.ScrollMode.AUTO, ALWAYS, HIDDEN, etc."),
            _prop("alignment", "Alineación en el eje principal: ft.MainAxisAlignment.START / CENTER / END / SPACE_BETWEEN / SPACE_EVENLY."),
            _subtitulo("Exclusivas de Column"),
            _prop("horizontal_alignment", "Alineación horizontal de los hijos: ft.CrossAxisAlignment.START / CENTER / END."),
            _subtitulo("Exclusivas de Row"),
            _prop("vertical_alignment", "Alineación vertical de los hijos: ft.CrossAxisAlignment.START / CENTER / END."),
            _prop("wrap", "Si True, los hijos pasan a línea siguiente al desbordarse."),
            _subtitulo("Uso en esta app"),
            _codigo(
                "# Column con scroll para la tabla de transacciones\n"
                "ft.Column(controls=[tabla], scroll=ft.ScrollMode.AUTO)\n\n"
                "# Row para layout horizontal: formulario + lista\n"
                "ft.Row(\n"
                "    controls=[panel_form, contenedor_lista],\n"
                "    expand=True,\n"
                ")"
            ),
        ]

    def s_nav():
        return [
            _titulo(ft.Icons.MENU, "NavigationRail"),
            _sep(),
            _desc(
                "NavigationRail es un componente Material Design para navegar entre un "
                "número reducido de vistas (2-5). Se posiciona en el lateral de la app, "
                "siendo ideal para pantallas anchas como escritorio o tablet."
            ),
            _subtitulo("Propiedades principales"),
            _prop("selected_index", "Índice del destino actualmente seleccionado."),
            _prop("destinations", "Lista de NavigationRailDestination (mínimo 2). Cada uno tiene icon, selected_icon y label."),
            _prop("label_type", "Visibilidad de etiquetas: ft.NavigationRailLabelType.ALL / SELECTED / NONE."),
            _prop("trailing", "Control colocado debajo de todos los destinos. En esta app se usa para el botón de salir (LOGOUT)."),
            _prop("on_change", "Evento al cambiar de destino. Se lee e.control.selected_index."),
            _prop("bgcolor", "Color de fondo del rail."),
            _prop("min_width", "Ancho mínimo en píxeles. Por defecto 72."),
            _nota("En Flet 0.85 ft.Tabs tiene bugs al pasar parámetros. Se usa NavigationRail como alternativa estable."),
            _subtitulo("Uso en esta app"),
            _codigo(
                "rail = ft.NavigationRail(\n"
                "    selected_index=0,\n"
                "    label_type=ft.NavigationRailLabelType.ALL,\n"
                "    min_width=100,\n"
                "    destinations=[\n"
                "        ft.NavigationRailDestination(\n"
                "            icon=ft.Icons.LIST_ALT_OUTLINED,\n"
                "            selected_icon=ft.Icons.LIST_ALT,\n"
                "            label=\"Transacciones\",\n"
                "        ),\n"
                "    ],\n"
                "    trailing=ft.IconButton(\n"
                "        icon=ft.Icons.LOGOUT,\n"
                "        tooltip=\"Volver a inicio\",\n"
                "        on_click=lambda e: _salir_cb[0](e),\n"
                "    ),\n"
                "    on_change=navegar,\n"
                ")"
            ),
        ]

    def s_datatable():
        return [
            _titulo(ft.Icons.TABLE_CHART, "DataTable"),
            _sep(),
            _desc(
                "DataTable muestra datos en formato tabla Material Design con filas y "
                "columnas. Soporta ordenación interactiva haciendo clic en los encabezados."
            ),
            _subtitulo("Estructura"),
            _prop("columns", "Lista de DataColumn. Cada columna tiene: label (control visible), numeric (alinea a la derecha), on_sort (callback de ordenación)."),
            _prop("rows", "Lista de DataRow. Cada fila tiene cells=[DataCell(content=control)]."),
            _prop("sort_column_index", "Índice de la columna activa de ordenación (muestra indicador visual)."),
            _prop("sort_ascending", "True para orden ascendente, False para descendente."),
            _prop("column_spacing", "Espacio horizontal entre columnas."),
            _subtitulo("Patrón de ordenación con lambdas"),
            _desc("Esta app usa un diccionario de lambdas indexado por columna para ordenar dinámicamente:"),
            _codigo(
                "SORT_KEYS = [\n"
                "    lambda t: str(t.fecha),\n"
                "    lambda t: t.tipo.value,\n"
                "    lambda t: t.categoria.value,\n"
                "    lambda t: t.descripcion,\n"
                "    lambda t: t.importe,\n"
                "]\n\n"
                "def al_ordenar(e):\n"
                "    col = e.column_index\n"
                "    sort_estado[\"asc\"] = not sort_estado[\"asc\"]\n"
                "    trans_actual.sort(\n"
                "        key=SORT_KEYS[col],\n"
                "        reverse=not sort_estado[\"asc\"],\n"
                "    )"
            ),
            _nota("Usar tabla.rows.clear() en lugar de tabla.rows = [] para que Flet detecte el cambio."),
        ]

    def s_dropdown():
        return [
            _titulo(ft.Icons.ARROW_DROP_DOWN_CIRCLE, "Dropdown"),
            _sep(),
            _desc(
                "Dropdown permite seleccionar una única opción de una lista desplegable. "
                "Es el control principal de filtrado en la vista de transacciones."
            ),
            _subtitulo("Propiedades principales"),
            _prop("options", "Lista de ft.dropdown.Option(key=..., text=...). La key es el valor interno, text el visible."),
            _prop("value", "Clave de la opción seleccionada actualmente."),
            _prop("label", "Etiqueta descriptiva del campo."),
            _prop("width", "Ancho en píxeles."),
            _prop("ref", "ft.Ref[ft.Dropdown]() para acceder al control desde callbacks sin variables globales."),
            _subtitulo("Patrón ft.Ref"),
            _desc("ft.Ref permite acceder a un control creado en otro ámbito:"),
            _codigo(
                "mes_ref = ft.Ref[ft.Dropdown]()\n\n"
                "# Crear el Dropdown con ref=\n"
                "ft.Dropdown(ref=mes_ref, label=\"Mes\", value=\"0\", options=[...])\n\n"
                "# Leer el valor desde un callback:\n"
                "def al_filtrar(e):\n"
                "    valor = mes_ref.current.value"
            ),
            _nota("En Flet 0.85 on_change no funciona si se asigna tras crear el control. Solución: botón 'Filtrar' que dispara la carga manualmente."),
        ]

    def s_textfield_button():
        return [
            _titulo(ft.Icons.TEXT_FIELDS, "TextField y Button"),
            _sep(),
            _subtitulo("TextField"),
            _desc("Campo de entrada de texto. Soporta validación, tipo de teclado, modo multilínea y acceso por referencia."),
            _prop("label", "Etiqueta flotante del campo."),
            _prop("value", "Valor actual del campo."),
            _prop("ref", "ft.Ref[ft.TextField]() para leer/escribir el valor desde callbacks."),
            _prop("keyboard_type", "Tipo de teclado virtual: ft.KeyboardType.NUMBER, EMAIL, URL, etc."),
            _prop("multiline", "Si True, permite múltiples líneas de texto."),
            _prop("read_only", "Si True, el usuario no puede editar el contenido."),
            _prop("min_lines / max_lines", "Altura mínima y máxima del campo multilínea."),
            _subtitulo("Button"),
            _desc("Botón de acción principal Material Design."),
            _nota("ElevatedButton está deprecado en Flet 0.85 — usar ft.Button."),
            _prop("text", "Texto visible del botón."),
            _prop("on_click", "Callback ejecutado al pulsar."),
            _prop("width", "Ancho fijo en píxeles."),
            _prop("style", "ft.ButtonStyle con bgcolor, color y padding para personalizar la apariencia."),
            _subtitulo("IconButton"),
            _desc("Botón compacto con icono, ideal para acciones secundarias en listas o barras."),
            _prop("icon", "Icono de ft.Icons.XXX."),
            _prop("tooltip", "Texto emergente al pasar el cursor."),
            _prop("icon_color", "Color del icono."),
            _prop("on_click", "Callback al pulsar."),
            _codigo(
                "ft.Button(\n"
                "    \"Guardar\",\n"
                "    on_click=guardar,\n"
                "    width=300,\n"
                "    style=ft.ButtonStyle(\n"
                "        bgcolor=ft.Colors.TEAL_700,\n"
                "        color=ft.Colors.WHITE,\n"
                "        padding=16,\n"
                "    ),\n"
                ")"
            ),
        ]

    def s_animaciones():
        return [
            _titulo(ft.Icons.PLAY_ARROW, "Animaciones"),
            _sep(),
            _desc(
                "Flet permite animar propiedades de controles de forma declarativa. "
                "Al cambiar una propiedad animada, Flutter interpola automáticamente "
                "entre el valor anterior y el nuevo."
            ),
            _subtitulo("animate_opacity"),
            _prop("Valor", "ft.Animation(duración_ms, curva). Activa la animación de la propiedad opacity."),
            _prop("ft.AnimationCurve", "Curva de interpolación: EASE_IN_OUT, LINEAR, BOUNCE_OUT, EASE_IN, EASE_OUT, etc."),
            _prop("on_animation_end", "Callback ejecutado cuando la animación termina. Clave del patrón de transición."),
            _subtitulo("Patrón fade entre vistas"),
            _desc("Esta app usa un doble fade para cambiar entre vistas sin solapamientos:"),
            _codigo(
                "# 1. Configurar el contenedor animado\n"
                "area = ft.Container(\n"
                "    animate_opacity=ft.Animation(250, ft.AnimationCurve.EASE_IN_OUT),\n"
                "    opacity=1,\n"
                ")\n\n"
                "# 2. Al navegar: guardar contenido nuevo y disparar fade-out\n"
                "def navegar(e):\n"
                "    contenido_pendiente[0] = nueva_vista\n"
                "    area.opacity = 0   # Flutter anima hasta 0\n"
                "    pag.update()\n\n"
                "# 3. Al terminar fade-out: cambiar contenido y fade-in\n"
                "def on_fade_out(e):\n"
                "    area.content = contenido_pendiente[0]\n"
                "    contenido_pendiente[0] = None\n"
                "    area.opacity = 1   # Flutter anima hasta 1\n"
                "    pag.update()\n\n"
                "area.on_animation_end = on_fade_out"
            ),
            _subtitulo("Lista mutable para closures anidadas"),
            _desc("Python no permite reasignar variables de scope externo en closures. Se usa una lista de un elemento como workaround:"),
            _codigo(
                "# En lugar de: contenido_pendiente = None\n"
                "contenido_pendiente = [None]  # lista mutable\n\n"
                "def callback(e):\n"
                "    contenido_pendiente[0] = nueva_vista  # funciona\n"
                "    # nueva_vista = ...  # Error: UnboundLocalError"
            ),
        ]

    CONTENIDOS = [s_que_es, s_page, s_container, s_column_row, s_nav, s_datatable, s_dropdown, s_textfield_button, s_animaciones]

    def _nueva_columna(idx):
        return ft.Column(
            controls=CONTENIDOS[idx](),
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=14,
        )

    contenedor_scroll = ft.Container(
        content=_nueva_columna(0),
        expand=True,
    )

    nav_items = []
    seccion_activa = [0]

    def seleccionar(idx):
        seccion_activa[0] = idx
        for i, item in enumerate(nav_items):
            activo = i == idx
            item.bgcolor = ft.Colors.TEAL_700 if activo else None
            item.content.controls[0].color = ft.Colors.WHITE if activo else ft.Colors.TEAL_400
            item.content.controls[1].color = ft.Colors.WHITE if activo else None
        contenedor_scroll.content = _nueva_columna(idx)
        pag.update()

    for i, (nombre, icono) in enumerate(SECCIONES):
        def hacer_click(idx):
            return lambda e: seleccionar(idx)

        nav_items.append(
            ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(icono, size=16, color=ft.Colors.WHITE if i == 0 else ft.Colors.TEAL_400),
                        ft.Text(nombre, size=13, color=ft.Colors.WHITE if i == 0 else None),
                    ],
                    spacing=8,
                ),
                padding=10,
                border_radius=8,
                on_click=hacer_click(i),
                bgcolor=ft.Colors.TEAL_700 if i == 0 else None,
            )
        )

    sidebar = ft.Container(
        content=ft.Column(controls=nav_items, spacing=4, scroll=ft.ScrollMode.AUTO),
        width=210,
        padding=12,
    )

    cuerpo = ft.Row(
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(content=contenedor_scroll, expand=True, padding=20),
        ],
        expand=True,
    )

    if on_volver:
        cabecera = ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.Icons.ARROW_BACK,
                        on_click=on_volver,
                        tooltip="Volver a inicio",
                    ),
                    ft.Text("Documentación Flet", size=18, weight=ft.FontWeight.BOLD),
                ],
                spacing=4,
            ),
            padding=8,
            bgcolor=ft.Colors.TEAL_700,
        )
        return ft.Column(controls=[cabecera, cuerpo], expand=True, spacing=0)

    return ft.Column(controls=[cuerpo], expand=True, spacing=0)
