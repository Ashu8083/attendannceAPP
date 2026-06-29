from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repo.employee_repo import EmployeeRepo
from app.repo.user_repo import UserRepo
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_repo import UserRepo
from app.service.organisation_service import OrganisationService
from app.service.user_service import UserService
from app.service.employee_services import EmployeeService

def get_organaistion_service(
    db: Session = Depends(get_db)
):
    repo = OrganisationRepo(db)
    return OrganisationService(repo)

def get_user_service(
        db: Session = Depends(get_db)
):
    user_repo = UserRepo(db)
    organisation_repo = OrganisationRepo(db)
    return UserService(user_repo,organisation_repo)

def get_employee_service(
        db: Session = Depends(get_db)
):
    employee_repo = EmployeeRepo(db)
    ueser_repo = UserRepo(db)
    return EmployeeService(employeeRepo=employee_repo,userRepo= ueser_repo)

