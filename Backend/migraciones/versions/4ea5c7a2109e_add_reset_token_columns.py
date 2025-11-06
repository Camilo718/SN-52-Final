"""add reset token columns

Revision ID: 4ea5c7a2109e
Revises: 4122cdbdfe78
Create Date: 2025-11-05 17:54:09.984234
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

revision: str = '4ea5c7a2109e'
down_revision: Union[str, None] = '4122cdbdfe78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("usuarios")]

    # Solo agregar si no existen
    if "reset_token" not in columns:
        op.add_column("usuarios", sa.Column("reset_token", sa.String(255), nullable=True))

    if "reset_token_expira" not in columns:
        op.add_column("usuarios", sa.Column("reset_token_expira", sa.DateTime(), nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("usuarios")]

    if "reset_token" in columns:
        op.drop_column("usuarios", "reset_token")

    if "reset_token_expira" in columns:
        op.drop_column("usuarios", "reset_token_expira")
