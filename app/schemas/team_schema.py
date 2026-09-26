import uuid
from pydantic import  BaseModel

class CreateTeam(BaseModel):
    name: str
    department_id: int
    team_head : uuid.UUID
    description: str | None = None
    is_activated: bool

class UpdateTeam(BaseModel):
    name: str | None = None
    team_head: uuid.UUID | None = None
    description: str | None = None
    is_activated: bool | None = None

class TeamSearchFilter(BaseModel):
    department_id: int | None = None
    name: str | None = None
    is_activated: bool | None = None



