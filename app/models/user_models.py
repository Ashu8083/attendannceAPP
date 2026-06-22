import uuid
from datetime import datetime
from ..db.database import Base
from sqlalchemy.orm  import Mapped , mapped_column
from sqlalchemy import String,ForeignKey,DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum

from ..enums.user_status_enums import UserStatus
from ..enums.role_enums import UserRole
from ..db.timestamp import TimestampMixin


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
    password_hash : Mapped[str] = mapped_column(
        String(225)
    )
    role : Mapped[UserRole] = mapped_column(
         SQLEnum(UserRole)
    )
    status : Mapped [UserStatus] = mapped_column
    (
        SQLEnum (UserStatus)
    )
    

