from uuid import UUID
from pydantic import BaseModel


from pydantic import BaseModel, Field

class AuthContext(BaseModel):
    user_id: UUID
    organisation_id: UUID
    system_role: str
    employee_id: UUID | None = None
    permissions: set[str] = Field(default_factory=set)