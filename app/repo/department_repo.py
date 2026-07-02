import uuid
from typing import List

from mako.util import restore__ast
from sqlalchemy.orm  import Session

from app.enums.departement_status import DepartmentStatusEnum
from app.models import DepartmentModel
from app.schemas.department_schema import DepartmentCreate
from app.models.department_model import DepartmentModel
from app.schemas.organisation_schema import OrganisationUpdateStatus


class DepartmentRepo:
    def __init__(self,db : Session):
        self.db = db
    def create_departments(self , DepartmentCreateSchema : DepartmentCreate , organisation_id : uuid.UUID ):
        department = DepartmentModel(
                    name = DepartmentCreateSchema.name,
                    organisation_id = organisation_id,
                    department_status =  DepartmentStatusEnum.ACTIVATE

        )
        try:
            self.db.add(department)
            self.db.commit()
            self.db.refresh(department)
        except Exception as e:
            self.db.rollback()
            raise e
        return department


    def get_all_depertment (self, organisation_id : uuid.UUID) -> List[type[DepartmentModel]]:
        departments =self.db.query(DepartmentModel).filter(DepartmentModel.organisation_id == organisation_id).all()

        return departments

    def department_id (self,organisation_id : uuid.UUID, department_name : str) -> type[DepartmentModel] | None:

        return self.db.query(DepartmentModel).filter(DepartmentModel.name == department_name,
                                                     DepartmentModel.organisation_id == organisation_id).one_or_none()

    def get_department(self, department_name : str , organisation_id : uuid.UUID) -> type[DepartmentModel] | None:
        return self.db.query(DepartmentModel).filter(DepartmentModel.name == department_name,
                                                     DepartmentModel.organisation_id == organisation_id).one_or_none()

    def remove_department_(self,department_name : str , organisation_id : uuid.UUID):
        department  =self.db.query(DepartmentModel).filter(DepartmentModel.name == department_name,
                                                            DepartmentModel.organisation_id == organisation_id).one_or_none()

        try:
            self.db.delete(department)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e
        return department

    def suspend_department(self):
        return
    def soft_delete_department(self,department_name : str , organisation_id : uuid.UUID):
        department = self.db.query(DepartmentModel).filter(DepartmentModel.name == department_name,
                                                           DepartmentModel.organisation_id == organisation_id).first()

        department = department.department_status = DepartmentStatusEnum.DELETED
        try :
             self.db.commit()
             self.db.refresh(department)
        except Exception as e:
            self.db.rollback()
            raise e
    def update_department(self):
        return