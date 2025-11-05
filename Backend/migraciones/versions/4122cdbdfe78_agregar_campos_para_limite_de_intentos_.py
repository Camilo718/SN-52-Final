"""Agregar campos para limite de intentos de login

Revision ID: 4122cdbdfe78
Revises: 710045434184
Create Date: 2025-11-05 14:13:23.573770

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4122cdbdfe78'
down_revision: Union[str, None] = '710045434184'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Agregar columnas para límite de intentos de login
    op.add_column('usuarios', sa.Column('intentos_fallidos', sa.Integer(), nullable=False, default=0))
    op.add_column('usuarios', sa.Column('bloqueado_hasta', sa.DateTime(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Eliminar columnas
    op.drop_column('usuarios', 'bloqueado_hasta')
    op.drop_column('usuarios', 'intentos_fallidos')
