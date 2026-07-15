from enum import Enum

class SubscriptionDuratioORG(str, Enum):

        UNDEFIND = "UNDFIND"
        YEARLY = "YEARLY"
        MONTHLY = "MONTHLY"

class SubscriptionTypeORG(str,Enum):
        FREEIMUM = "FREEMIUM"
        BASIC = "BASIC"
        PREMIMUM = "PREMIMUM"

class SubscriptionStatusORG(str,Enum):
        ACTIVE = "ACTIVE"
        EXPIRED = "EXPIRED"
        SUSPENDED = "SUPRNDED"
