import uuid

import pytest
from unittest.mock import MagicMock

from app.enums.work_mode import WorkMode



@pytest.fixture
def employee():
    employee = MagicMock()
    employee.id = uuid.uuid4()
    employee.name = "testName testsurname"
    employee.employee_code = "EMP001"
    employee.work_mode = WorkMode.WFO

    organisation = MagicMock()
    organisation.office_latitude = 20.123
    organisation.office_longitude = 85.456
    organisation.allowed_rediuse = 100

    employee.organisation = organisation
    return employee
