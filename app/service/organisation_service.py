import re
import uuid

from app.schemas.organisation_schema import CreateOrganisation,OrgnisationDetails,OrganisationUpdateStatus,OrganisationDetailsUpdate
from app.repo.organisation_repo import OrganisationRepo



class OrganisationService():
    def __init__(self,organisationrepo :OrganisationRepo):
        self.organisationRepo = organisationrepo

    def generate_organissation_code(self,org_name: str) -> str:

        prefix = re.sub(r'[^A-Za-z]', '', org_name)[:3].upper()

        unique_part = str(uuid.uuid4()).replace("-", "")[:6].upper()

        return f"{prefix}-{unique_part}"


    def create_oranisation(self,data: CreateOrganisation ):

        existing_org = self.organisationRepo.get_organisation_by_email(data.organisation_email)
        if existing_org:
                raise ValueError("Organisation already exists")
        code =self.generate_organissation_code(data.organisation_name)
        organisation = self.organisationRepo.create_organisation(data,code=code)

        return organisation
    
    def get_organisation(self,organisation_code):

        organisation = self.organisationRepo.get_organisation_by_code(organisation_code)
        if not organisation:
            return
        response  = OrgnisationDetails(
                    organisation_name= organisation.name,
                    organisation_code= organisation.organisation_code,
                    organisation_status=organisation.status,
                    subscription_type=  (
                                            organisation.subscription.subscription_type
                                            if organisation.subscription
                                            else None
                                         )
        )
        return response
    
    def update_organisation(self,organisation_code :str,
                            data :OrganisationDetailsUpdate):
        organisation = self.organisationRepo.get_organisation_by_code(organisation_code)
        if not organisation :
             raise {
                  "organisation not found"
             }
        organisation=  self.organisationRepo.update_organisation(organisation_code,data)
        return organisation
        
         


