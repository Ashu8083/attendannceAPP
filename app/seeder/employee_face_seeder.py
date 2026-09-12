import uuid
import random
import argparse
from pathlib import Path
from datetime import date, time, timedelta

from sqlalchemy.orm import Session

from app.models.attendance_record_model import Attendance
from app.models.attendance_record_evidance import AttendanceEvidence
from app.models.employee_models import Employee
from app.models.organisations import Organisation

from app.enums.attandance_status import (
    AttendanceStatus,
    TypeAttendance,
)
from app.enums.work_mode import WorkMode


# ============================================================
# CONFIGURATION & CONSTANTS
# ============================================================

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
UPLOADS_DIR = PROJECT_ROOT / "uploads"

# Reference attendance image
DEFAULT_IMAGE_PATH = (
    UPLOADS_DIR
    / "organisations"
    / "10fbcac9-3ce1-4c53-a943-b2a5eb10f17a"
    / "attendance"
    / "2026"
    / "09"
    / "11"
    / "EMP002_04d9550b-86c3-4e1f-8fe7-c483549cdaab_CHECKIN.jpg"
)

# Number of attendance records per month for test seeding
ATTENDANCE_PER_MONTH = 15

# Target months to seed (August and September 2026)
MONTHS = [
    (2026, 8),
    (2026, 9),
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def resolve_reference_image(custom_path: Path = None) -> tuple[Path, str]:
    """
    Resolves the reference image path and its relative URL string for DB storage.
    """
    target = custom_path or DEFAULT_IMAGE_PATH

    if not target.exists():
        # Fallback search inside uploads directory for any check-in or jpg image
        jpg_files = list(UPLOADS_DIR.rglob("*.jpg"))
        if jpg_files:
            target = jpg_files[0]
        else:
            raise FileNotFoundError(
                f"No reference attendance image found at {target} and no fallback jpg in {UPLOADS_DIR}"
            )

    try:
        # Calculate relative path from uploads/ directory for DB face_profile_url
        uploads_idx = target.parts.index("uploads")
        relative_url = str(Path(*target.parts[uploads_idx + 1:]))
    except (ValueError, IndexError):
        relative_url = str(target)

    return target, relative_url


def get_working_days(
    year: int,
    month: int,
    allow_future: bool = True,
) -> list[date]:
    """
    Get Monday-Friday dates for the given month.
    If allow_future is False, future dates beyond today are excluded.
    For test data seeding, allow_future=True enables generating 15 days in September.
    """
    current_date = date(year, month, 1)
    working_days = []
    today = date.today()

    while current_date.month == month:
        # Monday = 0, Friday = 4
        if current_date.weekday() < 5:
            if allow_future or current_date <= today:
                working_days.append(current_date)
        current_date += timedelta(days=1)

    return working_days


def generate_punchin_time() -> time:
    """Generate random punch-in time between 08:00 and 09:59."""
    return time(
        hour=random.choice([8, 9]),
        minute=random.randint(0, 59),
    )


def generate_punchout_time() -> time:
    """Generate random punch-out time between 17:00 and 18:59."""
    return time(
        hour=random.choice([17, 18]),
        minute=random.randint(0, 59),
    )


def generate_face_match_score() -> float:
    """Generate random face match score between 0.85 and 0.98."""
    return round(random.uniform(0.85, 0.98), 3)


# ============================================================
# MAIN SEEDER FUNCTION
# ============================================================

def seed_attendance(
    db: Session,
    employee_id: uuid.UUID = None,
    organisation_id: uuid.UUID = None,
    employee_code: str = None,
    records_per_month: int = ATTENDANCE_PER_MONTH,
    months: list[tuple[int, int]] = None,
    image_path: Path = None,
    allow_future: bool = True,
):
    """
    Seeds test attendance and evidence records for August and September.
    Uses reference image for face evidence.
    """
    if months is None:
        months = MONTHS

    # 1. Resolve reference image
    ref_image_path, relative_face_url = resolve_reference_image(image_path)
    print(f"Using reference image: {ref_image_path}")
    print(f"Face profile URL stored in DB: {relative_face_url}")

    # 2. Find employee and organisation automatically if not provided
    employee = None
    if employee_id:
        employee = db.get(Employee, employee_id)
    elif employee_code:
        employee = db.query(Employee).filter(Employee.employee_code == employee_code).first()

    if not employee:
        # Fallback to first available employee in DB (preferably EMP002 or EMP001)
        employee = db.query(Employee).filter(Employee.employee_code == "EMP002").first()
        if not employee:
            employee = db.query(Employee).first()

    if not employee:
        raise ValueError("No employee found in database to seed attendance for.")

    employee_id = employee.id
    employee_code = employee.employee_code
    organisation_id = organisation_id or employee.organisation_id

    print(f"\nSeeding attendance for:")
    print(f"  Employee Code  : {employee_code}")
    print(f"  Employee ID    : {employee_id}")
    print(f"  Organisation ID: {organisation_id}")
    print(f"  Records/Month  : {records_per_month}")

    # Counters
    total_attendance = 0
    total_evidence = 0

    # 3. Process each month
    for year, month in months:
        print(f"\nProcessing {year}-{month:02d}...")

        working_days = get_working_days(year=year, month=month, allow_future=allow_future)
        if not working_days:
            print(f"  No working days available for {year}-{month:02d}")
            continue

        # Get existing attendance dates for this month
        existing_attendances = (
            db.query(Attendance)
            .filter(
                Attendance.employee_id == employee_id,
                Attendance.attendance_date >= date(year, month, 1),
                Attendance.attendance_date <= date(year, month, len(working_days) + 8),
            )
            .all()
        )
        existing_dates = {att.attendance_date for att in existing_attendances}
        existing_count = len(existing_dates)

        available_dates = [d for d in working_days if d not in existing_dates]

        needed_count = max(0, records_per_month - existing_count)
        if needed_count == 0:
            print(f"  Month {year}-{month:02d} already has {existing_count} records (target: {records_per_month}). Skipping.")
            continue

        num_to_create = min(needed_count, len(available_dates))
        if num_to_create == 0:
            print(f"  No available dates to create new records for {year}-{month:02d}")
            continue

        selected_dates = random.sample(available_dates, num_to_create)
        selected_dates.sort()

        print(f"  Creating {num_to_create} attendance records (existing: {existing_count}, target: {records_per_month})...")

        for att_date in selected_dates:
            punchin_time = generate_punchin_time()
            punchout_time = generate_punchout_time()

            attendance = Attendance(
                id=uuid.uuid4(),
                organisation_id=organisation_id,
                employee_id=employee_id,
                attendance_date=att_date,
                is_punchin=True,
                punchin_time=punchin_time,
                is_punchout=True,
                punchout_time=punchout_time,
                status=AttendanceStatus.PRESENT,
                work_mode=WorkMode.WFO,
            )
            db.add(attendance)
            db.flush()

            # Check-in evidence
            checkin_ev = AttendanceEvidence(
                id=uuid.uuid4(),
                attendance_record_id=attendance.id,
                face_match_score=generate_face_match_score(),
                type=TypeAttendance.CHECKIN,
                face_profile_url=relative_face_url,
            )

            # Check-out evidence
            checkout_ev = AttendanceEvidence(
                id=uuid.uuid4(),
                attendance_record_id=attendance.id,
                face_match_score=generate_face_match_score(),
                type=TypeAttendance.CHECKOUT,
                face_profile_url=relative_face_url,
            )

            db.add(checkin_ev)
            db.add(checkout_ev)

            total_attendance += 1
            total_evidence += 2

            print(f"    ✓ {att_date} | IN {punchin_time} | OUT {punchout_time}")

    # 4. Commit transaction
    try:
        db.commit()
    except Exception:
        db.rollback()
        raise

    # 5. Summary
    print("\n========================================")
    print("  Attendance & Evidence Seeding Completed")
    print("========================================")
    print(f"  Total Attendance Records Created : {total_attendance}")
    print(f"  Total Evidence Records Created   : {total_evidence}")
    print(f"  Reference Image Used             : {ref_image_path}")
    print("========================================")


# ============================================================
# CLI ENTRY POINT
# ============================================================

if __name__ == "__main__":
    from app.db.database import SessionLocal

    parser = argparse.ArgumentParser(description="Seed test attendance & face evidence records.")
    parser.add_argument("--employee-code", type=str, help="Employee code (e.g. EMP002)")
    parser.add_argument("--employee-id", type=str, help="Employee UUID")
    parser.add_argument("--organisation-id", type=str, help="Organisation UUID")
    parser.add_argument("--per-month", type=int, default=ATTENDANCE_PER_MONTH, help="Number of records per month (default 15)")

    args = parser.parse_args()

    emp_id = uuid.UUID(args.employee_id) if args.employee_id else None
    org_id = uuid.UUID(args.organisation_id) if args.organisation_id else None

    db = SessionLocal()

    try:
        seed_attendance(
            db=db,
            employee_id=emp_id,
            organisation_id=org_id,
            employee_code=args.employee_code,
            records_per_month=args.per_month,
        )
    except Exception as error:
        db.rollback()
        print("\n❌ Seeder execution failed:", error)
        raise
    finally:
        db.close()