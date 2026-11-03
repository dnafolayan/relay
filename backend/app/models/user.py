import datetime
import enum

from app.models.base import Base
from sqlalchemy import DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column


class UserRole(enum.Enum):
    ADMIN: str = "admin"
    USER: str = "user"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="roleenum"), nullable=False
    )

    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)

    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, nullable=False, server_default=func.now()
    )
