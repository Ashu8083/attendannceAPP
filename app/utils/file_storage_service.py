from abc import ABC, abstractmethod
from datetime import datetime

from app.enums.attandance_status import TypeAttendance


class FileService(ABC):

    @abstractmethod
    def save_attendance_image(
        self,
        organisation_id,
        employee_code,
        attendance_id,
        check_out_type : TypeAttendance,
        captured_at: datetime,
        image_bytes: bytes,
        extension: str = "jpg",
    ) -> str:
        pass