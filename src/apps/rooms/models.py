from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, CheckConstraint
from core.db.session import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bookings.models import Booking

class Room(Base):
    __tablename__='rooms'
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255), unique=True)
    capacity: Mapped[int] = mapped_column(CheckConstraint('capacity > 0'))
    bookings: Mapped[list['Booking']] = relationship(back_populates='room')