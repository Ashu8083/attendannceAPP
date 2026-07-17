from uuid import UUID

from sqlalchemy.orm import Session

from app.models.shift import Shift


class ShiftRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, shift: Shift) -> Shift:
        self.db.add(shift)
        self.db.commit()
        self.db.refresh(shift)
        return shift

    def get_by_id(self, shift_id: int) -> Shift | None:
        return (
            self.db.query(Shift)
            .filter(Shift.id == shift_id)
            .first()
        )

    def get_all(self):
        return self.db.query(Shift).all()

    def get_by_organisation(self, organisation_id: UUID):
        return (
            self.db.query(Shift)
            .filter(Shift.organisation_id == organisation_id)
            .all()
        )

    def update(self, shift: Shift) -> Shift:
        self.db.commit()
        self.db.refresh(shift)
        return shift

    def delete(self, shift: Shift):
        self.db.delete(shift)
        self.db.commit()