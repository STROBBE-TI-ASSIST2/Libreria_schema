# Libreria_schema (db_schema)

Librería **Python** que centraliza y reutiliza **modelos SQLAlchemy** y **migraciones Alembic** para múltiples proyectos (por ejemplo aplicaciones Flask).

El objetivo es **evitar duplicación de modelos** entre repositorios y mantener un **esquema de base de datos consistente**.

---

# Características

- Base declarativa común (`Base`) para todos los modelos.
- Modelos organizados por módulos.
- Compatible con **SQLAlchemy 2.x**.
- Configuración lista para **Alembic migrations**.
- Puede ejecutarse:
  - dentro de una aplicación **Flask**
  - o **standalone** mediante variables de entorno.
- Permite **ignorar tablas externas** durante el autogenerate de Alembic.

---

# Requisitos

- Python **3.10+**
- SQLAlchemy **2.x**
- Alembic **1.13+**

Dependencias principales:
SQLAlchemy
alembic

Dependencias opcionales usadas por algunos modelos:
flask_login
pytz


---

# Instalación

### Instalación editable (recomendado para desarrollo)

```bash
pip install -e .
