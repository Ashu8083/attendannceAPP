import uuid
from datetime import date
from datetime import datetime
from ..db.database import Base
from sqlalchemy.orm  import Mapped , mapped_column,relationship
from sqlalchemy import String,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum

from app.enums.user_status_enums import UserStatus
from app.enums.role_enums import UserRole
from app.db.timestamp import TimestampMixin


class User(Base,TimestampMixin):
    __tablename__ = "user"

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid= True),
        primary_key=True,
        default=uuid.uuid4
    )
    organisation_id : Mapped [uuid.UUID] = mapped_column(
        ForeignKey("organisation.id")
    )
    full_name : Mapped [str] = mapped_column(
        String (225)
    )
    email : Mapped[str] = mapped_column(
        String(225),
        unique = True
    )
    profile_image : Mapped[str] = mapped_column(
        String(225),
        nullable= True
    )
    password_hash : Mapped[str] = mapped_column(
        String(225),
        nullable= True
    )
    role : Mapped[UserRole] = mapped_column(
         SQLEnum(UserRole),
         default= UserRole.EMPLOYEE
    )
    status : Mapped [UserStatus] = mapped_column(
        SQLEnum(UserStatus),
        default= UserStatus.ACTIVE,
        nullable= True
    )
    device = relationship(
        "UserDeviceDetails",
        back_populates ="user"
    )
    organisation = relationship(
        "Organisation",
        back_populates="user"
    )
    
    

