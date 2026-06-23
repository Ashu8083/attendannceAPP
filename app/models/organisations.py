
import uuid


from ..db.database import Base

from sqlalchemy.orm import relationship
from sqlalchemy import String , ForeignKey
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
    organisation_code : Mapped[str] = mapped_column(String(20),unique= True)    
    status: Mapped[OrganizationStatus]= mapped_column(
        SQLEnum(OrganizationStatus)
    )
    subscription: Mapped["Subscription"] = relationship(
    "Subscription",
    back_populates="organisation",
    uselist=False
)

