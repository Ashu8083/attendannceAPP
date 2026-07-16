from pydantic import BaseModel
from typing import List

from app.enums.departement_status import DepartmentStatusEnum


class DepartmentCreate(BaseModel):
    name : str
   
class DepartmentResponse(BaseModel):
    name : str
    derpartment_status : DepartmentStatusEnum

    model_config = {
        "from_attributes": True
    }

class DepartmentUpdate(BaseModel):
    departments : str
    department_status: DepartmentStatusEnum
class DepartmentDelete(BaseModel):
    departments : str
    department_status: DepartmentStatusEnum = DepartmentStatusEnum.DELETED

class ListOfDepartment(BaseModel):
    
    departments : List[DepartmentResponse]
