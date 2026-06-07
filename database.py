import os
import psycopg2
from dotenv import load_dotenv
from models import Transaccion, TipoTransaccion, Categoria

load_dotenv()


def _connect():
    """Conecta a la base de datos usando la URL de conexión almacenada en las variables de entorno."""
    return psycopg2.connect(os.getenv("DATABASE_URL"))


def init_db() -> None:
    """Crea la tabla de transacciones si no existe."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS transacciones (
                    id          SERIAL PRIMARY KEY,
                    tipo        VARCHAR(10)  NOT NULL,
                    importe     NUMERIC(10,2) NOT NULL,
                    categoria   VARCHAR(50)  NOT NULL,
                    descripcion TEXT,
                    fecha       DATE         NOT NULL
                );
            """)


def insert(tran: Transaccion) -> int:
    """Inserta una nueva transacción en la base de datos y devuelve su ID."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO transacciones (tipo, importe, categoria, descripcion, fecha)
                VALUES (%s, %s, %s, %s, %s) 
                RETURNING id;
                """,
                (
                    tran.tipo.value,
                    tran.importe,
                    tran.categoria.value,
                    tran.descripcion,
                    tran.fecha,
                ),
            )
            return cur.fetchone()[0]


def get_all() -> list[Transaccion]:
    """Recupera todas las transacciones de la base de datos."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, tipo, importe, categoria, descripcion, fecha FROM transacciones ORDER BY fecha DESC;"
            )
            rows = cur.fetchall()
            return [
                Transaccion(
                    id=row[0],
                    tipo=TipoTransaccion(row[1]),
                    importe=float(row[2]),
                    categoria=Categoria(row[3]),
                    descripcion=row[4],
                    fecha=row[5],
                )
                for row in rows
            ]
            
def get_filtered(mes: int | None = None, categoria: str | None = None) -> list[Transaccion]:
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

    with _connect() as conn:
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


def delete(tran_id: int) -> None:
    """Elimina una transacción de la base de datos por su ID."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM transacciones WHERE id = %s;", (tran_id,))
            conn.commit()
            
            
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


def get_ingresos_por_categoria() -> dict[str, float]:
    """Devuelve el total de ingresos agrupado por categoría."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT categoria, SUM(importe)
                FROM transacciones
                WHERE tipo = 'Ingreso'
                GROUP BY categoria
                ORDER BY SUM(importe) DESC
            """)
            filas = cur.fetchall()
    return {fila[0]: float(fila[1]) for fila in filas}
