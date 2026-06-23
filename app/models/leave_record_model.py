import uuid
from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum

from ..db.database import Base
from ..enums.leave_status import LeaveStatus
from ..db.timestamp import TimestampMixin

class LeaveRequest(Base,TimestampMixin):
    __tablename__ = "leave_requests"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("employees.id")
    )
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[LeaveStatus] = mapped_column(
        SQLEnum(LeaveStatus)
    )
    approved_by :Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id")
    )