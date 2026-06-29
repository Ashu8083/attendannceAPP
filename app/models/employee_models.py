import uuid

from datetime import date

from app.enums.work_mode import WorkMode

from ..enums.employee_status import  EmployeeStatus
from sqlalchemy import ForeignKey,String,Date, UniqueConstraint
from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.dialects.postgresql import ENUM as SQLEnums
from ..db.timestamp import TimestampMixin


from ..db.database import Base


class Employee(Base,TimestampMixin):

    __tablename__ = "employees"
    id  : Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4
    )
    __table_args__ = (
        UniqueConstraint(
            "organisation_id",
            "employee_code",
            name="uq_org_employee_code"
        ),
    )
    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id")
    )
    organisation_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id")
    )
    employee_code: Mapped[str] = mapped_column(
        String(50),
        unique = True
    )
    department: Mapped[str] = mapped_column(
        String(100),
        nullable= True
    )
    designation: Mapped[str] = mapped_column(
        String(100),
        nullable=True
    )
    emplopyee_status : Mapped[EmployeeStatus] = mapped_column(
            SQLEnums(EmployeeStatus),
            default=EmployeeStatus.ACTIVE
    )
    shift_id : Mapped[int] = mapped_column(
        ForeignKey("shift.id"),
        nullable= True
    )
    join_date : Mapped[date] = mapped_column(
        Date
    )
    shift =  relationship(
        "Shift",
        back_populates= "employee"

    )
    # manaer_id : Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("user.id")
    # )

    # Employee.py

    role_id:Mapped[uuid.UUID] = mapped_column(
                                                UUID(as_uuid=True),
                                                ForeignKey("role.id"),
                                                nullable=True,
    )
    work_mode : Mapped[WorkMode] = mapped_column(
                                                SQLEnums(
                                                WorkMode,
                                                native_enum=False,
                                                validate_strings=True,
                                                ),
                                                default=WorkMode.WFO
                                                )

    role = relationship(
                        "Role",
                        back_populates="employee",
                        )
    leave_requests = relationship(
                                "LeaveRequest",
                                back_populates= "employee",
                                cascade= "all,delete-orphan"
                                )
    documents = relationship(
                            "EmployeeDocuments",
                             back_populates="employee",
                             uselist=False
                            )
    employee_details= relationship(
                                    "EmployeeDetails",
                                    back_populates="employee",

                                 )
    organisation = relationship(
                                 "Organisation",
                                 back_populates="employee"
                                )
    attendance_records = relationship(
                                        "Attendance",
                                         back_populates="employee"
)
     
     


