import uuid
from sqlalchemy import String ,ForeignKey ,Boolean
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum 

from ..db.database import Base
from ..enums.attandance_status import AttendanceStatus
from ..db.timestamp import TimestampMixin


class AttendanceLog(Base,TimestampMixin):
    __tablename__ = "attendance_log"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default= uuid.uuid4
    )
    attendance_records_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("attendance_records.id")
    )
    oranisation_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id")
    )
    device_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("userdevice.id")
    )
    log : Mapped[str] = mapped_column(
        String(225)
    )
    is_success : Mapped[bool] = mapped_column(
        Boolean,
        default= False
    )

