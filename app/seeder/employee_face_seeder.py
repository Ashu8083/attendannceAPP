# app/seeder/attendance_seeder.py

import uuid
import random

from pathlib import Path
from datetime import date, time, timedelta

from PIL import Image, ImageDraw

from sqlalchemy.orm import Session

from app.models.attendance_record_model import Attendance
from app.models.attendance_record_evidance import AttendanceEvidence
from app.models.employee_models import Employee

from app.enums.attandance_status import (
    AttendanceStatus,
    TypeAttendance,
)
from app.enums.work_mode import WorkMode


BASE_PATH = Path("uploads")


def create_dummy_image(
    file_path: Path,
    employee_code: str,
    attendance_date: date,
    punch_type: str,
):
    """
    Creates a dummy JPG image for development/testing.
    """

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    image = Image.new(
        "RGB",
        (800, 600),
        "white",
    )

    draw = ImageDraw.Draw(image)

    draw.text(
        (50, 50),
        "ATTENDANCE EVIDENCE",
        fill="black",
    )

    draw.text(
        (50, 100),
        f"Employee: {employee_code}",
        fill="black",
    )

    draw.text(
        (50, 150),
        f"Date: {attendance_date}",
        fill="black",
    )

    draw.text(
        (50, 200),
        f"Type: {punch_type}",
        fill="black",
    )

    image.save(
        file_path,
        format="JPEG",
        quality=90,
    )


def seed_attendance(
    db: Session,
    employee_id: uuid.UUID,
    organisation_id: uuid.UUID,
):
    employee = db.get(Employee, employee_id)

    if not employee:
        raise ValueError(
            f"Employee {employee_id} not found"
        )

    employee_code = employee.employee_code

    months = [
        (2026, 8),
        (2026, 9),
    ]

    total_attendance = 0
    total_images = 0

    for year, month in months:

        # ---------------------------------------
        # Get weekdays
        # ---------------------------------------

        current_date = date(
            year,
            month,
            1,
        )

        working_days = []

        while current_date.month == month:

            # Monday = 0
            # Sunday = 6
            if current_date.weekday() < 5:
                working_days.append(current_date)

            current_date += timedelta(days=1)

        # ---------------------------------------
        # Pick 15 days
        # ---------------------------------------

        attendance_dates = random.sample(
            working_days,
            15,
        )

        attendance_dates.sort()

        for attendance_date in attendance_dates:

            # ---------------------------------------
            # Generate punch-in time
            # ---------------------------------------

            punchin_time = time(
                hour=random.choice([8, 9]),
                minute=random.randint(0, 59),
            )

            # ---------------------------------------
            # Generate punch-out time
            # ---------------------------------------

            punchout_time = time(
                hour=random.choice([17, 18]),
                minute=random.randint(0, 59),
            )

            # ---------------------------------------
            # Attendance
            # ---------------------------------------

            attendance = Attendance(
                id=uuid.uuid4(),

                organisation_id=organisation_id,

                employee_id=employee_id,

                attendance_date=attendance_date,

                is_punchin=True,

                punchin_time=punchin_time,

                is_punchout=True,

                punchout_time=punchout_time,

                status=AttendanceStatus.PRESENT,

                work_mode=WorkMode.OFFICE,
            )

            db.add(attendance)

            # Important:
            # We need attendance.id before
            # creating the evidence path.
            db.flush()

            # ---------------------------------------
            # Directory
            # ---------------------------------------

            directory = (
                BASE_PATH
                / "organisations"
                / str(organisation_id)
                / "attendance"
                / str(year)
                / f"{month:02d}"
                / f"{attendance_date.day:02d}"
            )

            directory.mkdir(
                parents=True,
                exist_ok=True,
            )

            # ---------------------------------------
            # CHECK-IN IMAGE
            # ---------------------------------------

            checkin_filename = (
                f"{employee_code}_"
                f"{attendance.id}_"
                f"check-in.jpg"
            )

            checkin_path = (
                directory /
                checkin_filename
            )

            create_dummy_image(
                file_path=checkin_path,
                employee_code=employee_code,
                attendance_date=attendance_date,
                punch_type="CHECK-IN",
            )

            # ---------------------------------------
            # CHECK-OUT IMAGE
            # ---------------------------------------

            checkout_filename = (
                f"{employee_code}_"
                f"{attendance.id}_"
                f"check-out.jpg"
            )

            checkout_path = (
                directory /
                checkout_filename
            )

            create_dummy_image(
                file_path=checkout_path,
                employee_code=employee_code,
                attendance_date=attendance_date,
                punch_type="CHECK-OUT",
            )

            # ---------------------------------------
            # CHECK-IN evidence
            # ---------------------------------------

            checkin_evidence = AttendanceEvidence(
                id=uuid.uuid4(),

                attendance_record_id=attendance.id,

                face_match_score=round(
                    random.uniform(0.85, 0.98),
                    3,
                ),

                type=TypeAttendance.CHECKIN,

                face_profile_url=str(
                    checkin_path
                ),
            )

            # ---------------------------------------
            # CHECK-OUT evidence
            # ---------------------------------------

            checkout_evidence = AttendanceEvidence(
                id=uuid.uuid4(),

                attendance_record_id=attendance.id,

                face_match_score=round(
                    random.uniform(0.85, 0.98),
                    3,
                ),

                type=TypeAttendance.CHECKOUT,

                 face_profile_url=str(
                    checkout_path
                ),
            )

            db.add(checkin_evidence)
            db.add(checkout_evidence)

            total_attendance += 1
            total_images += 2

    db.commit()

    print(
        f"Created {total_attendance} attendance records"
    )

    print(
        f"Created {total_images} attendance images"
    )