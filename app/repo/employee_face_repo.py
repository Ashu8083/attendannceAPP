from uuid import UUID
from sqlalchemy.orm import Session


from app.core.logging_config import logger
from app.models.employee_face_model import EmployeeFaceModel
from app.schemas.employee_schema import CreateEmployeeFaceRecord


class EmployeeFaceRepo:
    def __init__(self, db : Session):
        self.db = db

    def create_employee_face_record (self, employee_id : UUID , embedding  : list[float]) -> EmployeeFaceModel:

        employee_id = employee_id
        embedding = embedding

        employee_face_record = EmployeeFaceModel(
            employee_id = employee_id,
            embedding = embedding

        )
        try:
            self.db.add(employee_face_record)
            self.db.commit()
            self.db.refresh(employee_face_record)
        except Exception as e:
            logger.error(f"error while creating employee face record{e}")
            self.db.rollback()
            raise e

        return employee_face_record

    def get_employee_face_record (self, employee_id) :
        employee_face_record = self.db.query(EmployeeFaceModel).filter(EmployeeFaceModel.employee_id == employee_id).first()

        return employee_face_record

    def update_employee_face_record(self, employee_id : UUID ,employee_face_embedding : list[float]) -> EmployeeFaceModel :
        employee_face_record = self.db.query(EmployeeFaceModel).filter(EmployeeFaceModel.employee_id == employee_id).first()

        employee_face_record.embedding = employee_face_embedding
        try:
            self.db.commit()
            self.db.refresh(employee_face_record)
            return employee_face_record
        except Exception as e:
            logger.error(f"error while updating employee face record{e}")
            self.db.rollback()
            raise e




