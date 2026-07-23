from unittest.mock import patch

import pytest

from app.exceptions.custom_exception import (
    EmployeeNotFound,
    TodayAttendanceAlreadyTaken
)



class TestAttendanceService:

    @patch('app.service.attendance_service.get_distance')
    def test_punch_in_success(
            self,
            mock_distance,
            attendance_service,
            employee_repo ,
            attendance_repo ,
            employee,
            attendance,
            employee_id,
            organisation_id,
            punch_schema,
                            ):
            mock_distance.return_value = 10
            employee_repo.get_employee_by_employee_id.return_value = employee
            attendance_repo.today_attendance_employee_is_punch_in.return_value = None
            attendance_repo.punch_in.return_value = attendance
            result  = attendance_service.punch_in_attendance(
                punch_schema,
                employee_id,
                organisation_id,
            )

            assert result == attendance

    def test_employee_not_found(

                    self,

                    attendance_service,

                    employee_repo,

                    employee_id,

                    organisation_id,

                    punch_schema,

            ):
                employee_repo.get_employee_by_employee_id.return_value = None

                with pytest.raises(EmployeeNotFound):
                    attendance_service.punch_in_attendance(

                        punch_schema,

                        employee_id,

                        organisation_id,

                    )

    def test_already_punched(

                    self,

                    attendance_service,

                    employee_repo,

                    attendance_repo,

                    employee,

                    employee_id,

                    organisation_id,

                    punch_schema,

            ):
                employee_repo.get_employee_by_employee_id.return_value = employee

                attendance_repo.today_attendance_employee_is_punch_in.return_value = object()

                with pytest.raises(TodayAttendanceAlreadyTaken):
                    attendance_service.punch_in_attendance(

                        punch_schema,

                        employee_id,

                        organisation_id,

                    )

