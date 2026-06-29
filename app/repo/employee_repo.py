import uuid
from typing import Any

from sqlalchemy.orm import Session, InstrumentedAttribute
from .user_repo import UserRepo
from app.models.user_models import User
from app.models.employee_models import Employee
from app.models.employee_details_model import EmployeeDetails as ED
from app.models.organisations import Organisation
from app.enums.employee_status import EmployeeStatus
from app.enums.role_enums import UserRole
from app.models.user_models import User
from app.schemas.employee_schema import *


class EmployeeRepo:

    def __init__(self, db: Session):
        self.db = db

    def createEmployee(self, user_id: uuid.UUID, employeedata: CreateEmployee, organisation_id: uuid.UUID):
        existing = self.get_employee_by_employee_code(organisation_id=organisation_id,
                                                      employee_code=employeedata.employee_code
                                                      )
        if existing:
            raise ValueError("Employee code already exists")

        employee = Employee(user_id=user_id, organisation_id=organisation_id, employee_code=employeedata.employee_code,
                            department=employeedata.department, join_date=employeedata.join_date, )
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

    def get_employee_by_employee_code(self, organisation_id: uuid, employee_code: str):

        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id,
                                                  Employee.employee_code == employee_code).first()
        if not employee:
            return None
        return employee

    def get_employee_by_name(self, employee_name: str):

        return (
            self.db.query(Employee)
            .join(Employee.employee_details)
            .filter(
                EmployeeDetails.full_name.ilike(f"%{employee_name}%")
            )
            .all()
        )

    def update_employee_details(
            self,
            employee_code: str,
            organisation_id: uuid,
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

    def employee_update_status(self, organisation_id: uuid, employee_code, employee_status: EmployeeStatusUpdate):
        employee = self.get_employee_by_employee_code(organisation_id=organisation_id, employee_code=employee_code)
        if employee:
            employee.employee_status = employee_status.status
            try:
                self.db.commit()
                self.db.refresh(employee)
            except Exception:
                self.db.rollback()
                raise
        return None

    def get_all_employee(self, organisation_id: str):
        employee = self.db.query(Employee).filter(Employee.organisation_id == organisation_id).all()

        return employee
