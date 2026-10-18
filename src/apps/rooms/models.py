from datetime import datetime
from decimal import Decimal
from typing import TYPE_CHECKING, Optional
from sqlalchemy import String, CheckConstraint, Numeric, Text, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db.session import Base

if TYPE_CHECKING:
    from apps.bookings.models import Booking


class Room(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), unique=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    capacity: Mapped[int] = mapped_column(nullable=False)
    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    bookings: Mapped[list['Booking']] = relationship(back_populates='room')

    __table_args__ = (
        CheckConstraint('capacity > 0', name='ck_rooms_capacity_positive'),
        CheckConstraint('price_per_night >= 0', name='ck_rooms_price_non_negative'),
    )
