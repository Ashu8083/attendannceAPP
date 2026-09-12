import asyncio
from unittest.mock import patch, MagicMock
import pytest

from app.exceptions.custom_exception import (
    EmployeeNotFound,
    TodayAttendanceAlreadyTaken,
    FaceDoseNotMatch
)


class TestAttendanceService:

    @patch('app.service.attendance_service.arcface_match')
    @patch('app.service.attendance_service.extract_face_embedding_db')
    @patch('app.service.attendance_service.get_distance')
    def test_punch_in_success(
            self,
            mock_distance,
            mock_extract,
            mock_match,
            attendance_service,
            employee_repo,
            attendance_repo,
            employee,
            attendance,
            employee_id,
            organisation_id,
    ):
        mock_distance.return_value = 10
        mock_extract.return_value = [0.1]
        mock_match.return_value = (0.85, 0.9)
        employee_repo.get_employee_by_employee_id.return_value = employee
        attendance_repo.today_attendance_employee_is_punch_in.return_value = None
        attendance_repo.punch_in.return_value = attendance
        attendance_service.file_service.save_attendance_image.return_value = "uploads/test.jpg"

        result_attendance, storage_path = asyncio.run(
            attendance_service.punch_in_attendance(
                face_image=b"fake_image_data",
                employee_latitude=12.9716,
                employee_longitude=77.5946,
                employee_id=employee_id,
                organisation_id=organisation_id,
            )
        )

        assert result_attendance == attendance
        assert storage_path == "uploads/test.jpg"

    def test_employee_not_found(
            self,
            attendance_service,
            employee_repo,
            employee_id,
            organisation_id,
    ):
        employee_repo.get_employee_by_employee_id.return_value = None
        with pytest.raises(EmployeeNotFound):
            asyncio.run(
                attendance_service.punch_in_attendance(
                    face_image=b"fake_image_data",
                    employee_latitude=12.9716,
                    employee_longitude=77.5946,
                    employee_id=employee_id,
                    organisation_id=organisation_id,
                )
            )

    def test_already_punched(
            self,
            attendance_service,
            employee_repo,
            attendance_repo,
            employee,
            employee_id,
            organisation_id,
    ):
        employee_repo.get_employee_by_employee_id.return_value = employee
        attendance_repo.today_attendance_employee_is_punch_in.return_value = object()

        with pytest.raises(TodayAttendanceAlreadyTaken):
            asyncio.run(
                attendance_service.punch_in_attendance(
                    face_image=b"fake_image_data",
                    employee_latitude=12.9716,
                    employee_longitude=77.5946,
                    employee_id=employee_id,
                    organisation_id=organisation_id,
                )
            )

    @patch('app.service.attendance_service.arcface_match')
    @patch('app.service.attendance_service.extract_face_embedding_db')
    @patch('app.service.attendance_service.get_distance')
    def test_punch_out_success(
            self,
            mock_distance,
            mock_extract,
            mock_match,
            attendance_service,
            employee_repo,
            attendance_repo,
            employee,
            attendance,
            employee_id,
            organisation_id,
    ):
        mock_distance.return_value = 10
        mock_extract.return_value = [0.1]
        mock_match.return_value = (0.85, 0.9)
        employee_repo.get_employee_by_employee_id.return_value = employee
        attendance_repo.today_attendacnce_employee_is_punch_out.return_value = None
        attendance_repo.punch_out.return_value = attendance
        attendance_service.file_service.save_attendance_image.return_value = "uploads/test_out.jpg"

        result_attendance, storage_path = asyncio.run(
            attendance_service.punch_out_attendance(
                face_image=b"fake_image_data",
                employee_latitude=12.9716,
                employee_longitude=77.5946,
                employee_id=employee_id,
                organisation_id=organisation_id,
            )
        )

        assert result_attendance == attendance
        assert storage_path == "uploads/test_out.jpg"


