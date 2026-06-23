import uuid

from datetime import datetime
from sqlalchemy import ForeignKey,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Enum as SQLEnum
from app.db.database import Base
from app.enums.subcription_type import SubscriptionType
from app.db.timestamp import TimestampMixin

class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    organisation_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("organisation.id"),
        unique=True
    )

    subscription_type: Mapped[SubscriptionType] = mapped_column(
        SQLEnum(SubscriptionType)
    )

    starting_date: Mapped[datetime] = mapped_column(
        DateTime
    )

    organisation: Mapped["Organisation"] = relationship(
        "Organisation",
        back_populates="subscription"
    )