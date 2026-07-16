from app.repo.department_repo  import DepartmentRepo
from app.schemas.department_schema import  DepartmentCreate
import uuid


class DepartmentService:
    def __init__(self , department_repo: DepartmentRepo):
        self.department_repo = department_repo

    def get_all_department(self,organisation_id : uuid.UUID):
        return  self.department_repo.get_all_depertment(organisation_id)

    def get_department(self,department_name : str , organisation_id : uuid.UUID):
        return self.department_repo.get_department(department_name ,organisation_id)

    def create_department(self,departmentSchema : DepartmentCreate , organisation_id : uuid.UUID):

        department = self.department_repo.get_department(departmentSchema.name,organisation_id = organisation_id )
        if  department:
            raise Exception('Department already exists')
        return  self.department_repo.create_departments(departmentSchema,organisation_id)

    def update_department(self,department_id : uuid.UUID , department_name : str):

        return
    def soft_delete_department(self,department_name:str,organisation_id : uuid.UUID):
        department = self.department_repo.get_department(department_name,organisation_id = organisation_id )
        if not department:
            raise Exception('Department does not exist')
        return self.department_repo.soft_delete_department(department_name,organisation_id)

