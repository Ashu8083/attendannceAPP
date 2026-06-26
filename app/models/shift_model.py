import uuid
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import String,ForeignKey,Integer
from sqlalchemy import Time
from datetime import time

from sqlalchemy.dialects.postgresql import UUID

from app.models.organisations import Organisation
from app.db.database import Base
from app.db.timestamp import TimestampMixin


class Shift(Base,TimestampMixin):

    __tablename__ = "shift"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key= True
    )
    name : Mapped[str] = mapped_column(
        String(22),
        nullable= False
    )
    organisation_id :Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid = True),
       ForeignKey("organisation.id"),
        nullable= False
    )
    start_time : Mapped[time] = mapped_column(
        Time
    )
    end_time : Mapped[time] = mapped_column(
        Time
    )
    grace_minutes : Mapped[int] = mapped_column(
        Integer
    )
    organisation = relationship(
                                "Organisation",
                                back_populates="shifts"
                                )
