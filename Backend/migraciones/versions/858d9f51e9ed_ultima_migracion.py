"""ultima_migracion

Revision ID: 858d9f51e9ed
Revises: 2983ff2881d4
Create Date: 2025-12-13 11:00:55.645243

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '858d9f51e9ed'
down_revision: Union[str, None] = '2983ff2881d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
