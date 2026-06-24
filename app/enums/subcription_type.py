from enum import Enum

class SubscriptionDuration(str, Enum):
        Freeimium = "Freeimium"
        Basic = "Basic"
        Premimum = "Premimum"

class SubscriptionType(str,Enum):
        YEARLY = "YEARLY"
        MONTHLY = "MONTHLY"
