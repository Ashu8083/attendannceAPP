import uuid
from datetime import datetime

from sqlalchemy import String ,ForeignKey ,DateTime
from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum 

from ..db.database import Base
from ..enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode
from ..db.timestamp import TimestampMixin


class Attendance(Base,TimestampMixin):
    
    __tablename__ = "attendance_records"

    id  : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid= True),
        primary_key= True,
        default= uuid.uuid4
    )
    organisation_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id"),
        nullable= False
    )
    employee_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id")
    )
    attendance_date : Mapped[datetime] = mapped_column(
        DateTime
    )
    punchin_time : Mapped[datetime] = mapped_column(
        DateTime
    )
    punchout_time :Mapped[datetime] = mapped_column(
        DateTime
    )
    status: Mapped[AttendanceStatus] = mapped_column(
        SQLEnum(AttendanceStatus,
                native_enum=False,
                validate_strings=True)
    )
    work_mode : Mapped[WorkMode] = mapped_column(
        SQLEnum(
        WorkMode,
        native_enum=False,
        validate_strings=True
    )
    )
    organisation = relationship(
        "Attendance_Record",
        back_populates="organisation"
    )
    
    
