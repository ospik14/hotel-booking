from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from core.db.session import Base

class Room(Base):
    __tablename__='rooms'
    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(255))
    capacity: Mapped[int]