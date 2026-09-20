from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, func
from core.db.session import Base

class Booking(Base):
    __tablename__='booking'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'))
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id', ondelete='CASCADE'))
    booking_start_at: Mapped[datetime] 
    booking_end_at: Mapped[datetime] 
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())