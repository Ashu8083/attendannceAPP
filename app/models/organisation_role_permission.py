import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class OrganisationLevelRolePermissions(Base):
    __tablename__ = "organisation_role_permissions"

    organisation_role_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation_roles.id", ondelete="CASCADE"),
        primary_key=True,
    )

    permission_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )

    role = relationship(
        "OrganisationRole",
        back_populates="role_permission",
    )
    permission = relationship("Permission", back_populates="organisation_role_permissions")