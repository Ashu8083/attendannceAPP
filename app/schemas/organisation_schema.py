from typing import Optional

from pydantic import BaseModel,ConfigDict

from datetime import date,datetime

from app.enums.organissation_status_enums import OrganizationStatus
from app.enums.subcription_type import SubscriptionType
from app.models.employee_models import Employee

class CreateOrganisation(BaseModel) :  
    organisation_name :str
    organisation_email : str 
    organisation_status : OrganizationStatus
    organisation_phone : str
    organisation_address :str    
class OrgnisationDetails(BaseModel):

    organisation_name :str
    organisation_code :str
    organisation_status : OrganizationStatus
    subscription_type: Optional[SubscriptionType] = None

class OrganisationUpdateStatus(BaseModel):
    organisation_name :str
    organisation_status : OrganizationStatus

class OrganisationDetailsUpdate(BaseModel):
    organisation_name :str
    organisation_staus : str
    subscription_type : Optional[SubscriptionType] = None

class OrganisationDetailsResponse(BaseModel):

    name: str

    organisation_code: str

    organisation_email: str

    status: OrganizationStatus

    model_config = ConfigDict(from_attributes=True)