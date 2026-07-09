from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.organisation_schema import CreateOrganisation, OrganisationDetailsResponse,OrgnisationDetails,OrganisationUpdateStatus
from app.service.organisation_service import OrganisationService
from app.dependancy.service_dependancy import get_organaistion_service

organisation_router = APIRouter(prefix="/organisation",tags=["organisation"])

@organisation_router.post("/create",response_model=OrganisationDetailsResponse)
def create(
    data: CreateOrganisation,
    service: OrganisationService = Depends(get_organaistion_service)
):
    organisation = service.create_oranisation(data)
    return organisation

@organisation_router.get("/get_organisation/{organisation_code}")
def get_organisation_details(
    organisation_code: str,
    service: OrganisationService = Depends(get_organaistion_service)
):
    organisation = service.get_organisation(organisation_code)
    return organisation


@organisation_router.put("/update_organisation/{organisation_code}")
def upadate_organisation_details(
    organisation_code : str,
    data : OrganisationUpdateStatus,
    service : OrganisationService = Depends(get_organaistion_service)
):
    try : 
        organisation :OrgnisationDetails = service.update_organisation(organisation_code,data)
        return {
            "id": str(organisation.id),
            "name": organisation.name
                }
    except  Exception as e : 
        JSONResponse(
            content= "error",
            status_code=400
        )
    
