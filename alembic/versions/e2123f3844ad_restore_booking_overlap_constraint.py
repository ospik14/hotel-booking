"""restore_booking_overlap_constraint

Revision ID: e2123f3844ad
Revises: d754a050da3c
Create Date: 2026-10-12 21:28:24.109031

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2123f3844ad'
down_revision: Union[str, Sequence[str], None] = 'd754a050da3c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("""
    ALTER TABLE bookings
    ADD CONSTRAINT no_overlapping_booking
    EXCLUDE USING gist (
        room_id WITH =,
        daterange(check_in_date, check_out_date) WITH &&
    );
""")
    """Upgrade schema."""
    pass


def downgrade() -> None:
    op.execute("ALTER TABLE bookings DROP CONSTRAINT IF EXISTS no_overlapping_booking;")
    """Downgrade schema."""
    pass
