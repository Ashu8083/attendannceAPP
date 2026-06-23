import uuid

from datetime import datetime
from sqlalchemy import ForeignKey,DateTime,String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Enum as SQLEnum

from ..db.database import Base
from ..enums.subcription_type import SubscriptionType
from ..db.timestamp import TimestampMixin

class Subscription(Base,TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )
    organisation_id: Mapped[uuid.UUID] = mapped_column(
    ForeignKey("organisation.id")
)
    subscription_type: Mapped[SubscriptionType] = mapped_column(
        SQLEnum(SubscriptionType)
    )
    starting_date : Mapped[datetime] = mapped_column(
        DateTime
    )
    # method_of_payment : Mapped[str] = mapped_column(
    #     String
    # )