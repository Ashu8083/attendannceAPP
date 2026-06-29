
import uuid


from ..db.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import String , ForeignKey,Float,Integer
from sqlalchemy.dialects.postgresql import UUID 
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped , mapped_column
from ..enums.organissation_status_enums import OrganizationStatus


from ..enums.organissation_status_enums import OrganizationStatus
from ..db.timestamp import TimestampMixin

class Organisation(Base,TimestampMixin):

    __tablename__ = "organisation"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID (as_uuid= True),
        primary_key=True,
        default=uuid.uuid4
    )
    name : Mapped[str] = mapped_column(String(225))
    organisation_code : Mapped[str] = mapped_column(
                                                    String(20),
                                                    unique= True,
                                                    index=True)    
    status: Mapped[OrganizationStatus]= mapped_column(
        SQLEnum(OrganizationStatus)
    )
    subscription: Mapped["Subscription"] = relationship(
    "Subscription",
    back_populates="organisation",
    uselist=False
    )
    organisation_email : Mapped[str] = mapped_column(
      String(225),
      unique= True,
      index= True,
    )
    address : Mapped[str] = mapped_column(
        String(225)
    )
    phone_number : Mapped[str] = mapped_column(
        String(20)
    )

    latitude : Mapped[float] = mapped_column(Float,
                                             nullable=True)
    longitude : Mapped[Float] = mapped_column(Float,
                                              nullable=True)
    allowed_radius = mapped_column(Integer, default=100)
    number_of_employee : Mapped[int] = mapped_column(
        Integer,
        default= 0
    )
    departments = relationship(
                                "DepartmentModel",
                                 back_populates="organization",
                                 cascade="all, delete-orphan"
                                )
   
    attendance_records = relationship(
                        "Attendance",
                        back_populates="organisation",
                        cascade="all,delete-orphan"
                        )

    employee = relationship(
                            "Employee",
                            back_populates="organisation",
                            cascade="all,delete-orphan"
                            )
    shift = relationship(
                        "Shift",
                        back_populates="organisation"
                        )
    user =  relationship(
        "User",
        back_populates="organisation"
    )
