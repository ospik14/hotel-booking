from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func, DateTime,text
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from core.db.session import Base

class Booking(Base):
    __tablename__='bookings'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(
        ForeignKey('rooms.id', ondelete='CASCADE')
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now()
    )
    
    __table_args__ = (
        ExcludeConstraint(
            ('room_id', '='),
            (text('tstzrange(start_time, end_time)'), '&&'),
            
            name='no_overlapping_booking',
            using='gist'
        ),
    )