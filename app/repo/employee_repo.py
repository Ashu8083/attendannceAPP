import uuid
from typing import Any
from uuid import UUID

from sqlalchemy.orm import Session, InstrumentedAttribute
from sqlalchemy import Select, select

from app.models import Employee
from app.models.employee_details_model import EmployeeDetails as ED, EmployeeDetails
from app.schemas.employee_schema import *
from app.models import Employee, EmployeeRoles


class EmployeeRepo:

    def __init__(self, db: Session):
        self.db = db

    def createEmployee(self, user_id: uuid.UUID, employeedata: CreateEmployee, organisation_id: uuid.UUID):
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
        self.db.flush()
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
        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
        return employee

#employee details by Code
    def get_employee_by_employee_code(self, organisation_id: uuid, employee_code: str) -> type[Employee] | None:

        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id,
                                                  Employee.employee_code == employee_code,
                                                  Employee.emplopyee_status == EmployeeStatus.ACTIVE).first()
        if not employee:

            raise ValueError("Employee code does not exist")
        return employee
    def get_employee_by_employee_id(self, employee_id: uuid.UUID,organisation_id : uuid.UUID) -> type[Employee] | None:
        return self.db.query(Employee).filter(Employee.employee_id == employee_id,
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
        return self.db.query(Employee).filter(Employee.department_name == department_name,
                                              Employee.organisation_id== organisation_id).all()

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
                raise
        return None

    def get_all_employee(self, organisation_id: uuid.UUID) -> list[type[Employee]]:
        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id).all()

        return employee


    def get_employee_id(self,organisation_id : uuid.UUID, employee_code: str):
        employee_id = self.db.query(Employee.id).filter(Employee.organisation_id == organisation_id ,
                                                        Employee.employee_code == employee_code).first()
        return employee_id
    def get_employee_by_user_id(self, user_id: uuid.UUID) -> type[Employee] | None:
        return self.db.query(Employee).filter(Employee.user_id == user_id).first()

    def assign_admin(self, organisation_id: uuid.UUID, employee_code: str, organisation_role_id:uuid.UUID) :
        smts = select(Employee).where(Employee.organisation_id == organisation_id,
                                             Employee.employee_code == employee_code)

        employee = self.db.execute(smts).scalar()
        employee.employee_roles.role_id = organisation_role_id

    def remove_admin(self, organisation_id: uuid.UUID, employee_code: uuid.UUID) :
        smts = select(Employee).where(Employee.organisation_id == organisation_id,
                                      Employee.employee_code == employee_code)
        employee = self.db.execute(smts).scalar()
        employee.employee_roles.role_id = None
