from sqlalchemy import String,UniqueConstraint,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class OrganisationRoles(Base, TimestampMixin):
    __tablename__ = "organisation_roles"
    __table_args__ = (
        UniqueConstraint(
            "role_name",
            "organisation_id",
        ),
    )
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    role_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )
    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id"),
    )

    organisation = relationship("Organisation", back_populates="organisation_lvl_roles")
    role_permission = relationship("OrganisationRolePermissions", back_populates="role",
                                   cascade="all, delete-orphan")
    employee_roles = relationship("EmployeeRoles", back_populates="role")