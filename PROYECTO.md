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
    └─► ft.app(target=main)
            └─► crea ft.Page  (la ventana)
                    └─► llama a tu función main(page)
                            └─► tú añades controles a page
```

### Conceptos clave

| Concepto | Qué es |
|---|---|
| `ft.app(target=main)` | Arranca la app. `target` es la función que recibe la página |
| `ft.Page` | La ventana. Tiene propiedades: `title`, `width`, `height`, `theme_mode`, etc. |
| `page.add(control)` | Añade un control (widget) a la ventana y lo renderiza |
| `page.update()` | Refresca la UI después de cambiar algo (necesario cuando modificas controles existentes) |
| Control | Cualquier elemento visual: texto, botón, campo de texto, columna... |

### Controles básicos que usarás

```python
ft.Text("Hola")                    # Texto estático
ft.ElevatedButton("Click")         # Botón con relieve
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

ft.ElevatedButton("Click", on_click=al_pulsar)
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
                ft.ElevatedButton("Pulsa aquí", on_click=al_pulsar),
                contador,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
        )
    )


ft.app(target=main)
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

## Notas para la entrega

- Código comentado en **español** siguiendo PEP 8
- `README.md` con instrucciones de instalación y uso
- Commits semánticos: `feat(models): añadir dataclass Transaccion`
- **No hace falta** login, cifrado, ni tests automatizados para el CE
- `.env` en `.gitignore` — nunca subir credenciales al repo
