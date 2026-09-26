from sqlalchemy.orm import Session

from app.models import Team
from app.models import DepartmentModel, Organisation
from app.schemas.team_schema import UpdateTeam
from app.schemas.team_schema import TeamSearchFilter


class TeamRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, team: Team):
        self.db.add(team)
        self.db.commit()
        self.db.refresh(team)
        return team

    def update(self, team ,team_update: UpdateTeam):

        updated_data = team_update.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(team, key, value)
        self.db.commit()
        self.db.refresh(team)
    def get_team_by_id(self, team_id: int) :
        return self.db.query(Team).filter(Team.id == team_id).first()


    def search_team_by_filter(self,team:TeamSearchFilter,organisation_id,branch_id ):

        query = self.db.query(Team)
        query = query.join(DepartmentModel,
                           Team.department_id == DepartmentModel.department_id)

        query = query.filter(DepartmentModel.organisation_id == organisation_id,
                             DepartmentModel.branch_id == branch_id)

        if team.department_id :
            query = query.filter(Team.department_id == team.department_id)

        if team.name :
            query = query.filter(
                Team.name.ilike(f"%{team.name}%"))

        if team.is_activated is not None:
            query = query.filter(
                Team.is_activated == team.is_activated
            )

        return query.all()










