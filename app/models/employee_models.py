import uuid

from datetime import date

from ..enums.employee_status import  EmployeeStatus
from sqlalchemy import ForeignKey,String,Date
from sqlalchemy.orm import Mapped , mapped_column
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
    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id")
    )
    oganisation_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id")
    )
    emplopyee_code: Mapped[str] = mapped_column(
        String(50),
        unique = True
    )
    department: Mapped[str] = mapped_column(
        String(100)
    )
    designation: Mapped[str] = mapped_column(
        String(100)
    )
    emplopyee_status : Mapped[EmployeeStatus] = mapped_column(
            SQLEnums(EmployeeStatus)
    )
    join_date : Mapped[date] = mapped_column(
        Date
    )
    # manaer_id : Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("user.id")
    # )
     
     


