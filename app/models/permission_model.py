import uuid

from enum import Enum
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID,ENUM as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.enums.permission_scop import PermissionScopEnum,PermissionScopEnumUpdate
from app.db.database import Base


class Permission(Base):
    __tablename__ = "permissions"


    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    

    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )
    scope : Mapped[PermissionScopEnumUpdate] = mapped_column(
            SQLEnum(PermissionScopEnumUpdate),
            default= PermissionScopEnumUpdate .ORGANIZATION
        )

    assignable : Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    organisation_role_permissions = relationship(
        "OrganisationLevelRolePermissions",
        back_populates="permission",
    )
    system_role_permissions = relationship(
        "SystemRolePermissions",
        back_populates="permission",

    )