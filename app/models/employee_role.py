from sqlalchemy import UUID, ForeignKey
import uuid
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class EmployeeRoles(Base, TimestampMixin):
    __tablename__ = "employee_role"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        unique=True,
        primary_key=True,
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
    )
    organisation_roles_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation_roles.id")
    )

    employee = relationship("Employee",
                        back_populates="employee_roles", )
    role = relationship("OrganisationRoles",
                                back_populates="employee_roles", )
