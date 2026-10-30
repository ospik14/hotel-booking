from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, String, ForeignKey, func
from core.db.session import Base


class Hotel(Base):
    __tablename__='hotels'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(String(255))
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
            server_default=func.now(),
    )
    images: Mapped[list['HotelImage']] = relationship(back_populates='hotel')

class HotelImage(Base):
    __tablename__='hotel_images'

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255))
    is_main: Mapped[bool] = mapped_column(default=False)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    hotel: Mapped['Hotel'] = relationship(back_populates='images')