from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Index
from db_schema.db import Base  # importa Base desde .db
from flask_login import UserMixin

class Usuario(Base,UserMixin):
    __tablename__ = "USUARIO"   # ← si fue typo, usa "USUARIO"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(100), nullable=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    dni: Mapped[str] = mapped_column(String(10), nullable=True)     # Perú: 8 dígitos (ajusta si necesitas)
    area: Mapped[str] = mapped_column(String(50), nullable=True)
    area2: Mapped[str] = mapped_column(String(50), nullable=True)
    cargo: Mapped[str] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        Index("uq_usuario_dni", "dni", unique=True),   # quítalo si no debe ser único
        Index("ix_usuario_nombre", "username"),
    )

    # IMPORTANTE: tu PK no se llama "id", así que define get_id()
    def get_id(self) -> str:
        return str(self.id_usuario)
