"""add usuario not null a REQ_EQUIPOS_RED

Revision ID: c768dd2f8ba2
Revises: 1d013660bf76
Create Date: 2025-10-20 11:57:50.512893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c768dd2f8ba2'
down_revision: Union[str, None] = '1d013660bf76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



_USR_TYPE = sa.String(50)  # o sa.Text() si prefieres

def upgrade():
    # 1) Agregar columna como NULL temporalmente
    op.add_column(
        "REQ_EQUIPOS_RED",
        sa.Column("usuario", _USR_TYPE, nullable=True)
    )

    # 2) Backfill explícito (históricos). Cambia 'pendiente' si deseas otro literal.
    op.execute("""
        UPDATE r
           SET r.usuario = 'pendiente'
        FROM REQ_EQUIPOS_RED r
        WHERE r.usuario IS NULL
    """)

    # (Opcional) Si quieres rellenar desde USUARIO.username:
    # op.execute("""
    #     UPDATE r
    #        SET r.usuario = COALESCE(u.username, 'pendiente')
    #     FROM REQ_EQUIPOS_RED r
    #     LEFT JOIN USUARIO u ON u.id_usuario = r.usuario_solicita_id
    #     WHERE r.usuario IS NULL
    # """)

    # 3) Volverla NOT NULL
    op.alter_column(
        "REQ_EQUIPOS_RED", "usuario",
        existing_type=_USR_TYPE,
        nullable=False
    )

    # 4) (Opcional pero útil) Evitar cadenas vacías/espacios solamente
    # op.create_check_constraint(
    #     "ck_req_er_usuario_not_blank",
    #     "REQ_EQUIPOS_RED",
    #     "LEN(LTRIM(RTRIM(usuario))) > 0"
    # )

def downgrade():
    # Si creaste el CHECK arriba, elimínalo primero:
    # op.drop_constraint("ck_req_er_usuario_not_blank", "REQ_EQUIPOS_RED", type_="check")

    op.alter_column("REQ_EQUIPOS_RED", "usuario", existing_type=_USR_TYPE, nullable=True)
    op.drop_column("REQ_EQUIPOS_RED", "usuario")