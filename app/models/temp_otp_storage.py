from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Boolean,Time
from sqlalchemy.orm import relationship,mapped_column,Mapped
from sqlalchemy.dialects.postgresql import UUID
from app.db.database import  Base
from app.db.timestamp import TimestampMixin
from datetime import datetime,time
import uuid


class TempOtpStorage(Base,TimestampMixin):
    __tablename__ = 'temp_otp_storage'

    id  : Mapped [uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key = True,
        default=uuid.uuid4
    )
    otp = Column(String )
    date : Mapped[datetime] = Column(DateTime,nullable = False)
    expire_time : Mapped[time] = mapped_column(
        Time,
    )
    user_id : Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
    )
    user = relationship("User",
                        back_populates="temp_otp_storage")
    is_expired : Mapped[bool] = mapped_column(
        Boolean,
        default = False,
    )

