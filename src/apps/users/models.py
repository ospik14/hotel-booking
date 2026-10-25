import enum
from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import func, DateTime, String, Enum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.db.session import Base

if TYPE_CHECKING:
    from apps.bookings.models import Booking


class Role(enum.Enum):
    SUPER_ADMIN = 'super_admin'
    HOTEL_ADMIN = 'hotel_admin'
    USER = 'user'


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(
        Enum(
            Role,
            name='role',
            native_enum=True,
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        nullable=False,
        server_default=Role.USER.value,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true')
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    bookings: Mapped[list['Booking']] = relationship(back_populates='user')
