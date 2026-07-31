import uuid

from sqlalchemy.orm import Session
from sqlalchemy import func, select
from app.models.organisations import Organisation
from app.schemas.organisation_schema import CreateOrganisation,OrganisationDetailsUpdate,OrganisationDetailsResponse


class OrganisationRepo:

    def __init__(self, db: Session):
        self.db = db

    def check_organisation(self, organisation_id: uuid.UUID) :
        return self.db.query(Organisation.id).filter(Organisation.id == organisation_id).first()


    def get_organisation_by_code(self, code: str) :
        return (
            self.db.query(Organisation)
            .filter(Organisation.organisation_code == code)
            .first()
        )

    def get_organisation_by_id(self, organisation_id):
        return (
            self.db.query(Organisation)
            .filter(Organisation.id == organisation_id)
            .first()
        )
    def get_organisation_by_email(self,organisation_email) -> Organisation:
        return (
            self.db.query(Organisation)
            .filter(Organisation.organisation_email == organisation_email)
            .first()
        )

    def get_organisation_id_by_organisation_code(self, organisation_code: str):
        return (
            self.db.query(Organisation.id)
            .filter(Organisation.organisation_code == organisation_code).scalar())

    def create_organisation(
        self,
        data: CreateOrganisation,
        code :str
    ) -> OrganisationDetailsResponse:

        organisation = Organisation(
            name=data.organisation_name,
            organisation_code=code,
            organisation_email = data.organisation_email,
            status=data.organisation_status,
            phone_number = data.organisation_phone,
            address =data.organisation_address

        )

        self.db.add(organisation)
        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    def update_organisation(self,organisation_code:str ,data: OrganisationDetailsUpdate):
    
        organisation = self.db.query(Organisation).filter(Organisation.organisation_code == organisation_code)
        for feild in data.model_dump().items():
            setattr(organisation,feild,data)
        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    def delete_organisation(self, organisation: Organisation):

        self.db.delete(organisation)
        self.db.commit()