import enum
from datetime import datetime, date
from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, DateTime, text, Date, Enum, Numeric, CheckConstraint
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from core.db.session import Base

if TYPE_CHECKING:
    from apps.rooms.models import Room
    from apps.users.models import User


class BookingStatus(enum.Enum):
    CONFIRMED = 'CONFIRMED'
    CANCELLED = 'CANCELLED'
    COMPLETED = 'COMPLETED'


class Booking(Base):
    __tablename__ = 'bookings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(
        ForeignKey('rooms.id', ondelete='RESTRICT')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='RESTRICT')
    )
    check_in_date: Mapped[date] = mapped_column(Date(), nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date(), nullable=False)
    guests: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(
            BookingStatus,
            name='bookingstatus',
            native_enum=True,
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        server_default=BookingStatus.CONFIRMED.value,
    )
    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    room: Mapped['Room'] = relationship(back_populates='bookings')
    user: Mapped['User'] = relationship(back_populates='bookings')

    __table_args__ = (
        CheckConstraint('guests > 0', name='ck_bookings_guests_positive'),
        CheckConstraint(
            'check_out_date > check_in_date',
            name='ck_bookings_dates_valid',
        ),
        CheckConstraint('total_price >= 0', name='ck_bookings_total_price_non_negative'),
        CheckConstraint(
            'price_per_night >= 0',
            name='ck_bookings_price_per_night_non_negative',
        ),
        ExcludeConstraint(
            ('room_id', '='),
            (text("daterange(check_in_date, check_out_date, '[)')"), '&&'),
            where=text("status = 'CONFIRMED'"),
            name='no_overlapping_booking',
            using='gist',
        ),
    )
