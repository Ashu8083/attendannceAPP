import uuid
from datetime import date,datetime


from sqlalchemy import Date, ForeignKey,DateTime,String
from sqlalchemy.orm import Mapped, mapped_column,relationship
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
        UUID(as_uuid = True),
        ForeignKey("employees.id"),
        nullable= False
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id"),
        nullable= True,
    )
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[date] = mapped_column(Date)
    status: Mapped[LeaveStatus] = mapped_column(
        SQLEnum(LeaveStatus)
    )
    reason : Mapped[str] = mapped_column(
        String(300)
    )
    approved_by :Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id")
    )
    approved_at : Mapped[datetime] = mapped_column(
        DateTime
    )
    employee = relationship(
                            "Employee",
                            back_populates="leave_requests"
                            )
    organisation = relationship(
        "Organisation",
        back_populates="leave_requests"
    )

    @property
    def employee_code(self):
        return self.employee.code