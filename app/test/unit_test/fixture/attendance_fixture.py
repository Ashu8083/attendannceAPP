import pytest
from unittest.mock import MagicMock


@pytest.fixture
def attendance():
    attendance = MagicMock

    attendance.is_punch_in = True
    return attendance