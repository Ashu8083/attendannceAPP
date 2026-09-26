import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.service.organisation_calender import (
OrganisationCalendarService,
)

from app.schemas.organisation_calendar import (
    OrganisationCalendarCreate,
    OrganisationCalendarUpdate,
    HolidayCreate,
    HolidayUpdate,
    OrganisationWorkScheduleCreate,
    OrganisationWorkScheduleUpdate,
)
from core.response_helper import CommonJSONResponse

router = APIRouter(
    prefix="/organisation-calendar",
    tags=["Organisation Calendar"],
)


# =========================================================
# CALENDAR
# =========================================================

@router.post(
    "/{organisation_id}",
    status_code=status.HTTP_201_CREATED,
)
def create_calendar(
    organisation_id: uuid.UUID,
    data: OrganisationCalendarCreate,
    service: OrganisationCalendarService = Depends(get_db),
):
    organisation_calendar = service.create_calendar(
        organisation_id=organisation_id,
        data=data,
    )

    return CommonJSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=organisation_calendar,
        
    )


@router.get(
    "/{organisation_id}",
)
def get_calendar(
    organisation_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    try:
        return service.get_calendar(
            organisation_id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


@router.patch(
    "/{organisation_id}",
)
def update_calendar(
    organisation_id: uuid.UUID,
    data: OrganisationCalendarUpdate,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    try:
        return service.update_calendar(
            organisation_id=organisation_id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# =========================================================
# HOLIDAYS
# =========================================================

@router.post(
    "/{calendar_id}/holidays",
    status_code=status.HTTP_201_CREATED,
)
def create_holiday(
    calendar_id: uuid.UUID,
    data: HolidayCreate,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    return service.create_holiday(
        calendar_id=calendar_id,
        data=data,
    )


@router.get(
    "/{organisation_id}/holidays",
)
def get_holidays(
    organisation_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    return service.get_holidays(
        organisation_id
    )


@router.patch(
    "/holidays/{holiday_id}",
)
def update_holiday(
    holiday_id: uuid.UUID,
    data: HolidayUpdate,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    try:
        return service.update_holiday(
            holiday_id=holiday_id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )


# =========================================================
# WORK SCHEDULE
# =========================================================

@router.post(
    "/{calendar_id}/work-schedule",
    status_code=status.HTTP_201_CREATED,
)
def create_work_schedule(
    calendar_id: uuid.UUID,
    data: OrganisationWorkScheduleCreate,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    return service.create_work_schedule(
        calendar_id=calendar_id,
        data=data,
    )


@router.get(
    "/{organisation_id}/work-schedule",
)
def get_work_schedule(
    organisation_id: uuid.UUID,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    return service.get_work_schedule(
        organisation_id
    )


@router.patch(
    "/work-schedule/{work_schedule_id}",
)
def update_work_schedule(
    work_schedule_id: uuid.UUID,
    data: OrganisationWorkScheduleUpdate,
    db: Session = Depends(get_db),
):
    service = OrganisationCalendarService(db)

    try:
        return service.update_work_schedule(
            work_schedule_id=work_schedule_id,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e),
        )