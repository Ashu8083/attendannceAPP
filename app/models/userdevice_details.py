import uuid
from datetime import datetime, date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey,Integer,String,DateTime,Boolean

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class UserDeviceDetails(Base, TimestampMixin):
    __tablename__ = "userdevice"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key= True,
        default=uuid.uuid4
    )
    user_id = mapped_column(
                            UUID(as_uuid=True),
                            ForeignKey("user.id"),
                            nullable=False
                            )
    
    device_type : Mapped[str] = mapped_column(
        String
    )
    device_unique_id : Mapped[str] = mapped_column(
        String
    )
    firebaseFCM_token : Mapped[str] = mapped_column(
        String
    )
    refresh_token_id : Mapped[uuid.UUID] = mapped_column(
        UUID
    )
    last_login : Mapped[datetime] = mapped_column(
        DateTime
    )
    logout_time : Mapped[datetime] = mapped_column(
        DateTime
    )
    is_login : Mapped[bool] = mapped_column(
        Boolean ,
        default= True
    )
    user = relationship(
                        "User",
                        back_populates="devices"
                        )