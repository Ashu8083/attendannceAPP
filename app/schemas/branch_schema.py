import uuid

from pydantic import BaseModel


class UpdateBranch(BaseModel):
    branch_name : str | None = None
    address : str | None = None
    city : str | None = None
    state : str | None = None
    zip_code : str | None = None
    longitude : float | None = None
    latitude : float | None = None
    geofencing: int | None = None
    total_number_paid_leaves : int | None = None

class SearchFilters(BaseModel):
    branch_name : str | None = None
    organisation_id : uuid.UUID | None = None
    status : None = None