from datetime import datetime, date
from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func, DateTime, text, Date
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from core.db.session import Base

if TYPE_CHECKING:
    from rooms.models import Room

class Booking(Base):
    __tablename__='bookings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(
        ForeignKey('rooms.id', ondelete='CASCADE')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    check_in_date: Mapped[date] = mapped_column(Date(), nullable=False)
    check_out_date: Mapped[date] = mapped_column(Date(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    room: Mapped['Room'] = relationship(back_populates='bookings')
    
    __table_args__ = (
        ExcludeConstraint(
            ('room_id', '='),
            (text('daterange(check_in_date, check_out_date)'), '&&'),
            
            name='no_overlapping_booking',
            using='gist'
        ),
    )