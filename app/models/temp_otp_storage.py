from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship,mapped_column,Mapped
from app.db.database import  Base
from app.db.timestamp import TimestampMixin
from datetime import datetime,time
import uuid


class TempOtpStorage(Base,TimestampMixin):
    __tablename__ = 'temp_otp_storage'

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    expire_time : Mapped[time] = mapped_column(
        DateTime,
    )
    user_id = Mapped[uuid.UUID] = mapped_column(
        ForeignKey('user.id', onupdate='CASCADE', ondelete='CASCADE'),
    )
    user = relationship("User",
                        back_populates="temp_otp_storage")

