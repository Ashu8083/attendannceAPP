from unittest.mock import MagicMock
from unittest.mock import patch
import pytest
from app.auth.auth_cntx import AuthContext

from app.exceptions.custom_exception import (
UserNotFound,EmployeeIsInactive
)

class TestAuthService:

    @patch("app.service.auth_service.decode_token")
    def test_verify_token_access_token(self,
                                       decode_token_mock,
                                       user_repo,
                                       user,
                                       user_id,
                                       auth_service,
                                       organisation_id,
                                       employee_id,
                                       ):
        decode_token_mock.return_value = {
            "user_id": str(user_id),
            "organisation_id": str(organisation_id),
            "employee_id": str(employee_id),
            "token_type": "access",
        }
        user_repo.get_user.return_value = user
        result = auth_service.verify_access_token("user_token")
        expected_result = AuthContext(
                                        user_id=user.id,
                                        organisation_id=user.organisation_id,
                                        system_role="ORGANISATION",  # depends on your enum value
                                        employee_id=user.employee.id,
                                        permissions={
                                                    "employee.create",
                                                    "employee.update",
                                                },

                                    )

    @patch("app.service.auth_service.decode_token")
    def test_user_not_found(            seld,
                                       decode_token_mock,
                                       user_repo,
                                       user,
                                       user_id,
                                       auth_service,
                                       organisation_id,
                                       employee_id,):
            decode_token_mock.return_value = {
                "user_id": None,
                "organisation_id": str(organisation_id),
                "employee_id": str(employee_id),
                "token_type": "access",
            }
            user_repo.get_user.return_value = None

            with pytest.raises(UserNotFound):
                auth_service.verify_access_token("user_token")

    @patch("app.service.auth_service.decode_token")
    def test_employee_inactive(        self,
                                       decode_token_mock,
                                       user_repo,
                                       user,
                                       user_id,
                                       auth_service,
                                       organisation_id,
                                       employee_id,):

        decode_token_mock.return_value = {
            "user_id": str(user_id),
        }












