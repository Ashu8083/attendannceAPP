from app.schemas.organisation_schema import CreateOrganisation,OrgnisationDetails
from app.repo.organisation_repo import OrganisationRepo


class OrganisationService():
    def __init__(self,organisationrepo :OrganisationRepo):
        self.organisationRepo = organisationrepo

    def generate_organissation_code(organissation_name):

        return

    def create_oranisation(self,data: CreateOrganisation ):

        existing_org = self.organisationRepo.get_organisation_by_code(data.organisation_code)
        if existing_org:
                raise ValueError("Organisation already exists")
        organisation = self.organisationRepo.create_organisation(data)

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


