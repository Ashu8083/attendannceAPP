from pydantic import BaseModel, Field
from uuid import UUID
from app.enums.subcription_type import SubscriptionTypeORG,SubscriptionDuratioORG,SubscriptionStatusORG
from datetime import datetime

class SubscriptionCreate(BaseModel):

    organisation_id: UUID

    subscription_type: SubscriptionTypeORG | None = None

    starting_date: datetime = Field(default_factory=datetime.now)

class UpdateSubscription(BaseModel):
     
    organisation_id : UUID
    subscription_type : SubscriptionTypeORG | None
    subscription_status: SubscriptionStatusORG | None
    starting_date : datetime = Field(default_factory=datetime.now)


