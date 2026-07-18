from sqlalchemy import UUID,ForeignKey
import uuid
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class UserRole(Base, TimestampMixin):
    __tablename__ = "user_role"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
    )
    user_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
    )
    system_roles_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("system_roles.id", ondelete="CASCADE"),
    )


    user = relationship("User",
                        back_populates="user_role",
                        )

