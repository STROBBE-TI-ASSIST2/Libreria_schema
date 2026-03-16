# db_schema/migrations/env.py
from __future__ import annotations
import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import create_engine, pool
from db_schema.db import Base  # fallback si no hay Flask

config = context.config

# Solo intenta leer logging si existe un alembic.ini real
if config.config_file_name and os.path.exists(config.config_file_name):
    fileConfig(config.config_file_name)

# 🔹 Tablas que NO quieres que formen parte de las migraciones
IGNORED_TABLES = {
    "PICKING_DETALLE",   # ejemplo: tabla externa
    # "OTRA_TABLA",      # agrega aquí las que quieras ignorar
}

def get_url_and_metadata():
    try:
        # Cuando corre via Flask-Migrate
        from flask import current_app
        url = current_app.config.get("SQLALCHEMY_DATABASE_URI")
        metadata = current_app.extensions["migrate"].db.metadata
        return url, metadata
    except Exception:
        # Fallback para correr Alembic sin Flask
        # 👇 Importa modelos para que Base.metadata tenga TODO
        try:
            from db_schema import models  # noqa: F401
        except Exception:
            # si falla el import, igual Base.metadata tendrá lo que se haya importado antes
            pass

        url = os.getenv("ALEMBIC_DB_URL") or os.getenv("DATABASE_URL")
        metadata = Base.metadata
        return url, metadata

# 🔹 Filtro para excluir tablas del autogenerate
def include_object(object, name, type_, reflected, compare_to):
    # Si es una tabla y está en la lista de ignoradas → Alembic la ignora
    if type_ == "table" and name in IGNORED_TABLES:
        return False
    return True

def run_migrations_offline():
    url, target_metadata = get_url_and_metadata()
    if not url:
        raise RuntimeError("No DB URL. Define SQLALCHEMY_DATABASE_URI (Flask) o ALEMBIC_DB_URL/DATABASE_URL.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        include_object=include_object,  # 👈 importante
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    url, target_metadata = get_url_and_metadata()
    if not url:
        raise RuntimeError("No DB URL. Define SQLALCHEMY_DATABASE_URI (Flask) o ALEMBIC_DB_URL/DATABASE_URL.")
    connectable = create_engine(url, poolclass=pool.NullPool, future=True)
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
            include_object=include_object,  # 👈 importante
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
