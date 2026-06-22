import uuid

from sqlalchemy import ForeignKey,String
from sqlalchemy.orm import Mapped , mapped_column
from sqlalchemy.dialects.postgresql import UUID 


from ..db.database import Base


class Employee(Base):

    __tablename__ = "employees"
    id  : Mapped[uuid.UUID]= mapped_column(
        UUID(as_uuid = True),
        primary_key = True,
        default = uuid.uuid4
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


