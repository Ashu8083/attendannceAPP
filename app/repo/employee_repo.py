import uuid
from sqlite3 import IntegrityError
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy import Select, select, func

from app.models import Employee
from app.models.employee_details_model import EmployeeDetails as ED, EmployeeDetails
from app.schemas.employee_schema import *
from app.models import Employee, EmployeeRoles
from app.core.logging_config import logger



class EmployeeRepo:

    def __init__(self, db: Session):
        self.db = db

    # ====================================================================================================================
    #         Generate Employee Code
    # ====================================================================================================================

    def generate_employee_code(self,organisation_id:uuid.UUID) -> str:
        stmt = (
            select(func.max(Employee.employee_code))
            .where(Employee.organisation_id == organisation_id)
        )
        last_code = self.db.scalar(stmt)
        if last_code is None:
            return "EMP001"
        number = int(last_code[3:]) + 1

        return f"EMP{number:03d}"

    # ====================================================================================================================
    #        Check Employee Exist
    # ====================================================================================================================

    def check_existing_employee(self,employee_code:str,organisation_id : uuid.UUID) -> type[UUID] | None:
        return self.db.query(Employee.id).filter(Employee.employee_code == employee_code,
                                                 Employee.organisation_id == organisation_id).first()

    # ====================================================================================================================
    #         Employee Create
    # ====================================================================================================================

    def createEmployee(self, user_id: uuid.UUID, employeedata: CreateEmployee, organisation_id: uuid.UUID):
        logger.info(f"Trying to create Employee ")
        existing = self.get_employee_by_employee_code(organisation_id=organisation_id,
                                                      employee_code=employeedata.employee_code
                                                      )

        if existing:
            raise ValueError("Employee code already exists")

        employee = Employee(user_id=user_id,
                            organisation_id=organisation_id,
                            employee_code=employeedata.employee_code,
                            department=employeedata.department,
                            join_date=employeedata.join_date,
                            )
        self.db.add(employee)

        logger.info(f"Employee with  employee code {employeedata.employee_code} added belong to organisation {organisation_id} ")

        employee_details = ED(
            employee_id=employee.id,
            full_name=employeedata.full_name,
            dob=employeedata.dob,
            gender=employeedata.gender,
            marital_status=employeedata.marital_status,
            address=employeedata.address,
            city=employeedata.city,
            state=employeedata.state,
        )
        self.db.add(employee_details)

        logger.info(f"Employee details add for  {employee_details.employee_code} ")
        self.db.flush()

        return employee

    def create_employee_admin(self,user_id :uuid.UUID ,organisation_id: uuid.UUID,admin_schema: CreateAdminEmployee | None) -> type[Employee] | None:
        logger.info(f"Trying to create Admin for organisation {organisation_id}")
        employee_record = Employee(
            user_id=user_id,
            organisation_id=organisation_id,
            employee_code=admin_schema.employee_code,
            department=admin_schema.department,
            join_date=admin_schema.join_date,

        )
        return employee_record

    def add_employee_details(self,user_full_name : str,employee_details_schema : CreateEmployeeDetails, employee_id : UUID) -> type[EmployeeDetails] | None:
        logger.info(f"Trying to add Employee details ")
        employee_details = ED(
            employee_id=employee_id,
            full_name=user_full_name,
            dob=employee_details_schema.dob,
            gender=employee_details_schema.gender,
            marital_status=employee_details_schema.marital_status,
            address=employee_details_schema.address,
            city=employee_details_schema.city,
            state=employee_details_schema.state,

        )
        self.db.add(employee_details)
        logger.info(f"Employee details add for")
        self.db.flush()
        return employee_details



    def add_user_to_organisation(self, organisation_id: uuid.UUID, user_id: uuid.UUID,create_employee:CreateExistingEmployee | None) -> type[Employee] | None:
        logger.info(f"Trying to add user to organisation {organisation_id}")
        employee_record = Employee(
            user_id=user_id,
            organisation_id=organisation_id,
            employee_code=create_employee.employee_code,

        )
        self.db.add(employee_record)
        self.db.flush()

        return employee_record
    #employee details by Code
    # ====================================================================================================================
    #           Employee  fetch method
    # ====================================================================================================================
    def get_employee_by_employee_code(self, organisation_id: uuid, employee_code: str) -> type[Employee] | None:

        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id,
                                                  Employee.employee_code == employee_code,
                                                  Employee.employee_status == EmployeeStatus.ACTIVE).first()
        if not employee:
            raise ValueError("Employee code does not exist")

        return employee


    def get_employee_by_employee_id(self, employee_id: uuid.UUID,organisation_id : uuid.UUID) -> type[Employee] | None:
        return self.db.query(Employee).filter(Employee.id == employee_id,
                                              Employee.organisation_id == organisation_id).first()

    def get_employee_by_name(self, employee_name: str):
        return (
            self.db.query(Employee)
            .join(Employee.employee_details)
            .filter(
                EmployeeDetails.full_name.ilike(f"%{employee_name}%")
            )
            .all()
        )
    def get_employee_by_department_name(self,department_name: str,organisation_id : uuid.UUID ) -> list[type[Employee]] | None:
        return self.db.query(Employee).filter(Employee.department == department_name,
                                              Employee.organisation_id== organisation_id).all()



    def get_all_employee(self, organisation_id: uuid.UUID) -> list[type[Employee]]:
        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id).all()
        return employee


    def get_employee_id(self,organisation_id : uuid.UUID, employee_code: str):
        employee_id = self.db.query(Employee.id).filter(Employee.organisation_id == organisation_id ,
                                                        Employee.employee_code == employee_code).scalar()
        return employee_id
    def get_employee_by_user_id(self, user_id: uuid.UUID) -> type[Employee] | None:
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()

    # ====================================================================================================================
    #           Update The Employee Details and Status
    # ====================================================================================================================

    def update_employee_details(
            self,
            employee_code: str,
            organisation_id: uuid.UUID,
            employee_details: EmployeeDetailsUpdate
    ) -> InstrumentedAttribute[Any] | None:

        employee = self.get_employee_by_employee_code(organisation_id, employee_code)

        if not employee:
            return None

        details = employee.employee_details

        for field, value in employee_details.model_dump(exclude_unset=True).items():
            setattr(details, field, value)
        try:
            self.db.commit()
            self.db.refresh(details)
        except Exception:
            self.db.rollback()
            logger.exception(f"Update employee details failed for {employee_code}")
            raise

        return details

    def employee_update_status(self, organisation_id: uuid.UUID, employee_code, employee_status: EmployeeStatusUpdate):
        employee = self.get_employee_by_employee_code(organisation_id=organisation_id, employee_code=employee_code)
        if employee:
            employee.employee_status = employee_status.employee_status
            try:
                self.db.commit()
                self.db.refresh(employee)
            except Exception:
                self.db.rollback()
                logger.exception(f"Update employee status failed for {employee_code}")
                raise
        return None

    # ====================================================================================================================
    #           Admin Assign to employee
    # ====================================================================================================================

    def assign_admin(self, organisation_id: uuid.UUID, employee_code: str, organisation_role_id:uuid.UUID) :
        stmt = select(Employee).where(Employee.organisation_id == organisation_id,
                                             Employee.employee_code == employee_code)

        employee = self.db.execute(stmt).scalar()
        employee.employee_roles.role_id = organisation_role_id
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def remove_admin(self, organisation_id: uuid.UUID, employee_code: uuid.UUID) :
        stmt = select(Employee).where(Employee.organisation_id == organisation_id,
                                      Employee.employee_code == employee_code)
        employee = self.db.execute(stmt).scalar()
        employee.employee_roles.role_id = None
        employee.save()
        self.db.commit()
        self.db.refresh(employee)
        return employee
