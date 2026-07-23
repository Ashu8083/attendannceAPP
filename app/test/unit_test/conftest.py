import pytest

import uuid

from unittest.mock import MagicMock
from app.repo.attendance_record_repo import  AttendanceRepo
from app.repo.employee_repo import EmployeeRepo
from app.test.unit_test.fixture.employee_fixture import *
from app.test.unit_test.fixture.attendance_fixture import *
from app.test.unit_test.fixture.schema_fixture import *
from app.service.attendance_service import AttendanceService


@pytest.fixture
def attendance_repo():
    return MagicMock(spec=AttendanceRepo)

@pytest.fixture
def employee_repo():
    return MagicMock(spec=EmployeeRepo)

@pytest.fixture
def attendance_service(
        attendance_repo: AttendanceRepo,
        employee_repo: EmployeeRepo
):
    return AttendanceService(
        attendacnce_record_repo=attendance_repo,
        employee_repo=employee_repo)

@pytest.fixture
def employee_id():
    return str(uuid.uuid4())

@pytest.fixture
def attendance_id():
    return str(uuid.uuid4())

@pytest.fixture

def organisation_id():

    return uuid.uuid4()