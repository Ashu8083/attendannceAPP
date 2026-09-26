from sqlalchemy.orm import Mapped, mapped_column, Relationship
import uuid
from sqlalchemy import Integer, String, UUID, ForeignKey, Float, Boolean
from sqlalchemy import Enum as SQLEnum
from app.db.database import Base

from ..enums.organissation_status_enums import OrganizationStatus

class Branch(Base):
    __tablename__ = "branches"

    id :Mapped[uuid.UUID] = mapped_column(
                       UUID(as_uuid=True),
                        primary_key=True,
                       default=uuid.uuid4,
                            )
    branch_name: Mapped[str]=mapped_column(
         String(80),
    )
    organisation_id : Mapped[uuid.UUID] =  mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id",ondelete="CASCADE"),
    )
    address:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    city:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    state:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    zip_code:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    longitude:Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    latitude:Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    geofencing : Mapped[int] = mapped_column(
        Integer,
        default=100,
    )
    grace_period : Mapped[int] = mapped_column(
        Integer,
    )
    total_number_of_paid_leaves :Mapped[int] = mapped_column(
        Integer,
        default=2,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    status: Mapped[OrganizationStatus]  =mapped_column(
        SQLEnum(OrganizationStatus)

    )
    organisation = Relationship(
                "Organisation",
                 back_populates="branch",
    )

    employee = Relationship(
        "Employee",
                 back_populates="branch",
    )
    attendance_records = Relationship(
        "Attendance",
        back_populates="branch",
    )

    shift = Relationship(
        "Shift",
            back_populates="branch",
        cascade="all, delete-orphan",
    )

    department = Relationship(
        "DepartmentModel",
            back_populates="branch",
        cascade="all, delete-orphan",
    )

    role = Relationship(
        "OrganisationRoles",
            back_populates="branch",
    )