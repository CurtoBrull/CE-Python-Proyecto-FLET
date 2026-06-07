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


def delete(tran_id: int) -> None:
    """Elimina una transacción de la base de datos por su ID."""
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM transacciones WHERE id = %s;", (tran_id,))
            conn.commit()
