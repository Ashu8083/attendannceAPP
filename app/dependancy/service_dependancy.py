from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repo.AuthRepo import AuthRepo
from app.repo.attendance_record_repo import AttendanceRepo
from app.repo.department_repo import DepartmentRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.role_repo import RoleRepo
from app.repo.user_repo import UserRepo
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_repo import UserRepo
from app.service.attendance_service import AttendanceService
from app.service.department_service import DepartmentService
from app.service.organisation_service import OrganisationService
from app.service.role_services.role_creation_service import RoleService
from app.service.user_service import UserService
from app.service.employee_services import EmployeeService
from app.service.auth_service import AuthService

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
    return EmployeeService(employee_repo=employee_repo,user_repo= ueser_repo)


def get_attendance_service(
        db :Session = Depends(get_db)
):
    attendance_repo = AttendanceRepo(db)
    employee_repo = EmployeeRepo(db)
    return AttendanceService(attendance_repo,employee_repo)

def get_role_service(
        db: Session= Depends(get_db)
):
    role_repo = RoleRepo(db)
    return RoleService(role_repo)

def get_department_service(
        db: Session = Depends(get_db),
):
    department_repo = DepartmentRepo(db)
    return DepartmentService(department_repo)

def get_auth_service(
        db: Session = Depends(get_db),
):
    auth_repo = AuthRepo(db)
    user_repo = UserRepo(db)
    return AuthService(auth_repo, user_repo)
