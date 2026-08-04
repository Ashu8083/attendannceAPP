import uuid

from sqlalchemy import ForeignKey, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class Token(Base, TimestampMixin):

    __tablename__ = "token"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id")
    )
    device_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("userdevice.id"),
        nullable=False
    )

    refresh_token: Mapped[str] = mapped_column(String)
    is_revoked: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    expires_at: Mapped[DateTime] = mapped_column(DateTime)
    device = relationship(
        "UserDeviceDetails",
        back_populates="refresh_tokens"
    )
    user = relationship(
        "User",
        back_populates="refresh_tokens"

    )