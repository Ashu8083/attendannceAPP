import uuid
import numpy as np
from uuid import UUID


from sqlalchemy.orm import Session
from fastapi import Request
from app.repo.employee_face_repo import EmployeeFaceRepo
from app.repo.employee_repo import EmployeeRepo
from app.face_model.face_embedding import extract_face_embedding_db
from app.face_model.face_matcher import arcface_match
from app.core.logging_config import logger


class EmployeeFaceService:
    def __init__(
                self,
                db: Session,
                employee_repo: EmployeeRepo,
                employee_face_repo: EmployeeFaceRepo,

        ):
            self.db = db
            self.employee_repo = employee_repo
            self.employee_face_repo = employee_face_repo

    async def register_employee_face(self,image_byte : bytes,request : Request):

        embedding = extract_face_embedding_db(image_byte)
        logger.info(f"employee id:")
        employee_id = self.employee_repo.check_employee_exist_by_employee_id(employee_id =request.state.auth.employee_id,organisation_id=request.state.auth.organisation_id)
        logger.info(f"employee id in request {request.state.auth.employee_id}")
        logger.info(f"organiastion id in request {request.state.auth.organisation_id}")

        if not employee_id:
            raise

        face_register = self.employee_face_repo.create_employee_face_record(employee_id=employee_id,embedding=embedding)
        if not face_register:
            raise

        return face_register

    async def verify_employee_face(self,request : Request,image_byte : bytes):
        employee_id = self.employee_repo.check_employee_exist_by_employee_id(employee_id = request.state.auth.employee_id,organisation_id=request.state.auth.organisation_id)
        if not employee_id:
            raise
        stored_embedding = self.employee_face_repo.get_employee_face_record(employee_id=employee_id)
        live_embedding = extract_face_embedding_db(image_byte)

        if not stored_embedding:
            raise

        face_similarity ,confidence = arcface_match(
                                                    stored_embedding,
                                                    live_embedding
                                                    )
        return {
            "face_similarity" : face_similarity,
            "confidence" : confidence

        }





    # async def register_face(
    #         self,
    #         employee_id: UUID,
    #         organisation_id: UUID,
    #         image: np.ndarray,
    # ):
    #     employee = self.employee_repo.check_employee_exist_by_employee_id(
    #         employee_id,
    #         organisation_id,
    #     )
    #     if not employee:
    #         raise EmployeeNotFound()
    #     embedding = self.face_service.extract_embedding(image)
    #     self.employee_face_repo.create_employee_face_record(
    #         employee.id,
    #         embedding.tolist(),
    #     )

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
