import uuid


from app.repo.user_repo import UserRepo
from app.repo.employee_repo import EmployeeRepo
from app.schemas.employee_schema import *
from app.service.face_services.InsightFaceService import InsightFaceService

class EmployeeService:
    def __init__(self,employee_repo : EmployeeRepo,user_repo : UserRepo,face_embending : InsightFaceService):
        self.employeeRepo = employee_repo
        self.userRepo = user_repo
        self.face_embending = face_embending
    
    def create_employee_service(self,organisation_id : uuid.UUID,employee_schema : CreateEmployee):

        
        user = self.userRepo.get_user_by_email(user_email= employee_schema.email)
        if not user:
            user = self.userRepo.create_user_as_employee(full_name = employee_schema.full_name, email = employee_schema.email, organisation_id = organisation_id)
        employee = self.employeeRepo.createEmployee(user_id= user.id, employeedata= employee_schema, organisation_id= organisation_id)
        if not employee :
            raise ValueError("Employee Creation Error")
        return employee



    def update_employee_service(self,organisation_id : uuid.UUID , employee_details_schema : EmployeeDetailsUpdate,employee_code : str):

        existing_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id= organisation_id, employee_code= employee_code)
        if not existing_employee :
            raise ValueError("Emoloyee not exist")
        try:
            updated_employee = self.employeeRepo.update_employee_details(employee_details_schema,organisation_id)
        except : 
            raise ValueError("something went wrong")
        
        return updated_employee
        
    def update_employee_status_service(self,organisation_id : uuid.UUID ,employee_code :str ,employee_status_update : EmployeeStatusUpdate):

        existing_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id= organisation_id, employee_code= employee_code)
        if not existing_employee :
            raise ValueError("Employee not exist")
        try :
            update_employee_status = self.employeeRepo.employee_update_status(employee_status_update,organisation_id)
        except:
            raise ValueError("Something went wrong")
        return update_employee_status

    def get_employee_service(self,organisation_id : uuid.UUID, employee_code : uuid.UUID):
        existing_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id,employee_code)
        if not existing_employee: 
            raise ValueError ("Employee not found")
        return existing_employee
    def get_employee_by_empID_service(self,organisation_id : uuid.UUID, employee_id : uuid.UUID):

        employee = self.employeeRepo.get_employee_by_employee_id(organisation_id,employee_id)
        if not employee :
            raise ValueError ("Employee not found")
        return employee

    def delete_employee_service(self):
        return
    def get_all_employee_service(self,organisation_id : uuid.UUID):

        return self.employeeRepo.get_all_employee(organisation_id=organisation_id)

    def register_face_id(self,image_bytes : bytes,employee_code: str,organisation_id : uuid.UUID):
        # embende the face id then store 
        embedding = self.face_embending.generate_embedding(image_bytes)
        if not embedding: 
            raise
        employee= self.employeeRepo.get_employee_by_employee_code(employee_code,organisation_id=organisation_id)
        if not employee: 
            raise

        self.employeeRepo.storeFaceEmbedding(embedding.tolist())
        return

    def update_face_id(self):
        return
