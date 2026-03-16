from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Index
from db_schema.db import Base  # importa Base desde .db
from flask_login import UserMixin

class Usuario_mantto(Base,UserMixin):
    __tablename__ = "USUARIO_MANTTO"   # ← si fue typo, usa "USUARIO"

    id_usuario: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    passwordd: Mapped[str] = mapped_column(String(100), nullable=False)

    # IMPORTANTE: tu PK no se llama "id", así que define get_id()
    def get_id(self) -> str:
        return str(self.id_usuario)