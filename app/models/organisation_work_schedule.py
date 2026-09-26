import uuid
from ..db.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import String, ForeignKey, Float, Integer, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped , mapped_column
from ..enums.organissation_status_enums import OrganizationStatus
from app.models.subcription_model import  Subscription

from ..enums.organissation_status_enums import OrganizationStatus
from ..db.timestamp import TimestampMixin


class OrganisationWorkSchedule(Base):
    __tablename__ = "organisation_work_schedule"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    calendar_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "organisation_calendar.id",
            ondelete="CASCADE"
        ),
        nullable=False,
    )
    day_of_week: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    is_working_day: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
    calendar = relationship(
        "OrganisationCalendar",
        back_populates="work_schedule",
    )