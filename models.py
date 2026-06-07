from dataclasses import dataclass, field
from datetime import date
import enum


class TipoTransaccion(enum.Enum):
    INGRESO = "Ingreso"
    GASTO = "Gasto"


class Categoria(enum.Enum):
    ALIMENTACION = "Alimentación"
    TRANSPORTE = "Transporte"
    VIVIENDA = "Vivienda"
    OCIO = "Ocio"
    SALUD = "Salud"
    EDUCACION = "Educación"
    NOMINA = "Nómina"
    OTROS = "Otros"


@dataclass
class Transaccion:
    tipo: TipoTransaccion
    importe: float
    categoria: Categoria
    descripcion: str
    fecha: date = field(default_factory=date.today)
    id: int | None = None  # None hasta que la BD asigne el id real
