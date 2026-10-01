from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.organisation_schema import( CreateOrganisation,
                                             OrganisationDetailsResponse,
                                             OrganisationUpdateStatus,
                                             UpdateOrganisationSubscription)


from app.service.organisation_service import OrganisationService
from app.dependancy.service_dependancy import get_organaistion_service
from app.core.response_helper import CommonJSONResponse

organisation_router = APIRouter(prefix="/organisation",tags=["organisation"])

@organisation_router.post("/create",response_model=OrganisationDetailsResponse)
def create(
    data: CreateOrganisation,
    service: OrganisationService = Depends(get_organaistion_service)
):
    organisation = service.create_oranisation(data)
    return CommonJSONResponse(
        content= organisation.json(),
        status_code=201,
        message= "Organisation created"
    )

@organisation_router.get("/get_organisation/{organisation_code}",response_model=OrganisationDetailsResponse)
def get_organisation_details(
    organisation_code: str,
    service: OrganisationService = Depends(get_organaistion_service)
):
    organisation = service.get_organisation(organisation_code)
    return CommonJSONResponse(
        content= organisation.json(),
        status_code=200,
        message= "Organisation retrieved"
    )


@organisation_router.patch("/update_organisation/{organisation_code}")
def update_organisation_details(
    organisation_code : str,
    data : OrganisationUpdateStatus,
    service : OrganisationService = Depends(get_organaistion_service)
):
    try : 
        organisation  = service.update_organisation(organisation_code,data)
        return CommonJSONResponse(
            content= organisation.json(),
            status_code=200,
            message= "Organisation updated"

        )
    except  Exception as e : 
        JSONResponse(
            content= "error",
            status_code=400
        )
    
@organisation_router.patch("/update_organisation_subcription", response_model= OrganisationDetailsResponse)
def update_organisation_subscription(update_schema :UpdateOrganisationSubscription ):
    return
