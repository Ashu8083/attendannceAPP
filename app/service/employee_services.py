import uuid


from app.repo.user_repo import UserRepo
from app.repo.employee_repo import EmployeeRepo
from app.schemas.employee_schema import *

class EmployeeService():
    def __init__(self,employeeRepo : EmployeeRepo,userRepo : UserRepo):
        self.employeeRepo = employeeRepo
        self.userRepo = userRepo
    
    def createEmployee_service(self,organisation_id : uuid,employeeSchema : CreateEmployee):

        user = self.userRepo.create_user_as_employee(full_name = employeeSchema.full_name,emial = employeeSchema.email,organisation_id = organisation_id)
        if not user:
            raise ValueError("User not found ")
        employee = self.employeeRepo.createEmployee(user_id= user.id,employeedata= employeeSchema)
        if not employee :
            raise ValueError("Employee Creation Error")
        return employee



    def update_employee_service(self,organisation_id : uuid , employeeDetailsSchema : EmployeeDetailsUpdate,employee_code : str):

        exsting_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id= organisation_id,employee_code= employee_code)
        if not exsting_employee : 
            raise ValueError("Emoloyee not exist")
        try:
            updated_employee = self.employeeRepo.update_employee_details(employeeDetailsSchema,organisation_id)
        except : 
            raise ValueError("something went wrong")
        
        return updated_employee
        
    def update_employee_status_service(self,organisation_id : uuid ,employee_code :str ,employee_status_update : EmployeeStatusUpdate):

        exsting_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id= organisation_id,employee_code= employee_code)
        if not exsting_employee : 
            raise ValueError("Emoloyee not exist")
        try :
            update_employee_status = self.employeeRepo.employee_update_status(employee_status_update,organisation_id)
        except:
            raise ValueError("Something went wrong")
    def get_employee_service(self,organisation_id : uuid, employee_code : str):
        existing_employee = self.employeeRepo.get_employee_by_employee_code(organisation_id,employee_code)
        if not existing_employee: 
            raise ValueError ("Employee not found")
        return existing_employee
        
    def delete_employee_service():
        return
    def get_all_employee_service(self,organisation_id):

        return self.employeeRepo.get_all_employee()
