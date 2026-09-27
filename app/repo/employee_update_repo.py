from typing import List
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.employee_models import Employee

from app.schemas.employee_schema_update import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeSearchFilter,
    FillEmployeeDetails,
    EmployeeDetailsUpdate,
)
from db.UnitOfWork import UnitOfWork
from models import EmployeeDetails, User


class EmployeeRepo:
    def __init__(self, db : Session):
        self.db = db


    def create_employee(self, employee : Employee) -> Employee:
        self.db.add(employee)
        self.db.flush()
        self.db.refresh(employee)
        return employee

    def update_employee(self,data : EmployeeUpdate , employee : Employee) -> Employee:

        for field,value in data.model_dump().items():
            setattr(employee,field,value)

        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def create_employee_details(self,employee_details : EmployeeDetails ) -> EmployeeDetails:
        self.db.add(employee_details)
        self.db.flush()
        self.db.refresh(employee_details)
        return employee_details

    def update_employee_details(
            self,
            employee_details: EmployeeDetails,
            details_update: EmployeeDetailsUpdate
    ) -> EmployeeDetails:
        for field, value in details_update.model_dump(exclude_unset=True).items():
            setattr(employee_details, field, value)
        self.db.add(employee_details)
        self.db.commit()
        self.db.refresh(employee_details)
        return employee_details


    def employee_search_filter(
            self,
            employee_search: EmployeeSearchFilter,
            organisation_id: UUID
    ) -> List[Employee]:

        query = self.db.query(Employee).filter(
            Employee.organisation_id == organisation_id
        )

        # Search by User.full_name
        if employee_search.full_name:
            query = (
                query
                .join(Employee.user)
                .filter(
                    User.full_name.ilike(
                        f"%{employee_search.full_name}%"
                    )
                )
            )

        # Department
        if employee_search.department_id:
            query = query.filter(
                Employee.department_id == employee_search.department_id
            )

        # Team
        if employee_search.team_id:
            query = query.filter(
                Employee.team_id == employee_search.team_id
            )

        # Organisation Branch
        if employee_search.organisation_branch_id:
            query = query.filter(
                Employee.organisation_branch_id
                == employee_search.organisation_branch_id
            )

        # Supervisor
        if employee_search.supervisor:
            query = query.filter(
                Employee.supervisor == employee_search.supervisor
            )

        # Employee Code
        if employee_search.employee_code:
            query = query.filter(
                Employee.employee_code == employee_search.employee_code
            )
        return query.all()


    def get_employee_by_id(self, employee_id : UUID) -> Employee:
        employee = self.db.query(Employee).filter(
            Employee.id == employee_id
        )
        return employee.first()

    def check_employee_exit(self,employee_id : UUID) -> UUID:
        employee = self.db.query(Employee.id).filter(
            Employee.id == employee_id
        ).first()

        return employee

