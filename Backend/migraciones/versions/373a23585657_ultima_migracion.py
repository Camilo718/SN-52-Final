"""ultima_migracion

Revision ID: 373a23585657
Revises: 858d9f51e9ed
Create Date: 2025-12-13 11:02:34.992226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '373a23585657'
down_revision: Union[str, None] = '858d9f51e9ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
