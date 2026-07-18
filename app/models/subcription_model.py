import uuid
from enum import Enum 
from datetime import datetime
from sqlalchemy import ForeignKey,DateTime,String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum


from sqlalchemy import Enum as SQLEnum
from app.db.database import Base
from app.enums.subcription_type import (SubscriptionTypeORG
                                        ,SubscriptionStatusORG,
                                         SubscriptionDuratioORG )
from app.db.timestamp import TimestampMixin

class Subscription(Base, TimestampMixin):
    __tablename__ = "subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    subscription_type: Mapped[SubscriptionTypeORG] = mapped_column(
        SQLEnum(SubscriptionTypeORG)
    )
    organisation_id = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id", ondelete="CASCADE"),
        unique=True,  # one subscription per organisation
        nullable=False,
    )

    starting_date: Mapped[datetime] = mapped_column(
        DateTime
    )

    ending_date : Mapped[datetime]= mapped_column(
        DateTime
    )

    subscription_duration : Mapped[SubscriptionDuratioORG] = mapped_column(
        SQLEnum(SubscriptionDuratioORG),
        nullable= True
    )

    subscription_status : Mapped[SubscriptionStatusORG] = mapped_column(
        SQLEnum(SubscriptionStatusORG),
        default= SubscriptionStatusORG.ACTIVE
    )


    organisation = relationship(
        "Organisation",
        back_populates="subscription"
    )