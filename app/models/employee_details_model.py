import uuid
from datetime import date
from sqlalchemy import ForeignKey,String,Date,Index
from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy.dialects.postgresql import ENUM as SQLEnums
from ..db.timestamp import TimestampMixin
from app.db.database import Base


class EmployeeDetails(Base, TimestampMixin):
    __tablename__ = "employee_details"

    __table_args__ = (
        Index(
            "employee_id",
            "full_name",
            "dob",
            "gender",
            "marital_status",
        ),
        Index(
            "idx_city"
            "employee_id",
            "full_name",
            "city"
    )
    )

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default=uuid.uuid4
    )
    employee_id : Mapped[uuid.UUID]= mapped_column(
        ForeignKey("employees.id")
    )
    full_name : Mapped[str] = mapped_column(
        String(50)
    )
    dob : Mapped[date] = mapped_column(
        Date
    )

    gender :Mapped[str] = mapped_column(
        String(10)
    )
    marital_status :Mapped[str] = mapped_column(
        String(20)
    )
    address : Mapped[str] = mapped_column(
        String(30)
    )
    city : Mapped[str] = mapped_column(
        String(30)
    )
    state : Mapped[str] = mapped_column(
        String(30)
    )
    employee = relationship(
    "Employee",
    back_populates="employee_details"
)

