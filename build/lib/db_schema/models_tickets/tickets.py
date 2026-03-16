from __future__ import annotations
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import pytz
import enum
from sqlalchemy import Enum as SAEnum
from sqlalchemy import text

from sqlalchemy import Integer, String, DateTime, Text, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db_schema.db import Base

# solo para type hints (evita ciclos en tiempo de ejecución)
#if TYPE_CHECKING:
    #from db_schema.models_generales.usuario import Usuario

_peru_tz = pytz.timezone("America/Lima")
def now_lima() -> datetime:
    return datetime.now(_peru_tz)

class EstadoTicket(enum.Enum):
    PENDIENTE = "Pendiente"
    APROBADO  = "Aprobado"
    ATENDIDO  = "Atendido"
    CERRADO   = "Cerrado"
    # opcional: RECHAZADO = "Rechazado"

class ReqEquipoRed(Base):
    __tablename__ = "REQ_EQUIPOS_RED"
    id_req_er: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # código visible (generado en SQL Server vía server_default con SEQUENCE)
    codigo: Mapped[str] = mapped_column(String(25),nullable=False,unique=True,server_default=text(
        "((('TCK-'+format(getdate(),'yyyyMM'))+'-')+right('0000'+CONVERT([varchar](10),NEXT VALUE FOR [dbo].[seq_req_er]),(4)))"
        ))
    usuario: Mapped[str] = mapped_column(Text, nullable=False)
    fecha_registro: Mapped[datetime] = mapped_column(DateTime(), default=now_lima)
    nombre_equipo: Mapped[str] = mapped_column(String(20), nullable=False)
    prioridad: Mapped[str] = mapped_column(String(20), nullable=False)
    descripcion: Mapped[str] = mapped_column(Text, nullable=False)
    informe_tecnico: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    fecha_atencion: Mapped[Optional[datetime]] = mapped_column(DateTime(), nullable=True)
    estado: Mapped[EstadoTicket] = mapped_column(
        SAEnum(EstadoTicket,native_enum=False,  # SQL Server no tiene ENUM
            create_constraint=True,  # crea CHECK (estado in (...))
            validate_strings=True,
            name="ck_estado_ticket"  # nombre estable del constraint
        ),
        nullable=False,
        default=EstadoTicket.PENDIENTE
    )
    # --- relacionar con tabla USUARIO (opcional) ---
    usuario_aprueba_id: Mapped[Optional[int]] = mapped_column(ForeignKey("USUARIO.id_usuario"), nullable=True)
    usuario_solicita_id: Mapped[Optional[int]] = mapped_column(ForeignKey("USUARIO.id_usuario"), nullable=True)
    usuario_aprueba: Mapped[Optional["Usuario"]] = relationship(foreign_keys=[usuario_aprueba_id])
    usuario_solicita: Mapped[Optional["Usuario"]] = relationship(foreign_keys=[usuario_solicita_id])
    __table_args__ = (
        Index("ix_req_er_fecha", "fecha_registro"),
        Index("ix_req_er_estado", "estado"),
    )




