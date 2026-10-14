"""add users roles

Revision ID: 18aaa2858b44
Revises: e2123f3844ad
Create Date: 2026-10-14 21:09:22.300976

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '18aaa2858b44'
down_revision: Union[str, Sequence[str], None] = 'e2123f3844ad'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
