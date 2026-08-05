import uuid
import numpy as np
from uuid import UUID
from sqlalchemy.orm import Session

from app.repo.employee_face_repo import EmployeeFaceRepo
from app.repo.employee_repo import EmployeeRepo
from app.exceptions.custom_exception import EmployeeNotFound
from app.face_model.mobilefacenet import MobileFaceNet
from app.face_model.service import FaceService
from app.service.employee_services import EmployeeService


class EmployeeFaceService:
    def __init__(
                self,
                db: Session,
                employee_repo: EmployeeRepo,
                employee_face_repo: EmployeeFaceRepo,
                face_service: FaceService,

        ):
            self.db = db
            self.employee_repo = employee_repo
            self.employee_face_repo = employee_face_repo
            self.face_service = face_service

    async def register_face(
            self,
            employee_id: UUID,
            organisation_id: UUID,
            image: np.ndarray,
    ):
        employee = self.employee_repo.check_employee_exist_by_employee_id(
            employee_id,
            organisation_id,
        )
        if not employee:
            raise EmployeeNotFound()
        embedding = self.face_service.extract_embedding(image)
        self.employee_face_repo.create_employee_face_record(
            employee.id,
            embedding.tolist(),
        )

    async def verify_face(
            self,
            employee_id: UUID,
            image: np.ndarray,
    ):
        face = self.employee_face_repo.get_by_employee_id(employee_id)
        if not face:
            raise
        result = self.face_service.verify(
            image=image,
            stored_embedding=np.asarray(
                face.embedding,
                dtype=np.float32,
            ),
        )
        return result
