from enum import Enum

class SubscriptionType(str, Enum):
    YEARLY = "YEARLY"
    MONTHLY = "MONTHLY"