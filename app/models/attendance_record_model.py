import uuid
from datetime import datetime,date,time

from sqlalchemy import String ,ForeignKey ,DateTime, UniqueConstraint,Date,Boolean,Time
from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum 

from ..db.database import Base
from ..enums.attandance_status import AttendanceStatus
from app.enums.work_mode import WorkMode
from ..db.timestamp import TimestampMixin


class Attendance(Base,TimestampMixin):
    
    __tablename__ = "attendance_records"

    __table_args__ = (UniqueConstraint(
                                        "employee_id",
                                        "attendance_date",
                                        name="uq_employee_attendance_date",
                                        ),
                        )
    #__table_args__ make sure that combination employee and attendance date must be unique

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
    attendance_date : Mapped[date] = mapped_column(
        Date
    )
    is_punchin : Mapped[bool] = mapped_column(
        Boolean ,
        default= False
    )
    punchin_time : Mapped[time] = mapped_column(

        Time,
    )
    is_punchout :Mapped[bool] = mapped_column(
        Boolean,
        default= False
    )
    punchout_time :Mapped[time] = mapped_column(
        Time,
        nullable= True
    )
    status: Mapped[AttendanceStatus] = mapped_column(
        SQLEnum(AttendanceStatus,
                native_enum=False,
                validate_strings=True),
                default= AttendanceStatus.PRESENT
    )
    work_mode : Mapped[WorkMode] = mapped_column(
        SQLEnum(
        WorkMode,
        native_enum=False,
        validate_strings=True
    )
    )
    organisation = relationship(
        "Organisation",
        back_populates="attendance_records"
    )
    
    employee = relationship(
    "Employee",
    back_populates="attendance_records"

)
