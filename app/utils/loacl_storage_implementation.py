from pathlib import Path
from datetime import datetime

from app.utils.file_storage_service import FileService


class LocalFileService(FileService):

    def __init__(self, base_path: str = "uploads"):
        self.base_path = Path(base_path)

    def save_attendance_image(
        self,
        organisation_id,
        employee_code,
        attendance_id,
        check_out_type,
        captured_at: datetime,
        image_bytes: bytes,
        extension: str = "jpg",
    ) -> str:
        directory = (
            self.base_path
            / "organisations"
            / str(organisation_id)
            / "attendance"
            / str(captured_at.year)
            / f"{captured_at.month:02d}"
            / f"{captured_at.day:02d}"
        )
        directory.mkdir(
            parents=True,
            exist_ok=True
        )
        filename = (
            f"{employee_code}_"
            f"{attendance_id}_"
            f"{check_out_type}."
            f"{extension}"
        )
        file_path = directory / filename
        file_path.write_bytes(image_bytes)
        # Return path that can be stored in DB
        return str(
            file_path.relative_to(self.base_path)
        )
    def save_profile_picture(
            self,
            organisation_id,
            employee_code,
            captured_at: datetime,
            image_bytes: bytes,
            extension: str = "jpg",
    ) -> str:
        directory = (
                self.base_path
                / "organisations"
                / str(organisation_id)
                / "branches"
                / "employees"
                / str(employee_code)
                / "profile"
        )
        directory.mkdir(
            parents=True,
            exist_ok=True
        )
        filename = f"profile.{extension}"
        file_path = directory / filename
        file_path.write_bytes(image_bytes)
        return str(
            file_path.relative_to(self.base_path)
        )