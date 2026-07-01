from pydantic import BaseModel
import uuid
class CreateRole(BaseModel):


    name: str
    description :str

class CreatePermision(BaseModel):
    name: str
    description : str
    
class CreateRolePermision(BaseModel):
    role_id : uuid.UUID
    permission_id: uuid.UUID

class UpadteRolerPermision(BaseModel):
    name: str | None = None
    description: str | None = None

class RoleResponse(BaseModel):

    id: uuid.UUID
    organisation_id: uuid.UUID
    name: str
    description: str