# Gestor de Gastos Personales

Aplicación de escritorio para registrar y visualizar gastos e ingresos personales, desarrollada como proyecto final del **Ciclo de Especialización en Desarrollo de Aplicaciones en Lenguaje Python** (BOE-A-2024-12503).

## Tecnologías

| Tecnología | Uso |
|---|---|
| [Python 3.11+](https://www.python.org/) | Lenguaje principal |
| [Flet](https://flet.dev/) | Framework de UI (Flutter para Python) |
| [Neon](https://neon.tech/) | Base de datos PostgreSQL serverless |
| [psycopg2](https://pypi.org/project/psycopg2-binary/) | Driver PostgreSQL |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Gestión de variables de entorno |

> Flet en GitHub: [https://github.com/flet-dev/flet](https://github.com/flet-dev/flet)

## Funcionalidades

- Añadir transacciones (gastos e ingresos) con categoría, importe, descripción y fecha
- Listar todas las transacciones con scroll
- Filtrar por mes y categoría
- Eliminar transacciones
- Resumen de ingresos, gastos y saldo en tiempo real
- Gráfico de barras de gastos e ingresos por categoría
- Navegación lateral (NavigationRail)
- Modo oscuro / claro

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

```
├── main.py              # Punto de entrada y configuración de la app
├── database.py          # Capa de acceso a PostgreSQL (Neon)
├── models.py            # Modelos de datos (dataclasses y enums)
├── views/
│   ├── form_view.py     # Formulario de nueva transacción
│   ├── list_view.py     # Lista de transacciones con filtros
│   └── chart_view.py    # Gráfico de gastos e ingresos
├── utils/
│   └── constants.py     # Constantes compartidas (colores, meses)
├── .env.example         # Plantilla de variables de entorno
└── requirements.txt     # Dependencias del proyecto
```

## Autor

**Javier Curto Brull**
Ciclo de Especialización — Desarrollo de Aplicaciones en Lenguaje Python
