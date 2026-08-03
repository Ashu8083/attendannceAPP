from typing import Optional
import uuid
from uuid import UUID
from pydantic import BaseModel
from app.enums.permission_scop import PermissionScopEnum,PermissionScopEnumUpdate


class CreateRoleSchema(BaseModel):
    name: str
    description :str

class CreatePermision(BaseModel):
    name: str
    description : str
    scope : PermissionScopEnumUpdate
    assignable : bool

class CreateListOfPermissions(BaseModel):
    permissions : list[CreatePermision]
    
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

class PermissionResponse(BaseModel):
    name : str
    description : str

class ListOFPermissions(BaseModel):
     permissions : list[CreatePermision]

class SystemRoleResponse(BaseModel):

    id: UUID
    role_name: str
    description: str | None
    model_config = {
        "from_attributes": True   # Pydantic v2
    }

class OrganisationRoleResponse(BaseModel):

    id: UUID
    name: str
    description: str | None
    model_config = {
        "from_attributes": True
    }