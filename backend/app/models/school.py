import datetime
from typing import TYPE_CHECKING

from app.models.base import Base
from app.models.user import User
from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.user import User  # noqa: F401


class School(Base):
    __tablename__ = "schools"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)

    phone_number: Mapped[str] = mapped_column(nullable=False, unique=True)

    users: Mapped[list["User"]] = relationship("User", back_populates="school")

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
