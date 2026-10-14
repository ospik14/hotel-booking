import enum
from datetime import datetime
from sqlalchemy import func, DateTime, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from core.db.session import Base

class Role(enum.Enum):
    ADMIN = 'admin'
    USER = 'user'

class User(Base):
    __tablename__='users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=True))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )