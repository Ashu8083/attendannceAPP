import pytest

import uuid

from unittest.mock import MagicMock

from app.repo.AuthRepo import AuthRepo
from app.repo.RolePermissionRepo.organisation_role_permission import OrganisationLevelRolePermissionsRepo
from app.repo.RolePermissionRepo.system_role_permission_repo import SystemRoleRepo
from app.repo.attendance_record_repo import  AttendanceRepo
from app.repo.employee_repo import EmployeeRepo
from app.test.unit_test.fixture.employee_fixture import *
from app.test.unit_test.fixture.attendance_fixture import *
from app.test.unit_test.fixture.user_fixture import *
from app.test.unit_test.fixture.schema_fixture import *
from app.service.attendance_service import AttendanceService
from app.repo.user_repo import UserRepo
from app.service.auth_service import AuthService


@pytest.fixture
def attendance_repo():
    return MagicMock(spec=AttendanceRepo)

@pytest.fixture
def employee_repo():
    return MagicMock(spec=EmployeeRepo)
@pytest.fixture
def user_repo():
    return MagicMock(spec=UserRepo)
@pytest.fixture
def auth_repo():
    return MagicMock(spec=AuthRepo)
@pytest.fixture
def system_role_repo():
    return MagicMock(spec=SystemRoleRepo)
@pytest.fixture
def org_role_repo():
    return MagicMock(spec=OrganisationLevelRolePermissionsRepo)

@pytest.fixture
def attendance_evidence_repo():
    return MagicMock()

@pytest.fixture
def file_service():
    return MagicMock()

@pytest.fixture
def employee_face_repo():
    return MagicMock()

@pytest.fixture
def db_session():
    return MagicMock()

@pytest.fixture
def attendance_service(
        attendance_repo: AttendanceRepo,
        attendance_evidence_repo: MagicMock,
        employee_repo: EmployeeRepo,
        db_session: MagicMock,
        file_service: MagicMock,
        employee_face_repo: MagicMock,
):
    return AttendanceService(
        attendance_record_repo=attendance_repo,
        attendance_evidence_repo=attendance_evidence_repo,
        employee_repo=employee_repo,
        db=db_session,
        file_service=file_service,
        employee_face_repo=employee_face_repo,
    )

@pytest.fixture
def auth_service(
        auth_repo: AuthRepo,
        user_repo: UserRepo,
        system_role_repo: SystemRoleRepo,
        org_role_repo : OrganisationLevelRolePermissionsRepo):
    return AuthService(
        auth_repo=auth_repo,
        user_repo=user_repo,
        system_role_repo=system_role_repo,
        org_role_repo=org_role_repo
    )


@pytest.fixture
def employee_id():
    return str(uuid.uuid4())

@pytest.fixture
def attendance_id():
    return str(uuid.uuid4())

@pytest.fixture

def organisation_id():

    return uuid.uuid4()

@pytest.fixture
def user_id():
    return uuid.uuid4()
