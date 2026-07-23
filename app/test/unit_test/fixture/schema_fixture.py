import pytest
from unittest.mock import MagicMock

from app.schemas.attendance_schema import PunchInOutSchema


@pytest.fixture
def punch_schema():
    schema = MagicMock(spec=PunchInOutSchema)
    schema.employee_latitude = 20.123
    schema.employee_longitude = 85.456
    return schema