from pydantic import BaseModel

from app.enums.departement_status import DepartmentStatusEnum


class DepartmentCreate(BaseModel):
    departments : str
class DepartmentUpdate(BaseModel):
    departments : str
    department_status: DepartmentStatusEnum
class DepartmentDelete(BaseModel):
    departments : str
    department_status: DepartmentStatusEnum = DepartmentStatusEnum.DELETED

