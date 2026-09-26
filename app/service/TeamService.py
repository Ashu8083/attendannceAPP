import uuid

from  sqlalchemy.orm import Session


from app.core.logging_config import logger
from app.schemas.team_schema import CreateTeam, TeamSearchFilter, UpdateTeam
from app.repo.team_repo import TeamRepo


class TeamService:

    def __init__(self ,repo : TeamRepo, db : Session):
        self.repo = repo
        self.db = db

    def create_team_service(self,data:CreateTeam):
        try:
            team = self.repo.create(data)
        except Exception as e:
            logger.error(e)
            raise
        return team

    def get_team_by_id(self,team_id:int):
        self.repo.get_team_by_id(team_id)

    def get_team_by_search_filter(self , data:TeamSearchFilter,
                                         organisation_id :uuid.UUID ,
                                          branch_id :uuid.UUID):
        teams =  self.repo.search_team_by_filter(data,organisation_id ,branch_id)
        if teams:
            return teams
        else:
            raise

    def update_team_service(self,team_id:uuid.UUID,data:UpdateTeam):

        team = self.repo.get_team_by_id(team_id)
        if team is None:
            raise
        try:
            team = self.repo.update(team, data)
            return team
        except Exception as e:
            logger.error(e)
            raise






