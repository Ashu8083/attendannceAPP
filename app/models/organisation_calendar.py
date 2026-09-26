import uuid
from sqlalchemy import UniqueConstraint, UUID, ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class OrganisationCalendar(Base,TimestampMixin):
    __tablename__ = "organisation_calendar"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default= uuid.uuid4(),
    )
    organisation_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id",ondelete="CASCADE"),
    )

    organisation_branch_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("branches.id",ondelete="CASCADE"),
        nullable=True,      
    )
    name : Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )
    finance_year_start: Mapped[Date] = mapped_column(
        Date,
    )
    finance_year_end: Mapped[Date] = mapped_column(
        Date,
    )
    status: Mapped[str] = mapped_column(
        String(255),
    )

    organisation = relationship(
        "Organisation",
        back_populates="organisation_calendar",

    )
    holidays = relationship(
        "Holidays",
        cascade="all, delete-orphan",
    )
    work_schedule = relationship(
        "OrganisationWorkSchedule",
        back_populates="calendar",
        cascade="all, delete-orphan",
    )
