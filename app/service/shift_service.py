from sqlalchemy.orm import Session

from app.models.shift import Shift
from app.repositories.shift_repository import ShiftRepository
from app.schemas.shift_schema import ShiftCreate, ShiftUpdate


class ShiftService:

    def __init__(self, db: Session):
        self.shift_repo = ShiftRepository(db)

    def create_shift(self, request: ShiftCreate):
        shift = Shift(
            name=request.name,
            organisation_id=request.organisation_id,
            start_time=request.start_time,
            end_time=request.end_time,
            grace_minutes=request.grace_minutes,
        )

        return self.shift_repo.create(shift)

    def get_shift(self, shift_id: int):
        return self.shift_repo.get_by_id(shift_id)

    def get_all_shifts(self):
        return self.shift_repo.get_all()

    def get_organisation_shifts(self, organisation_id):
        return self.shift_repo.get_by_organisation(organisation_id)

    def update_shift(self, shift_id: int, request: ShiftUpdate):
        shift = self.shift_repo.get_by_id(shift_id)

        if not shift:
            return None

        if request.name is not None:
            shift.name = request.name

        if request.start_time is not None:
            shift.start_time = request.start_time

        if request.end_time is not None:
            shift.end_time = request.end_time

        if request.grace_minutes is not None:
            shift.grace_minutes = request.grace_minutes

        return self.shift_repo.update(shift)

    def delete_shift(self, shift_id: int):
        shift = self.shift_repo.get_by_id(shift_id)

        if not shift:
            return False

        self.shift_repo.delete(shift)
        return True