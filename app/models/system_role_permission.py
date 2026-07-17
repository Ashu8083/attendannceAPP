import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class SystemRolePermissions(Base):
    __tablename__ = "system_role_permissions"

    system_roles: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("system_roles.id", ondelete="CASCADE"),
        primary_key=True,
    )

    permission_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )


    system_roles = relationship("SystemRoles", back_populates="system_role_permissions")
    permission = relationship("Permission", back_populates="system_role_permissions")