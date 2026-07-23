import uuid
from unittest.mock import MagicMock

import pytest

from app.enums.employee_status import EmployeeStatus
from app.enums.scops import AccountType


@pytest.fixture
def user():
    user = MagicMock()
    user.id = uuid.uuid4()
    user.email = "test_email"
    user.account_type = AccountType.ORGANISATION
    user.organisation_id = uuid.uuid4()


    employee = MagicMock()
    employee.emplopyee_status = EmployeeStatus.ACTIVE
    employee.id = uuid.uuid4()
    employee_role = MagicMock()
    organisation_permissions1 = MagicMock()
    organisation_permissions2 = MagicMock()
    permission1 = MagicMock()
    permission1.name = "employee.create"
    permission2 = MagicMock()
    permission2.name = "employee.update"
    organisation_permissions1.permission = permission1
    organisation_permissions2.permission = permission2
    employee_roles = MagicMock()
    employee_roles.organisation_permissions = [organisation_permissions1, organisation_permissions2]
    employee.employee_roles = employee_roles

    user.employee = employee

    return user



