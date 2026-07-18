from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


from app.db.database import Base
from app.db.timestamp import TimestampMixin

class SystemRoles(Base,TimestampMixin):
    __tablename__ = "system_roles"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
                      )
    role_name : Mapped[str] = mapped_column(
      String(255),
      unique=True,
      nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    system_role_permissions = relationship("SystemRolePermissions", back_populates="system_roles")

