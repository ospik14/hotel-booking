"""complete booking system schema

Revision ID: b1c2d3e4f5a6
Revises: 18aaa2858b44
Create Date: 2026-10-18 18:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = 'b1c2d3e4f5a6'
down_revision: Union[str, Sequence[str], None] = '18aaa2858b44'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

role_enum = postgresql.ENUM('admin', 'user', name='role', create_type=False)
booking_status_enum = postgresql.ENUM(
    'CONFIRMED',
    'CANCELLED',
    'COMPLETED',
    name='bookingstatus',
    create_type=False,
)


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS btree_gist;')

    role_enum.create(op.get_bind(), checkfirst=True)
    booking_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        'users',
        sa.Column(
            'role',
            role_enum,
            server_default='user',
            nullable=False,
        ),
    )
    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            server_default=sa.text('true'),
            nullable=False,
        ),
    )

    op.add_column('rooms', sa.Column('description', sa.Text(), nullable=True))
    op.add_column(
        'rooms',
        sa.Column(
            'price_per_night',
            sa.Numeric(10, 2),
            server_default='0',
            nullable=False,
        ),
    )
    op.add_column(
        'rooms',
        sa.Column(
            'is_active',
            sa.Boolean(),
            server_default=sa.text('true'),
            nullable=False,
        ),
    )
    op.add_column(
        'rooms',
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )
    op.add_column(
        'rooms',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )
    op.create_check_constraint(
        'ck_rooms_capacity_positive',
        'rooms',
        'capacity > 0',
    )
    op.create_check_constraint(
        'ck_rooms_price_non_negative',
        'rooms',
        'price_per_night >= 0',
    )

    op.add_column(
        'bookings',
        sa.Column('guests', sa.Integer(), server_default='1', nullable=False),
    )
    op.add_column(
        'bookings',
        sa.Column(
            'status',
            booking_status_enum,
            server_default='CONFIRMED',
            nullable=False,
        ),
    )
    op.add_column(
        'bookings',
        sa.Column(
            'price_per_night',
            sa.Numeric(10, 2),
            server_default='0',
            nullable=False,
        ),
    )
    op.add_column(
        'bookings',
        sa.Column(
            'total_price',
            sa.Numeric(10, 2),
            server_default='0',
            nullable=False,
        ),
    )
    op.add_column(
        'bookings',
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.text('now()'),
            nullable=False,
        ),
    )

    op.execute('ALTER TABLE bookings DROP CONSTRAINT IF EXISTS no_overlapping_booking;')
    op.execute("""
        ALTER TABLE bookings
        ADD CONSTRAINT no_overlapping_booking
        EXCLUDE USING gist (
            room_id WITH =,
            daterange(check_in_date, check_out_date, '[)') WITH &&
        )
        WHERE (status = 'CONFIRMED');
    """)

    op.create_check_constraint(
        'ck_bookings_guests_positive',
        'bookings',
        'guests > 0',
    )
    op.create_check_constraint(
        'ck_bookings_dates_valid',
        'bookings',
        'check_out_date > check_in_date',
    )
    op.create_check_constraint(
        'ck_bookings_total_price_non_negative',
        'bookings',
        'total_price >= 0',
    )
    op.create_check_constraint(
        'ck_bookings_price_per_night_non_negative',
        'bookings',
        'price_per_night >= 0',
    )

    op.drop_constraint('bookings_room_id_fkey', 'bookings', type_='foreignkey')
    op.drop_constraint('bookings_user_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_room_id_fkey',
        'bookings',
        'rooms',
        ['room_id'],
        ['id'],
        ondelete='RESTRICT',
    )
    op.create_foreign_key(
        'bookings_user_id_fkey',
        'bookings',
        'users',
        ['user_id'],
        ['id'],
        ondelete='RESTRICT',
    )

    op.create_index('ix_bookings_user_id', 'bookings', ['user_id'])
    op.create_index('ix_bookings_room_id', 'bookings', ['room_id'])
    op.create_index('ix_bookings_status', 'bookings', ['status'])
    op.create_index(
        'ix_bookings_check_in_date',
        'bookings',
        ['check_in_date'],
    )


def downgrade() -> None:
    op.drop_index('ix_bookings_check_in_date', table_name='bookings')
    op.drop_index('ix_bookings_status', table_name='bookings')
    op.drop_index('ix_bookings_room_id', table_name='bookings')
    op.drop_index('ix_bookings_user_id', table_name='bookings')

    op.drop_constraint('bookings_room_id_fkey', 'bookings', type_='foreignkey')
    op.drop_constraint('bookings_user_id_fkey', 'bookings', type_='foreignkey')
    op.create_foreign_key(
        'bookings_room_id_fkey',
        'bookings',
        'rooms',
        ['room_id'],
        ['id'],
        ondelete='CASCADE',
    )
    op.create_foreign_key(
        'bookings_user_id_fkey',
        'bookings',
        'users',
        ['user_id'],
        ['id'],
        ondelete='CASCADE',
    )

    op.drop_constraint('ck_bookings_price_per_night_non_negative', 'bookings', type_='check')
    op.drop_constraint('ck_bookings_total_price_non_negative', 'bookings', type_='check')
    op.drop_constraint('ck_bookings_dates_valid', 'bookings', type_='check')
    op.drop_constraint('ck_bookings_guests_positive', 'bookings', type_='check')

    op.execute('ALTER TABLE bookings DROP CONSTRAINT IF EXISTS no_overlapping_booking;')
    op.execute("""
        ALTER TABLE bookings
        ADD CONSTRAINT no_overlapping_booking
        EXCLUDE USING gist (
            room_id WITH =,
            daterange(check_in_date, check_out_date) WITH &&
        );
    """)

    op.drop_column('bookings', 'updated_at')
    op.drop_column('bookings', 'total_price')
    op.drop_column('bookings', 'price_per_night')
    op.drop_column('bookings', 'status')
    op.drop_column('bookings', 'guests')

    op.drop_constraint('ck_rooms_price_non_negative', 'rooms', type_='check')
    op.drop_constraint('ck_rooms_capacity_positive', 'rooms', type_='check')
    op.drop_column('rooms', 'updated_at')
    op.drop_column('rooms', 'created_at')
    op.drop_column('rooms', 'is_active')
    op.drop_column('rooms', 'price_per_night')
    op.drop_column('rooms', 'description')

    op.drop_column('users', 'is_active')
    op.drop_column('users', 'role')

    booking_status_enum.drop(op.get_bind(), checkfirst=True)
    role_enum.drop(op.get_bind(), checkfirst=True)
