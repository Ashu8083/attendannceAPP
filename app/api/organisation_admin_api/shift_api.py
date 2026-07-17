from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.shift_schema import (
    ShiftCreate,
    ShiftUpdate,
    ShiftResponse,
)
from app.service.shift_service import ShiftService

router = APIRouter(
    prefix="/shifts",
    tags=["Shift"],
)


@router.post("/", response_model=ShiftResponse)
def create_shift(
    request: ShiftCreate,
    db: Session = Depends(get_db),
):
    service = ShiftService(db)
    return service.create_shift(request)


@router.get("/{shift_id}", response_model=ShiftResponse)
def get_shift(
    shift_id: int,
    db: Session = Depends(get_db),
):
    service = ShiftService(db)
    shift = service.get_shift(shift_id)

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    return shift


@router.get("/", response_model=list[ShiftResponse])
def get_all_shifts(
    db: Session = Depends(get_db),
):
    service = ShiftService(db)
    return service.get_all_shifts()


@router.get(
    "/organisation/{organisation_id}",
    response_model=list[ShiftResponse],
)
def get_organisation_shifts(
    organisation_id: UUID,
    db: Session = Depends(get_db),
):
    service = ShiftService(db)
    return service.get_organisation_shifts(organisation_id)


@router.put("/{shift_id}", response_model=ShiftResponse)
def update_shift(
    shift_id: int,
    request: ShiftUpdate,
    db: Session = Depends(get_db),
):
    service = ShiftService(db)
    shift = service.update_shift(shift_id, request)

    if not shift:
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    return shift


@router.delete("/{shift_id}")
def delete_shift(
    shift_id: int,
    db: Session = Depends(get_db),
):
    service = ShiftService(db)

    if not service.delete_shift(shift_id):
        raise HTTPException(
            status_code=404,
            detail="Shift not found",
        )

    return {
        "message": "Shift deleted successfully"
    }