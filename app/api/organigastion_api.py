from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from ..schemas.organisation_schema import CreateOrganisation,OrgnisationDetails
from app.service.organisation_service import OrganisationService
from app.dependancy.service_dependancy import get_organaistion_service

router = APIRouter()

@router.post("/create")
def create(
    data: CreateOrganisation,
    service: OrganisationService = Depends(get_organaistion_service)
):
    organisation = service.create_oranisation(data)
    return {
        "id": str(organisation.id),
        "name": organisation.name
    }