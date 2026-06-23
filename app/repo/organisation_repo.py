from sqlalchemy.orm import Session

from app.models.organisations import Organisation
from app.schemas.organisation_schema import CreateOrganisation


class OrganisationRepo:

    def __init__(self, db: Session):
        self.db = db

    def get_organisation_by_code(self, code: str) -> Organisation | None:
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

    def get_organisation_id(self, organisation_code: str):
        return (
            self.db.query(Organisation.id)
            .filter(
                Organisation.organisation_code == organisation_code
            )
            .scalar()
        )

    def create_organisation(
        self,
        data: CreateOrganisation
    ) -> Organisation:

        organisation = Organisation(
            name=data.organisation_name,
            organisation_code=data.organisation_code,
            status=data.organisation_status
        )

        self.db.add(organisation)
        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    def update_organisation(self, organisation: Organisation):

        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    def delete_organisation(self, organisation: Organisation):

        self.db.delete(organisation)
        self.db.commit()