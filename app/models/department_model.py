from sqlalchemy.orm import Mapped , mapped_column,relationship
from sqlalchemy import ForeignKey,String , Integer
import uuid


from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.dialects.postgresql import UUID

from app.db.database import Base
from app.db.timestamp import TimestampMixin

class DepartmentModel(Base,TimestampMixin):

    __tablename__ = "department"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key= True,
    )
    deparrments : Mapped[str] = mapped_column(
        String(25)
    )
    organization_id: Mapped[uuid.UUID] = mapped_column(
                                UUID(as_uuid=True),
                                ForeignKey("organisation.id"),
                                nullable=False
                                )
    shift_time : Mapped[int] = mapped_column(
            ForeignKey("shift.id"),
            nullable=False
    )
    organization = relationship(
    "Organisation",
    back_populates="departments"
    )
