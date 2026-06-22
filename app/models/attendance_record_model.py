import uuid
from datetime import date

from sqlalchemy import String ,ForeignKey ,Date
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum 

from ..db.database import Base
from ..enums.attandance_status import AttendanceStatus
from ..db.timestamp import TimestampMixin


class Attendance(Base,TimestampMixin):
    
    __tablename__ = "attendance_records"

    id  : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid= True),
        primary_key= True,
        default= uuid.uuid4
    )

    employee_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id")
    )
    attendance_data : Mapped[date] = mapped_column(
        Date
    )
    punchin_time : Mapped[date] = mapped_column(
        Date
    )
    punchout_time :Mapped[date] = mapped_column(
        Date
    )
    status: Mapped[AttendanceStatus] = mapped_column(
        SQLEnum(AttendanceStatus)
    )