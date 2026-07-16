from typing import Optional
import uuid
from pydantic import BaseModel
from app.enums.permission_scop import PermissionScopEnum,PermissionScopEnumUpdate


class CreateRole(BaseModel):
    name: str
    description :str

class CreatePermision(BaseModel):
    name: str
    description : str
    scope : PermissionScopEnumUpdate
    assignable : bool

    
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
     permissions : list[str]