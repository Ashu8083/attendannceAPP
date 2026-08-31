import uuid
from datetime import date
from enum import Enum as PyEnum
from app.db.database import Base

from sqlalchemy import String, UUID, ForeignKey, Date,Enum
from sqlalchemy.orm import Mapped,mapped_column,relationship

from app.db.timestamp import TimestampMixin
from app.enums.calender_enums import HolidayType, HolidayStatus

class Holidays(Base,TimestampMixin):
    __tablename__ = "holidays_calender"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    organisation_calender_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation_calendar.id"),
    )
    holidays_date: Mapped[date] = mapped_column(
        Date,
    )
    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        String(225),
    )
    type_of_holiday: Mapped[PyEnum] = mapped_column(
       Enum(HolidayType),
    )
    status: Mapped[PyEnum] = mapped_column(
        Enum(HolidayStatus),
    )

    organisation_calender = relationship(
        "OrganisationCalender",
        back_populates="holidays",

    )
