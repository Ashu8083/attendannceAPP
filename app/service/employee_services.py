import uuid
from logging import raiseExceptions
from urllib import request

from redis.commands.search.reducers import random_sample
from app.db.UnitOfWork import UnitOfWork
from app.repo.user_repo import UserRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.organisation_repo import OrganisationRepo
from app.schemas.employee_schema import *
from app.exceptions.custom_exception import (
    UserNotFound,
    EmailAlreadyExists, EmployeeAlreadyExists, EmployeeNotFound,
    OraganisationNotFound
)
from app.email.service import email_service
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.models import OrganisationRoles
from sqlalchemy.orm import Session
from app.repo.department_repo import DepartmentRepo
from app.repo.employee_repo import EmployeeRepo


class EmployeeService:
    def __init__(self, employee_repo : EmployeeRepo, user_repo : UserRepo, organisation_repo :OrganisationRepo, organisation_role_repo : OrganisationLevelRolePermissionsRepo, db:Session, department_repo : DepartmentRepo) :
        self.employeeRepo = employee_repo
        self.userRepo = user_repo
        self.organisation_repo = organisation_repo
        self.organisation_role_repo = organisation_role_repo
        self.department_repo = department_repo
        self.db = db

    def generate_employee_code_by_organisation_id(self,oranisation_id :uuid) -> str:
        organisation_id = self.organisation_repo.check_organisation(oranisation_id)
        if not organisation_id :
            raise OraganisationNotFound
        return self.employeeRepo.generate_employee_code(organisation_id)

    def generate_employee_code(self,organisation_code : str) -> str:
        organisation_id = self.organisation_repo.get_organisation_id_by_organisation_code(organisation_code)
        if not organisation_id :
            raise OraganisationNotFound
        return self.employeeRepo.generate_employee_code(organisation_id)

    def add_existing_user_to_organisation(self,organisation_code :str,user_email:EmailStr, employee_detail_schema : CreateEmployeeDetails ,):

        organisation_id = self.organisation_repo.get_organisation_id_by_organisation_code(organisation_code)
        if not organisation_id :
            raise OraganisationNotFound


        user = self.userRepo.get_user_by_email(user_email= user_email)
        if not user:
            raise UserNotFound(user_email)
        if user.employee :
            raise EmployeeAlreadyExists

        employee_code = self.employeeRepo.generate_employee_code(organisation_id= organisation_id)
        create_employee = CreateExistingEmployee(
            full_name = user.full_name,
            email = user.email,
            employee_code = employee_code,
            employee_status= EmployeeStatus.ACTIVE
        )

        with UnitOfWork(self.db):
            employee = self.employeeRepo.add_user_to_organisation(create_employee=create_employee,organisation_id=organisation_id,user_id=user.id)

            employee_details = self.employeeRepo.add_employee_details(employee_details_schema =employee_detail_schema,employee_id = employee.id ,user_full_name= user.full_name)

        return {"employee":employee,
                "employee_details":employee_details}


    # ====================================================================================================================
    #          Employee & Admin Create Service
    # ====================================================================================================================

    async def create_employee_service(self,organisation_id : uuid.UUID,employee_schema : CreateEmployee):

        user = self.userRepo.get_user_by_email(user_email= employee_schema.email)
        if  user:
            raise EmailAlreadyExists

        employee = self.employeeRepo.get_employee_by_user_id(user.id)
        if employee:
            raise EmployeeAlreadyExists
        department_id = self.department_repo.department_id(organisation_id=organisation_id,department_name=employee_schema.department)
        employee_schema.department = department_id

        with UnitOfWork(self.db):

            user = self.userRepo.create_user_as_employee(full_name = employee_schema.full_name, email = employee_schema.email, organisation_id = organisation_id)
            employee = self.employeeRepo.createEmployee(user_id= user.id, employeedata= employee_schema, organisation_id= organisation_id)

            if not employee :
                raise ValueError("Employee Creation Error")
            await email_service.send_welcome_email(email=user.email)

            return employee

    async def create_admin_service(self,organisation_code : str,admin_schema : CreateAdminEmployee):
        organisation_id = self.organisation_repo.get_organisation_id_by_organisation_code(organisation_code)
        if not organisation_id :
            raise OraganisationNotFound
        user = self.userRepo.get_user_by_email(user_email= admin_schema.email)
        if user:
            raise EmailAlreadyExists
        with UnitOfWork(self.db):
            user = self.userRepo.create_user_as_employee(full_name=admin_schema.full_name,
                                                         email=admin_schema.email, organisation_id=organisation_id)

            organisation_admin_role = self.organisation_role_repo.create_role()
            admin = self.employeeRepo.create_employee_admin(user_id=user.id, admin_schema=admin_schema,
                                                        organisation_id=organisation_id)
            if not admin:
                raise ValueError("Employee Creation Error")
            await email_service.send_welcome_email(email=user.email)

            return admin



    def create_employee_service_by_organisation_code(self,organisation_code : str,employee_schema : CreateEmployee):

        organisation_id = self.organisation_repo.get_organisation_by_code(organisation_code)

        user = self.userRepo.get_user_by_email(user_email= employee_schema.email)
        
        if  user:
            raise EmailAlreadyExists

        user = self.userRepo.create_user_as_employee(full_name = employee_schema.full_name, email = employee_schema.email, organisation_id = organisation_id)

        employee = self.employeeRepo.createEmployee(user_id= user.id, employeedata= employee_schema, organisation_id= organisation_id)
        if not employee :
            raise ValueError("Employee Creation Error")
        return employee

    # ====================================================================================================================
    #           Employee Update Service
    # ====================================================================================================================

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

    # ====================================================================================================================
    #           All The Employee Get Method
    # ====================================================================================================================

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

    def get_all_employee_service(self,organisation_id : uuid.UUID):

        return self.employeeRepo.get_all_employee(organisation_id=organisation_id)

    # ====================================================================================================================
    #           Admin Assign  and Remove
    # ====================================================================================================================

    def assign_admin(self, organisation_code : str,employee_code : str):
        organisation_id = self.organisation_repo.get_organisation_by_code(organisation_code)
        if not organisation_id :
            raise
        employee = self.employeeRepo.get_employee_by_employee_code(organisation_id= organisation_id, employee_code= employee_code)
        if not employee :
            raise EmployeeNotFound
        
        organisation_role_id = self.organisation_role_repo.get_role(organisation_id= organisation_id, role_name= "ADMIN")
        new_admin = self.employeeRepo.assign_admin(employee_code,organisation_id,organisation_role_id=organisation_role_id)
        return new_admin


    def remove_admin(self,employee_code : str, organisation_code : str):

        organisation_id = self.organisation_repo.get_organisation_by_code(organisation_code)
        if not organisation_id :
            raise
        employee_id = self.employeeRepo.check_existing_employee(employee_code,organisation_id)
        if not employee_id :
            raise EmployeeNotFound

        return self.employeeRepo.remove_admin(employee_code=employee_code ,organisation_id= organisation_id)

##=================================================================================================
#======================================= Assign Role ========================================
#=================================================================================================

    def assign_role_to_employee(
        self,
        employee_code : str,
        organisation_id : UUID,
        organisation_role_name : str,

    ):

        organisation_role_id = self.organisation_role_repo.get_role(organisation_id= organisation_id, role_name= organisation_role_name)
        if not organisation_role_id :
            raise
        employee = self.employeeRepo.get_employee_by_employee_code(employee_code)
        if not employee :
            raise
        self.employeeRepo.assign_role_repo(organisation_id= organisation_id,employee_code= employee_code ,organisation_role_id= organisation_role_id)

        return employee



