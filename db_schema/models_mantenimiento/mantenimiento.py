from __future__ import annotations
from datetime import datetime
import pytz
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from db_schema.db import Base

_peru_tz = pytz.timezone("America/Lima")
def now_lima() -> datetime:
    return datetime.now(_peru_tz)

class Mantenimiento(Base):
    __tablename__ = "Mantenimientos_pc"

    id_pc: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo_stb: Mapped[str] = mapped_column(String(15), nullable=False)
    nombre_equipo: Mapped[str] = mapped_column(String(30), nullable=False)
    ip: Mapped[str] = mapped_column(String(20), nullable=False)
    sistema_operativo: Mapped[str] = mapped_column(String(50), nullable=False)
    procesador: Mapped[str] = mapped_column(String(20), nullable=False)
    ram: Mapped[int] = mapped_column(Integer, nullable=False)
    office: Mapped[str] = mapped_column(String(50), nullable=False)
    reporte: Mapped[str] = mapped_column(String(500), nullable=False)
    accion_correctiva: Mapped[str] = mapped_column(String(500), nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime(),               # usa DateTime(timezone=True) solo si tu columna es datetimeoffset
        default=now_lima
    )




