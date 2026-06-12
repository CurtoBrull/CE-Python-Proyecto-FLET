# Gestor de Gastos Personales

Aplicación de escritorio para registrar y visualizar gastos e ingresos personales, desarrollada como proyecto final del **Ciclo de Especialización en Desarrollo de Aplicaciones en Lenguaje Python** (BOE-A-2024-12503).

## Demo

**[https://ce-python-proyecto-flet.onrender.com/](https://ce-python-proyecto-flet.onrender.com/)**

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| [Python 3.11+](https://www.python.org/) | Lenguaje principal |
| [Flet](https://flet.dev/) | Framework de UI (Flutter para Python) |
| [Neon](https://neon.tech/) | Base de datos PostgreSQL serverless |
| [psycopg2](https://pypi.org/project/psycopg2-binary/) | Driver PostgreSQL |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gestión de variables de entorno |
| [Render](https://render.com/) | Despliegue web gratuito |

> Flet en GitHub: [https://github.com/flet-dev/flet](https://github.com/flet-dev/flet)

## Funcionalidades

- Añadir, **editar** y eliminar transacciones (gastos e ingresos)
- Listar transacciones con scroll y **ordenación por cualquier columna**
- Filtrar por mes y categoría, con botón limpiar filtros
- Resumen de ingresos, gastos y saldo en tiempo real
- **Exportar CSV** (diálogo nativo en escritorio, copia manual en web)
- Gráfico de barras de gastos e ingresos por categoría
- **Pantalla de inicio** con presentación y logo
- **Documentación Flet integrada** — 9 secciones con ejemplos de código real
- Navegación lateral (NavigationRail) con transiciones fade entre vistas
- Modo oscuro / claro con colores adaptativos

## Requisitos previos

- Python 3.11 o superior
- Cuenta gratuita en [Neon](https://neon.tech/) con un proyecto creado

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/CurtoBrull/CE-Python-Proyecto-FLET.git
cd CE-Python-Proyecto-FLET
```

### 2. Crear y activar el entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Crea un fichero `.env` en la raíz del proyecto con la connection string de tu proyecto Neon:

```env
DATABASE_URL=postgresql://user:password@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require
```

> La connection string se obtiene en **Neon Console → proyecto → Connection Details**.

La tabla de la base de datos se crea automáticamente al arrancar la app.

## Ejecución

```powershell
python main.py
```

## Preview en Android

Con el móvil y el PC en la misma red WiFi e instalada la app **Flet** desde Google Play:

```powershell
flet run --android main.py
```

Escanea el QR que aparece en la terminal con la app Flet del móvil.

## Estructura del proyecto

```text
├── main.py                  # Punto de entrada, navegación y temas
├── database.py              # Capa de acceso a PostgreSQL (Neon)
├── models.py                # Modelos de datos (dataclasses y enums)
├── views/
│   ├── splash_view.py       # Pantalla de inicio/presentación
│   ├── form_view.py         # Formulario crear/editar transacción
│   ├── list_view.py         # Tabla con filtros, ordenación y exportar CSV
│   ├── chart_view.py        # Gráfico de gastos e ingresos
│   └── flet_info_view.py    # Documentación Flet con 9 subsecciones
├── utils/
│   └── constants.py         # Constantes compartidas (colores, meses)
├── assets/
│   └── favicon.png          # Icono de pestaña web y logo de la app
├── render.yaml              # Configuración de despliegue en Render
├── .env.example             # Plantilla de variables de entorno
└── requirements.txt         # Dependencias del proyecto
```

## Despliegue en Render

La app incluye `render.yaml` con la configuración lista. Pasos para desplegar tu propia instancia:

### 1. Crear cuenta y nuevo servicio

1. Entra en [render.com](https://render.com) y crea una cuenta gratuita
2. **New → Web Service → Connect a repository** y selecciona este repo
3. Render detecta `render.yaml` automáticamente

### 2. Configurar variables de entorno

En el panel de Render, añade las siguientes variables en **Environment**:

| Variable | Valor |
|---|---|
| `DATABASE_URL` | Connection string de tu proyecto Neon |
| `FLET_FORCE_WEB_SERVER` | `true` |

> `PORT` lo asigna Render automáticamente — no hace falta configurarlo.

### 3. Desplegar

Pulsa **Deploy**. Render instala dependencias (`pip install -r requirements.txt`) y arranca con `python main.py`.

La URL pública aparece en el dashboard con formato `https://nombre-servicio.onrender.com`.

> **Nota:** el plan gratuito de Render apaga el servicio tras 15 minutos de inactividad. El primer acceso puede tardar ~30 segundos en arrancar.

---

## Autor

**Javier Curto Brull**
Ciclo de Especialización — Desarrollo de Aplicaciones en Lenguaje Python
