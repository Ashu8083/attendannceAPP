import uuid

from fastapi import APIRouter, Depends, Request, HTTPException

from app.dependancy.service_dependancy import get_team_service
from app.core.response_helper import CommonJSONResponse
from app.schemas.team_schema import CreateTeam, UpdateTeam, TeamSearchFilter
from app.service.TeamService import TeamService


team_router = APIRouter(
    prefix="/team",
    tags=["team"],
)

@team_router.get("/", tags=["team"])
async def get_team(
        request: Request,
        team_id : uuid.UUID,
        service: TeamService = Depends(get_team_service),
):

    team = service.get_team_by_id(team_id)
    return CommonJSONResponse(
        content=team,
        message=f"Team {team_id} found"
    )
@team_router.post("/", tags=["team"])
async def create_team(request : Request,
                      data : CreateTeam
                      ,service: TeamService = Depends(get_team_service)):

    team = service.create_team_service(request)
    return CommonJSONResponse(
        content=team,
        message=f"Team {team.id} created"
    )


@team_router.put("/", tags=["team"])
async def update_team(request: Request,
                      team_id : uuid.UUID,
                      update_data : UpdateTeam,
                      service : TeamService = Depends(get_team_service)):
    team = service.update_team_service(team_id, update_data)
    return CommonJSONResponse(
        content=team,
        message=f"Team {team_id} updated"
    )

@team_router.get("/", tags=["team"])
async def get_team_filter_search(request: Request,
                      search_filter:TeamSearchFilter = Depends(),
                      service: TeamService = Depends(get_team_service)):

    team = service.get_team_by_search_filter(search_filter,
                                             request.state.oganisation_id,
                                             request.state.branch_id)

    return CommonJSONResponse(
        content=team,
        message=f"Team {team.id} deleted"
    )








