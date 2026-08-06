from fastapi import Depends
from sqlalchemy.orm import Session


from app.db.database import get_db
from app.repo.AuthRepo import AuthRepo
from app.repo.attendance_record_repo import AttendanceRepo
from app.repo.department_repo import DepartmentRepo
from app.repo.employee_repo import EmployeeRepo
from app.repo.leave_repo import LeaveRepo
# from repo.RolePermissionRepo.role_repo import
from app.repo.organisation_repo import OrganisationRepo
from app.repo.user_repo import UserRepo
from app.service.attendance_service import AttendanceService
from app.service.department_service import DepartmentService
from app.service.leave_service import LeaveService
from app.service.organisation_service import OrganisationService
from app.service.role_services.system_role_permission_service import SystemRoleRepo, SystemRoleService
#from app.service.role_services.organisation_role_permission_service import
from app.service.user_service import UserService
from app.service.employee_services import EmployeeService
from app.service.auth_service import AuthService
from app.repo.user_device_repo import  UserDeviceDetailRepo
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.service.role_services.permission_service import RoleService
from app.repo.RolePermissionRepo.role_repo import RolePermissionRepo
from app.service.role_services.defult_role_permission import DefaultRolePermissionService
from app.repo.token_repo import TokenRepo
from app.service.user_device_service import UserDeviceAndTokenService
from app.repo.employee_face_repo import EmployeeFaceRepo
from app.service.employee_face_service import EmployeeFaceService


def get_organaistion_service(
    db: Session = Depends(get_db)
):
    repo = OrganisationRepo(db)
    organaistion_deful_role = DefaultRolePermissionService(db)
    return OrganisationService(repo,organaistion_deful_role)

def get_user_service(
        db: Session = Depends(get_db)
):
    user_repo = UserRepo(db)
    organisation_repo = OrganisationRepo(db)
    system_role_repo = SystemRoleRepo(db)
    db = db
    return UserService(user_repo,organisation_repo,system_role_repo,db= db)

def get_employee_service(
        db: Session = Depends(get_db)
):
    employee_repo = EmployeeRepo(db)
    user_repo = UserRepo(db)
    organisation_repo = OrganisationRepo(db)
    organisation_role_repo = OrganisationLevelRolePermissionsRepo(db)
    department_repo = DepartmentRepo(db)

    return EmployeeService(employee_repo=employee_repo,user_repo= user_repo,organisation_repo= organisation_repo,db = db,organisation_role_repo = organisation_role_repo,department_repo=department_repo)


def get_attendance_service(
        db :Session = Depends(get_db)
):
    attendance_repo = AttendanceRepo(db)
    employee_repo = EmployeeRepo(db)
    employee_face_repo = EmployeeFaceRepo(db)
    return AttendanceService(attendance_repo,employee_repo,employee_face_repo)
#
# def get_role_service(
#         db: Session= Depends(get_db)
# ):
#     role_repo = RolePermissionRepo(db)
#     return RoleService(role_repo)

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
    user_device_repo = UserDeviceDetailRepo(db)
    token_repo = TokenRepo(db)
    #employee_repo = EmployeeRepo(db)
    # role_permission_repo = RolePermissionRepo(db)
    organisation_role = OrganisationLevelRolePermissionsRepo(db)
    system_role = SystemRoleRepo(db)
    user_device_and_token_service = UserDeviceAndTokenService(token_repo = token_repo , user_device_repo= user_device_repo)

    return AuthService(db,auth_repo, user_repo,system_role,org_role_repo=organisation_role,user_device_and_token_service =user_device_and_token_service  )


def get_leave_service(
        db: Session = Depends(get_db),
):
    leave_repo = LeaveRepo(db)
    employee_repo = EmployeeRepo(db)
    return LeaveService(leave_repo = leave_repo, employee_repo= employee_repo)

def get_role_system_role_service(
        db: Session = Depends(get_db),
):
    system_role_repo = SystemRoleRepo(db)
    user_repo = UserRepo(db)
    return SystemRoleService(system_role_repo,user_repo)
def get_organisation_role_service(
        db: Session = Depends(get_db),
):
    organisation_repo = OrganisationRepo(db)
    return OrganisationService(organisation_repo)
def get_permission_service(
        db: Session = Depends(get_db),
):
    permission_repo = RolePermissionRepo(db)
    return RoleService(permission_repo)

def get_employee_face_service(
        db: Session = Depends(get_db),
):
    employee_repo = EmployeeRepo(db)
    employee_face_repo = EmployeeFaceRepo(db)
    return EmployeeFaceService(db = db,
                               employee_repo=employee_repo,
                               employee_face_repo=employee_face_repo,

                               )

def get_user_device_token_service(
        db: Session = Depends(get_db),
):
    user_device_repo = UserDeviceDetailRepo(db)
    token_repo = TokenRepo(db)
    user_device_token_service = UserDeviceAndTokenService(user_device_repo,token_repo)
    return user_device_token_service