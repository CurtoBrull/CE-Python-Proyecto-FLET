# Gestor de Gastos Personales — Proyecto Flet CE

## Idea

App de escritorio para **registrar y visualizar gastos e ingresos personales**.
Sin complicaciones, sin usuarios. Datos en **PostgreSQL serverless (Neon)**.

### Por qué encaja con el CE

| Criterio | Cómo lo cubre |
|---|---|
| POO | Clases `Transaccion`, `CategoriaEnum`, capa `Database` |
| Persistencia | PostgreSQL serverless en Neon con `psycopg2` |
| Interfaz gráfica | Flet (Flutter en Python) |
| Visualización de datos | Gráfico de barras nativo de Flet (`ft.BarChart`) |
| Complejidad justa | CRUD + filtros + resumen estadístico. Alcanzable en 2 semanas |

---

## Funcionalidades

1. **Añadir transacción** — tipo (gasto/ingreso), importe, categoría, fecha, descripción
2. **Listar transacciones** — tabla con scroll, orden por fecha
3. **Filtrar** — por mes y/o categoría
4. **Eliminar** transacción
5. **Resumen** — total ingresos, total gastos, balance
6. **Gráfico** — gastos por categoría (barras)

---

## Estructura del proyecto

```
flet/
├── main.py              # Punto de entrada, app Flet
├── database.py          # Capa de acceso a PostgreSQL (Neon)
├── models.py            # Dataclasses / modelos de datos
├── views/
│   ├── form_view.py     # Formulario añadir transacción
│   ├── list_view.py     # Tabla de transacciones
│   └── chart_view.py    # Gráfico de barras
├── .env                 # DATABASE_URL de Neon (no subir a git)
├── .env.example         # Plantilla sin credenciales (sí subir)
└── requirements.txt
```

---

## Pila tecnológica

- **Python 3.11+**
- **Flet** — UI (wrapper de Flutter)
- **Neon** — PostgreSQL serverless en la nube
- **psycopg2-binary** — driver PostgreSQL para Python
- **python-dotenv** — gestión de credenciales (connection string)
- **dataclasses** — modelos limpios (stdlib)

---

## Setup inicial

### 1. Entorno virtual

```powershell
cd "C:\Mega\CE-Desarrollo-de-Aplicaciones-en-Lenguaje-Python\Proyectos\flet"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Instalar dependencias

```powershell
pip install flet psycopg2-binary python-dotenv
```

### 3. Configurar credenciales Neon

Crear fichero `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://user:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require
```

> La connection string se obtiene en **Neon Console → proyecto → Connection Details**.

### 4. Verificar instalación

```powershell
python -c "import flet; print(flet.version.version)"
python -c "import psycopg2; print(psycopg2.__version__)"
```

### 4. Ejecutar la app (cuando esté construida)

```powershell
python main.py
```

### 5. Ver la app en el móvil Android

Flet permite previsualizar la app en un dispositivo Android sin compilar ni generar un APK.

**Requisitos:**
- Móvil y PC en la **misma red WiFi**
- App **Flet** instalada en el móvil (Google Play Store → "Flet")

**Ejecutar:**

```powershell
flet run --android main.py
```

Aparecerá un **código QR en la terminal**. Ábrelo con la app Flet del móvil y la app se cargará en tiempo real.

> Cualquier cambio que guardes en el código se recargará automáticamente en el móvil mientras el servidor esté activo.

---

## Plan de construcción paso a paso

| Paso | Qué construimos | Conceptos clave |
|---|---|---|
| 1 | Hola mundo Flet — ventana básica | `ft.app()`, `ft.Page`, controles básicos |
| 2 | Modelos de datos | `dataclasses`, `Enum`, tipos Python |
| 3 | Capa de base de datos | `psycopg2`, conexión Neon, CRUD, patrón repositorio |
| 4 | Formulario de entrada | `TextField`, `Dropdown`, `ElevatedButton`, eventos |
| 5 | Lista de transacciones | `DataTable`, `ListView`, actualización de estado |
| 6 | Filtros y resumen | Lógica de negocio, `ft.Row`/`Column` layout |
| 7 | Gráfico de barras | `ft.BarChart`, transformar datos para visualización |
| 8 | Pulir navegación y estilo | `NavigationRail`, temas, colores |

---

---

## Paso 1 — Hola mundo Flet

### Cómo funciona Flet

Flet es una librería que envuelve Flutter (el framework de UI de Google) para usarlo desde Python.
Cuando ejecutas `python main.py`, Flet arranca un proceso Flutter en segundo plano y te muestra una ventana nativa de escritorio.

**Flujo básico:**

```
python main.py
    └─► ft.run(main)
            └─► crea ft.Page  (la ventana)
                    └─► llama a tu función main(page)
                            └─► tú añades controles a page
```

### Conceptos clave

| Concepto | Qué es |
|---|---|
| `ft.run(main)` | Arranca la app. `target` es la función que recibe la página |
| `ft.Page` | La ventana. Tiene propiedades: `title`, `width`, `height`, `theme_mode`, etc. |
| `page.add(control)` | Añade un control (widget) a la ventana y lo renderiza |
| `page.update()` | Refresca la UI después de cambiar algo (necesario cuando modificas controles existentes) |
| Control | Cualquier elemento visual: texto, botón, campo de texto, columna... |

### Controles básicos que usarás

```python
ft.Text("Hola")                    # Texto estático
ft.Button("Click")         # Botón con relieve
ft.TextField(label="Nombre")       # Campo de texto
ft.Column([control1, control2])    # Apila controles en vertical
ft.Row([control1, control2])       # Apila controles en horizontal
ft.Container(content=..., padding=10)  # Caja con padding/margin/color
```

### Eventos

Los eventos se pasan como funciones (callbacks):

```python
def al_pulsar(e):          # e = evento, contiene info del click
    print("pulsado")

ft.Button("Click", on_click=al_pulsar)
```

`e` tiene propiedades útiles:

- `e.control` — el control que disparó el evento
- `e.page` — la página actual

### Tu tarea — crear `main.py`

Crea el fichero `main.py` en la raíz del proyecto con este contenido:

```python
import flet as ft


def main(page: ft.Page) -> None:
    # Configuración de la ventana
    page.title = "Gestor de Gastos"
    page.window.width = 900
    page.window.height = 650
    page.theme_mode = ft.ThemeMode.LIGHT

    # Contador simple para probar eventos
    contador = ft.Text("Clics: 0", size=20)
    clics = 0

    def al_pulsar(e):
        nonlocal clics
        clics += 1
        contador.value = f"Clics: {clics}"
        page.update()

    # Layout inicial
    page.add(
        ft.Column(
            controls=[
                ft.Text("Gestor de Gastos Personales", size=30, weight=ft.FontWeight.BOLD),
                ft.Text("Bienvenido. La app está en construcción.", size=16),
                ft.Button("Pulsa aquí", on_click=al_pulsar),
                contador,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


ft.run(main)
```

### Ejecutar

```powershell
python main.py
```

Debe abrirse una ventana de escritorio. Al pulsar el botón, el contador sube.

### Qué demuestra este paso

- `ft.app()` arranca el bucle de eventos de Flutter
- La función `main(page)` es el punto de entrada de la UI
- `nonlocal` permite modificar variables del scope externo desde un callback
- `page.update()` es **obligatorio** para que los cambios en controles existentes se reflejen en pantalla
- `ft.Column` organiza controles en vertical con `spacing` entre ellos

### Comprueba que funciona

- [ ] Se abre la ventana con título "Gestor de Gastos"
- [ ] Se ve el texto de bienvenida
- [ ] Al pulsar el botón, el contador incrementa
- [ ] La ventana tiene ~900x650 px

Cuando lo tengas funcionando, avisa y pasamos al **Paso 2 — Modelos de datos**.

---

## Paso 2 — Modelos de datos

### Qué es una dataclass

Una `dataclass` es una clase Python donde declaras los atributos con tipos y Python genera automáticamente `__init__`, `__repr__` y `__eq__`. Menos código, más legible.

```python
# Sin dataclass
class Punto:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

# Con dataclass — equivalente exacto
from dataclasses import dataclass

@dataclass
class Punto:
    x: float
    y: float
```

### Qué es un Enum

`Enum` define un conjunto fijo de valores con nombre. Evita usar strings sueltos ("gasto", "ingreso") que son propensos a typos.

```python
from enum import Enum

class Color(Enum):
    ROJO = "rojo"
    AZUL = "azul"

# Uso
c = Color.ROJO
print(c.value)   # "rojo"
print(c.name)    # "ROJO"
```

### Tu tarea — crear `models.py`

Crea `models.py` en la raíz del proyecto:

```python
from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class TipoTransaccion(Enum):
    GASTO = "gasto"
    INGRESO = "ingreso"


class Categoria(Enum):
    ALIMENTACION = "Alimentación"
    TRANSPORTE = "Transporte"
    VIVIENDA = "Vivienda"
    OCIO = "Ocio"
    SALUD = "Salud"
    EDUCACION = "Educación"
    OTROS = "Otros"


@dataclass
class Transaccion:
    tipo: TipoTransaccion
    importe: float
    categoria: Categoria
    descripcion: str
    fecha: date = field(default_factory=date.today)
    id: int | None = None   # None hasta que la BD asigne el id real
```

### Puntos clave

| Elemento | Por qué |
|---|---|
| `field(default_factory=date.today)` | Ejecuta `date.today()` en el momento de crear el objeto, no al definir la clase |
| `id: int \| None = None` | El id lo asigna PostgreSQL (SERIAL). Antes de insertar no existe |
| `Enum` para tipo y categoría | La BD guardará el `.value` ("gasto", "Alimentación"...) |

### Verificar en la terminal

Sin crear fichero nuevo, prueba directamente:

```powershell
python -c "
from models import Transaccion, TipoTransaccion, Categoria
t = Transaccion(TipoTransaccion.GASTO, 45.50, Categoria.ALIMENTACION, 'Supermercado')
print(t)
"
```

Debe imprimir algo como:
```
Transaccion(tipo=<TipoTransaccion.GASTO: 'gasto'>, importe=45.5, categoria=<Categoria.ALIMENTACION: 'Alimentación'>, descripcion='Supermercado', fecha=2026-06-06, id=None)
```

### Comprueba que funciona

- [ ] `models.py` creado sin errores de sintaxis
- [ ] El print muestra todos los campos correctamente
- [ ] `fecha` tiene el valor de hoy automáticamente
- [ ] `id` es `None`

Cuando lo tengas, avisa y pasamos al **Paso 3 — Base de datos con Neon**.

---

## Paso 3 — Base de datos con Neon

### Antes de escribir código

Necesitas tener la connection string de Neon. Si aún no tienes cuenta:

1. Entra en [neon.tech](https://neon.tech) y crea una cuenta gratuita
2. Crea un proyecto nuevo (cualquier nombre)
3. En el dashboard: **Connection Details → Connection string**
4. Copia la cadena que empieza por `postgresql://...`
5. Crea el fichero `.env` en la raíz del proyecto:

```env
DATABASE_URL=postgresql://user:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require
```

### Cómo funciona python-dotenv

`python-dotenv` lee el fichero `.env` y carga las variables como variables de entorno del proceso. Así las credenciales no están hardcodeadas en el código.

```python
from dotenv import load_dotenv
import os

load_dotenv()                          # lee .env
url = os.getenv("DATABASE_URL")        # recupera el valor
```

### Cómo funciona psycopg2

`psycopg2` es el driver que conecta Python con PostgreSQL. Flujo básico:

```
connection = psycopg2.connect(url)   # abre conexión TCP con Neon
cursor = connection.cursor()         # cursor para ejecutar SQL
cursor.execute("SELECT ...")         # ejecuta la query
connection.commit()                  # confirma cambios (INSERT/UPDATE/DELETE)
cursor.close()
connection.close()
```

Neon es serverless — cada conexión se establece en ~100ms. Para una app de escritorio no necesitamos pool de conexiones, basta con abrir/cerrar por operación.

### Tu tarea — crear `database.py`

```python
import os
import psycopg2
from dotenv import load_dotenv
from models import Transaccion, TipoTransaccion, Categoria
from datetime import date

load_dotenv()


def _conectar():
    """Abre y devuelve una conexión a Neon."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def init_db() -> None:
    """Crea la tabla transacciones si no existe."""
    conn = _conectar()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id          SERIAL PRIMARY KEY,
            tipo        VARCHAR(10)  NOT NULL,
            importe     NUMERIC(10,2) NOT NULL,
            categoria   VARCHAR(50)  NOT NULL,
            descripcion TEXT,
            fecha       DATE         NOT NULL
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


def insertar(t: Transaccion) -> int:
    """Inserta una transacción y devuelve el id asignado."""
    conn = _conectar()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO transacciones (tipo, importe, categoria, descripcion, fecha)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id
        """,
        (t.tipo.value, t.importe, t.categoria.value, t.descripcion, t.fecha),
    )
    nuevo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return nuevo_id


def obtener_todas() -> list[Transaccion]:
    """Devuelve todas las transacciones ordenadas por fecha descendente."""
    conn = _conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, tipo, importe, categoria, descripcion, fecha
        FROM transacciones
        ORDER BY fecha DESC
    """)
    filas = cur.fetchall()
    cur.close()
    conn.close()

    resultado = []
    for fila in filas:
        id_, tipo, importe, categoria, descripcion, fecha = fila
        t = Transaccion(
            tipo=TipoTransaccion(tipo),
            importe=float(importe),
            categoria=Categoria(categoria),
            descripcion=descripcion,
            fecha=fecha,
            id=id_,
        )
        resultado.append(t)
    return resultado


def eliminar(id_transaccion: int) -> None:
    """Elimina una transacción por su id."""
    conn = _conectar()
    cur = conn.cursor()
    cur.execute("DELETE FROM transacciones WHERE id = %s", (id_transaccion,))
    conn.commit()
    cur.close()
    conn.close()
```

### Por qué `%s` y no f-strings en SQL

```python
# MAL — SQL injection posible
cur.execute(f"DELETE FROM transacciones WHERE id = {id}")

# BIEN — psycopg2 sanitiza el valor
cur.execute("DELETE FROM transacciones WHERE id = %s", (id,))
```

Siempre pasar los valores como segundo argumento, nunca interpolarlos en el string.

### Verificar conexión y tabla

```powershell
python -c "
from database import init_db, insertar, obtener_todas
from models import Transaccion, TipoTransaccion, Categoria

init_db()
print('Tabla creada o ya existía')

t = Transaccion(TipoTransaccion.GASTO, 12.50, Categoria.ALIMENTACION, 'Café')
nuevo_id = insertar(t)
print(f'Insertado con id: {nuevo_id}')

todas = obtener_todas()
print(f'Total registros: {len(todas)}')
print(todas[0])
"
```

### Comprueba que funciona

- [ ] `.env` creado con la connection string real de Neon
- [ ] `init_db()` no lanza error
- [ ] `insertar()` devuelve un id numérico
- [ ] `obtener_todas()` devuelve la transacción insertada

Cuando lo tengas, avisa y pasamos al **Paso 4 — Formulario de entrada**.

---

## Paso 4 — Formulario de entrada

### Estructura de carpetas

Primero crea la carpeta `views/` y un `__init__.py` vacío dentro:

```powershell
New-Item -ItemType Directory views
New-Item -ItemType File views/__init__.py
```

### Cómo funciona un formulario en Flet

Un formulario en Flet es simplemente un conjunto de controles agrupados en un `ft.Column`.
No existe un widget "Form" especial — tú conectas los controles manualmente con eventos.

Patrón de un formulario:

```
TextField / Dropdown   ← el usuario introduce datos
ElevatedButton         ← dispara on_click
  └─► callback         ← lees .value de cada control
       └─► validas
            └─► llamas a database.insert()
                 └─► limpias el formulario
```

### Controles nuevos en este paso

| Control | Uso |
|---|---|
| `ft.Dropdown` | Lista desplegable. Sus opciones son `ft.dropdown.Option(key, text)` |
| `ft.TextField` | Campo de texto. `.value` devuelve lo escrito |
| `ft.SnackBar` | Mensaje temporal en la parte inferior de la ventana |
| `ref=ft.Ref[T]()` | Referencia a un control para acceder a él fuera de donde se define |

### `ft.Ref` — acceder a controles desde callbacks

En Flet los controles se definen al construir el layout. Para leer su valor desde un callback usamos `Ref`:

```python
importe_ref = ft.Ref[ft.TextField]()

ft.TextField(ref=importe_ref, label="Importe")

def guardar(e):
    valor = importe_ref.current.value   # accede al TextField
```

### Tu tarea — crear `views/form_view.py`

```python
import flet as ft
from database import insert
from models import Transaccion, TipoTransaccion, Categoria


def crear_formulario(page: ft.Page, on_guardado) -> ft.Column:
    """Devuelve el formulario de nueva transacción como un Column."""

    tipo_ref = ft.Ref[ft.Dropdown]()
    importe_ref = ft.Ref[ft.TextField]()
    categoria_ref = ft.Ref[ft.Dropdown]()
    descripcion_ref = ft.Ref[ft.TextField]()

    def guardar(e):
        # Validación básica
        if not importe_ref.current.value:
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

        t = Transaccion(
            tipo=TipoTransaccion(tipo_ref.current.value),
            importe=importe,
            categoria=Categoria(categoria_ref.current.value),
            descripcion=descripcion_ref.current.value or "",
        )
        insert(t)

        # Limpiar formulario
        importe_ref.current.value = ""
        descripcion_ref.current.value = ""
        page.snack_bar = ft.SnackBar(ft.Text("Transacción guardada"))
        page.snack_bar.open = True
        page.update()

        on_guardado()  # avisa a main.py para refrescar la lista

    return ft.Column(
        controls=[
            ft.Text("Nueva transacción", size=22, weight=ft.FontWeight.BOLD),
            ft.Dropdown(
                ref=tipo_ref,
                label="Tipo",
                value=TipoTransaccion.GASTO.value,
                options=[ft.dropdown.Option(t.value) for t in TipoTransaccion],
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
            ft.Button("Guardar", on_click=guardar, width=300),
        ],
        spacing=16,
    )
```

### Conectar el formulario a `main.py`

Sustituye el contenido de `main.py` por esto:

```python
import flet as ft
from database import init_db
from views.form_view import crear_formulario


def main(page: ft.Page) -> None:
    page.title = "Gestor de Gastos"
    page.window.width = 900
    page.window.height = 650
    page.theme_mode = ft.ThemeMode.LIGHT

    init_db()

    def on_guardado():
        pass  # en el paso 5 refrescará la lista

    page.add(crear_formulario(page, on_guardado))


ft.run(main)
```

### Comprueba que funciona

- [ ] Aparece el formulario con los campos
- [ ] El Dropdown de tipo muestra Gasto/Ingreso
- [ ] El Dropdown de categoría muestra todas las categorías
- [ ] Al guardar sin importe aparece el SnackBar de error
- [ ] Al guardar con datos correctos aparece "Transacción guardada"
- [ ] En Neon Console puedes ver el registro insertado

Cuando lo tengas, avisa y pasamos al **Paso 5 — Lista de transacciones**.

---

## Paso 5 — Lista de transacciones

### Diseño de la pantalla

A partir de este paso la app tendrá dos zonas en horizontal:

```
┌─────────────────┬──────────────────────────────────────┐
│   Formulario    │   Lista de transacciones             │
│   (350px)       │   + resumen (balance, totales)       │
└─────────────────┴──────────────────────────────────────┘
```

Esto se logra con `ft.Row` donde el formulario tiene ancho fijo y la lista ocupa el espacio restante con `ft.Expanded`.

### Controles nuevos en este paso

| Control | Uso |
|---|---|
| `ft.DataTable` | Tabla con cabeceras y filas. Columnas = `ft.DataColumn`, filas = `ft.DataRow`, celdas = `ft.DataCell` |
| `ft.Expanded` | Ocupa todo el espacio disponible dentro de un `Row` o `Column` |
| `ft.Divider` | Línea separadora horizontal |
| `ft.IconButton` | Botón con icono, sin texto |

### `ft.DataTable` — estructura básica

```python
ft.DataTable(
    columns=[
        ft.DataColumn(ft.Text("Fecha")),
        ft.DataColumn(ft.Text("Importe"), numeric=True),
    ],
    rows=[
        ft.DataRow(cells=[
            ft.DataCell(ft.Text("2026-06-07")),
            ft.DataCell(ft.Text("12.50 €")),
        ]),
    ],
)
```

### Tu tarea — crear `views/list_view.py`

```python
import flet as ft
from database import get_all, delete
from models import TipoTransaccion


def crear_lista(page: ft.Page, on_eliminado) -> ft.Column:
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
        transacciones = get_all()

        tabla.rows = []
        for t in transacciones:
            color = ft.colors.RED_400 if t.tipo == TipoTransaccion.GASTO else ft.colors.GREEN_400

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
                        icon=ft.icons.DELETE_OUTLINE,
                        icon_color=ft.colors.RED_300,
                        on_click=hacer_eliminar(t.id),
                    )),
                ])
            )

        ingresos = sum(t.importe for t in transacciones if t.tipo == TipoTransaccion.INGRESO)
        gastos = sum(t.importe for t in transacciones if t.tipo == TipoTransaccion.GASTO)
        balance = ingresos - gastos
        color_balance = ft.colors.GREEN_600 if balance >= 0 else ft.colors.RED_600

        resumen.value = f"Ingresos: {ingresos:.2f} €   Gastos: {gastos:.2f} €   Balance: {balance:.2f} €"
        resumen.color = color_balance

    cargar()

    return ft.Column(
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
```

> **Por qué `hacer_eliminar(tran_id)`** — si usaras `lambda e: delete(t.id)` directamente en el bucle, todos los botones capturarían el mismo `t` (el último del bucle). `hacer_eliminar` crea un nuevo scope por cada iteración, capturando el `id` correcto. Es el clásico problema de closures en bucles.

### Actualizar `main.py`

```python
import flet as ft
from database import init_db
from views.form_view import create_form
from views.list_view import crear_lista


def main(page: ft.Page) -> None:
    page.title = "Gestor de Gastos"
    page.window.width = 900
    page.window.height = 650
    page.theme_mode = ft.ThemeMode.LIGHT

    init_db()

    lista_ref = ft.Ref[ft.Column]()

    def refrescar(e=None):
        # Reconstruye la lista y reemplaza el contenido
        nueva_lista = crear_lista(page, refrescar)
        lista_ref.current.controls = nueva_lista.controls
        page.update()

    formulario = create_form(page, refrescar)
    lista = crear_lista(page, refrescar)
    lista.ref = lista_ref

    page.add(
        ft.Row(
            controls=[
                ft.Container(content=formulario, width=350, padding=20),
                ft.VerticalDivider(),
                ft.Container(content=lista, expand=True, padding=20),
            ],
            expand=True,
        )
    )


ft.run(main)
```

### Por qué `hacer_eliminar(tran_id)` y no lambda

```python
# MAL — todos los botones eliminan el último t.id del bucle
ft.IconButton(on_click=lambda e: delete(t.id))

# BIEN — cada botón captura su propio id
ft.IconButton(on_click=hacer_eliminar(t.id))
```

### Comprueba que funciona

- [ ] La app muestra formulario a la izquierda y lista a la derecha
- [ ] Las transacciones existentes aparecen en la tabla
- [ ] El resumen muestra los totales correctos
- [ ] Al guardar una transacción nueva aparece en la lista automáticamente
- [ ] El botón de eliminar borra la fila y actualiza el resumen

Cuando lo tengas, avisa y pasamos al **Paso 6 — Filtros**.

---

## Paso 6 — Filtros

### Qué vamos a añadir

Dos Dropdowns encima de la tabla: **mes** y **categoría**.
Al cambiar cualquiera, la tabla se repopula solo con las filas que coinciden.

```
[ Mes: Todos ▼ ]  [ Categoría: Todas ▼ ]
─────────────────────────────────────────
│ Fecha │ Tipo │ Categoría │ ...        │
```

### Cambio en `database.py` — añadir `get_filtradas()`

La query usa `WHERE` condicional: si el filtro es `None` no aplica esa condición.

Añade esta función al final de `database.py`:

```python
def get_filtradas(mes: int | None = None, categoria: str | None = None) -> list[Transaccion]:
    """Devuelve transacciones aplicando filtros opcionales de mes y categoría."""
    condiciones = []
    valores = []

    if mes is not None:
        condiciones.append("EXTRACT(MONTH FROM fecha) = %s")
        valores.append(mes)

    if categoria is not None:
        condiciones.append("categoria = %s")
        valores.append(categoria)

    where = ("WHERE " + " AND ".join(condiciones)) if condiciones else ""

    with _conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT id, tipo, importe, categoria, descripcion, fecha "
                f"FROM transacciones {where} ORDER BY fecha DESC",
                valores or None,
            )
            filas = cur.fetchall()

    return [
        Transaccion(
            id=f[0],
            tipo=TipoTransaccion(f[1]),
            importe=float(f[2]),
            categoria=Categoria(f[3]),
            descripcion=f[4],
            fecha=f[5],
        )
        for f in filas
    ]
```

> `EXTRACT(MONTH FROM fecha)` es SQL estándar PostgreSQL — devuelve el número de mes (1–12).

### Cambio en `list_view.py` — añadir filtros

Sustituye el fichero completo:

```python
import flet as ft
from database import get_filtradas, delete
from models import TipoTransaccion, Categoria

MESES = {
    0: "Todos",
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
    5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
    9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}


def crear_lista(pag: ft.Page, on_eliminado) -> tuple[ft.Column, callable]:
    """Devuelve la lista de transacciones con filtros y resumen."""

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

    filtro_mes = ft.Dropdown(
        label="Mes",
        value="0",
        options=[ft.dropdown.Option(key=str(k), text=v) for k, v in MESES.items()],
        width=160,
    )

    filtro_categoria = ft.Dropdown(
        label="Categoría",
        value="todas",
        options=[ft.dropdown.Option(key="todas", text="Todas")]
        + [ft.dropdown.Option(key=c.value, text=c.value) for c in Categoria],
        width=200,
    )

    def cargar():
        mes = int(filtro_mes.value) if filtro_mes.value != "0" else None
        cat = filtro_categoria.value if filtro_categoria.value != "todas" else None

        trans = get_filtradas(mes=mes, categoria=cat)

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

    def al_cambiar_filtro(e):
        cargar()
        pag.update()

    filtro_mes.on_change = al_cambiar_filtro
    filtro_categoria.on_change = al_cambiar_filtro

    cargar()

    columna = ft.Column(
        controls=[
            ft.Text("Transacciones", size=22, weight=ft.FontWeight.BOLD),
            ft.Row([filtro_mes, filtro_categoria], spacing=12),
            ft.Divider(),
            ft.Row([resumen]),
            ft.Column(controls=[tabla], scroll=ft.ScrollMode.AUTO),
        ],
        expand=True,
        spacing=12,
    )
    return columna, cargar
```

### Comprueba que funciona

- [ ] Aparecen los dos Dropdowns encima de la tabla
- [ ] Cambiar el mes filtra las filas correctamente
- [ ] Cambiar la categoría filtra las filas correctamente
- [ ] El resumen (ingresos/gastos/saldo) se recalcula con los datos filtrados
- [ ] "Todos" / "Todas" muestra todas las transacciones

Cuando lo tengas, avisa y pasamos al **Paso 7 — Gráfico de barras**.

---

## Paso 7 — Gráfico de barras

### Estructura de la pantalla

En este paso añadimos una segunda pestaña con el gráfico. Usaremos `ft.Tabs` para alternar entre la vista de lista y la vista de gráfico.

```
[ Lista de transacciones ]  [ Gráfico ]
─────────────────────────────────────────
  Gráfico de gastos por categoría
```

### Cambio en `database.py` — añadir `get_gastos_por_categoria()`

Añade al final de `database.py`:

```python
def get_gastos_por_categoria() -> dict[str, float]:
    """Devuelve el total de gastos agrupado por categoría."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT categoria, SUM(importe)
                FROM transacciones
                WHERE tipo = 'Gasto'
                GROUP BY categoria
                ORDER BY SUM(importe) DESC
            """)
            filas = cur.fetchall()
    return {fila[0]: float(fila[1]) for fila in filas}
```

### Cómo funciona `ft.BarChart`

```python
ft.BarChart(
    bar_groups=[
        ft.BarChartGroup(
            x=0,                          # posición en eje X
            bar_rods=[
                ft.BarChartRod(
                    from_y=0,             # base de la barra
                    to_y=45.50,           # altura = valor
                    width=30,
                    color=ft.Colors.BLUE,
                )
            ],
        ),
    ],
    bottom_axis=ft.ChartAxis(
        labels=[
            ft.ChartAxisLabel(value=0, label=ft.Text("Alimentación")),
        ],
        labels_size=40,
    ),
    max_y=100,
    expand=True,
)
```

### Tu tarea — crear `views/chart_view.py`

```python
import flet as ft
from database import get_gastos_por_categoria

COLORES = [
    ft.Colors.BLUE_400,
    ft.Colors.RED_400,
    ft.Colors.GREEN_400,
    ft.Colors.ORANGE_400,
    ft.Colors.PURPLE_400,
    ft.Colors.TEAL_400,
    ft.Colors.PINK_400,
]


def crear_grafico(pag: ft.Page) -> ft.Column:
    """Devuelve el gráfico de gastos por categoría como un Column."""

    chart_container = ft.Container(expand=True)

    def cargar():
        datos = get_gastos_por_categoria()

        if not datos:
            chart_container.content = ft.Text(
                "Sin datos de gastos para mostrar.", size=16
            )
            return

        categorias = list(datos.keys())
        valores = list(datos.values())
        max_val = max(valores) * 1.2

        grupos = [
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=v,
                        width=35,
                        color=COLORES[i % len(COLORES)],
                        tooltip=f"{cat}: {v:.2f} €",
                        border_radius=4,
                    )
                ],
            )
            for i, (cat, v) in enumerate(zip(categorias, valores))
        ]

        etiquetas = [
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(
                    ft.Text(cat, size=11, text_align=ft.TextAlign.CENTER),
                    width=70,
                ),
            )
            for i, cat in enumerate(categorias)
        ]

        chart_container.content = ft.BarChart(
            bar_groups=grupos,
            bottom_axis=ft.ChartAxis(labels=etiquetas, labels_size=50),
            left_axis=ft.ChartAxis(labels_size=40),
            max_y=max_val,
            expand=True,
            height=350,
            interactive=True,
        )

    cargar()

    return ft.Column(
        controls=[
            ft.Text("Gastos por categoría", size=22, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            chart_container,
        ],
        expand=True,
        spacing=16,
    )
```

### Actualizar `main.py` con `ft.Tabs`

```python
import flet as ft
from database import init_db
from views.form_view import crear_form
from views.list_view import crear_lista
from views.chart_view import crear_grafico


def main(pag: ft.Page) -> None:
    pag.title = "Gestor de Gastos"
    pag.window.width = 1000
    pag.window.height = 700
    pag.theme_mode = ft.ThemeMode.LIGHT

    init_db()

    def refrescar(e=None):
        recargar()
        pag.update()

    formulario = crear_form(pag, refrescar)
    lista, recargar = crear_lista(pag, refrescar)
    grafico = crear_grafico(pag)

    pag.add(
        ft.Tabs(
            selected_index=0,
            expand=True,
            tabs=[
                ft.Tab(
                    text="Transacciones",
                    content=ft.Row(
                        controls=[
                            ft.Container(content=formulario, width=350, padding=20),
                            ft.VerticalDivider(),
                            ft.Container(content=lista, expand=True, padding=20),
                        ],
                        expand=True,
                    ),
                ),
                ft.Tab(
                    text="Gráfico",
                    content=ft.Container(content=grafico, expand=True, padding=20),
                ),
            ],
        )
    )


ft.run(main)
```

### Comprueba que funciona

- [ ] Aparecen dos pestañas: "Transacciones" y "Gráfico"
- [ ] La pestaña Gráfico muestra barras por categoría
- [ ] Al pasar el ratón sobre una barra aparece el tooltip con el valor
- [ ] Si no hay gastos aparece el mensaje "Sin datos"

Cuando lo tengas, avisa y pasamos al **Paso 8 — Pulir estilo**.

---

## Notas para la entrega

- Código comentado en **español** siguiendo PEP 8
- `README.md` con instrucciones de instalación y uso
- Commits semánticos: `feat(models): añadir dataclass Transaccion`
- **No hace falta** login, cifrado, ni tests automatizados para el CE
- `.env` en `.gitignore` — nunca subir credenciales al repo
