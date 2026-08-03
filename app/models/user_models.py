import uuid
from datetime import date
from datetime import datetime
from ..db.database import Base
from sqlalchemy.orm  import Mapped , mapped_column,relationship
from sqlalchemy import String,ForeignKey,DateTime,Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Enum as SQLEnum

from app.enums.user_status_enums import UserStatus
from app.enums.scops import AccountType

from app.db.timestamp import TimestampMixin



class User(Base,TimestampMixin):
    __tablename__ = "user"
    __table_args__ = (
        Index("idx_user_organisation_id", "organisation_id","id"),
        Index("idx_user_email", "email","id"),

)

    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid= True),
        primary_key=True,
        default=uuid.uuid4
    )
    organisation_id : Mapped [uuid.UUID] = mapped_column(
        ForeignKey("organisation.id"),
        nullable= True
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
    account_type: Mapped[AccountType] = mapped_column(
        SQLEnum(AccountType),
        nullable= False
    )

    # system_role : Mapped[UserRoleUpdated] = mapped_column(
    #      SQLEnum(UserRoleUpdated),
    #      default= UserRoleUpdated.SYSTEM_USER
    # )
    status : Mapped [UserStatus] = mapped_column(
        SQLEnum(UserStatus),
        default= UserStatus.ACTIVE,
        nullable= True
    )
    # role_id: Mapped[uuid.UUID] = mapped_column(
    #     ForeignKey("role.id"),
    #     nullable= True
    # )
    employee = relationship(
        "Employee",
        back_populates="user",
        uselist=False,
    )
    device = relationship(
        "UserDeviceDetails",
        back_populates ="user"
    )
    organisation = relationship(
        "Organisation",
        back_populates="user"
    )
    temp_otp_storage = relationship(
        "TempOtpStorage",
        back_populates="user"
    )
    # role = relationship(
    #     "Role",
    #     back_populates="user"
    # )

    user_role = relationship(
        "UserRole",
        back_populates="user",
        uselist=False,
    )


