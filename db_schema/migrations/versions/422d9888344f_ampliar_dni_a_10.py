"""ampliar dni a 10

Revision ID: 422d9888344f
Revises: c768dd2f8ba2
Create Date: 2025-12-03 09:43:14.966886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '422d9888344f'
down_revision: Union[str, None] = 'c768dd2f8ba2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "USUARIO",
        "dni",
        existing_type=sa.VARCHAR(length=8, collation="Modern_Spanish_CI_AS"),
        type_=sa.String(length=10),
        existing_nullable=True,
    )



def downgrade() -> None:
    op.alter_column(
        "USUARIO",
        "dni",
        existing_type=sa.String(length=10),
        type_=sa.VARCHAR(length=8, collation="Modern_Spanish_CI_AS"),
        existing_nullable=True,
    )
