
import uuid
from sqlite3 import IntegrityError

from sqlalchemy.orm import Session
from app.core.logging_config import logger

from app.models import (
    OrganisationCalendar,
    Holidays,
    OrganisationWorkSchedule,
)

from app.schemas.organisation_calendar import (
    OrganisationCalendarCreate,
    OrganisationCalendarUpdate,
    HolidayCreate,
    HolidayUpdate,
    OrganisationWorkScheduleCreate,
    OrganisationWorkScheduleUpdate, HolidayQuery,
)

from app.repo.organisation_calender_repo import (
    OrganisationCalendarRepo,
)


class OrganisationCalendarService:

    def __init__(self, db: Session, repo: OrganisationCalendarRepo):
        self.repo = repo
        self.db = db

    # =========================================================
    # CREATE CALENDAR
    # =========================================================

    def create_calendar(
        self,
        organisation_id: uuid.UUID,
        data: OrganisationCalendarCreate,
    ):

        calendar = OrganisationCalendar(
            organisation_id=organisation_id,
            name=data.name,
            finance_year_start=data.finance_year_start,
            finance_year_end=data.finance_year_end,
            status=data.status,
        )
        try:
            self.repo.create_organisation_calendar(
                calendar
            )
        except Exception as e:
            logger.error("Organisation calendar already exists")
            raise


    # =========================================================
    # GET CALENDAR
    # =========================================================

    def get_calendar(
        self,
        organisation_id: uuid.UUID,
    ):
        calendar = self.repo.get_organisation_calendar_by_id(
            organisation_id
        )

        if not calendar:
            raise ValueError(
                "Organisation calendar not found"
            )

        return calendar

    # =========================================================
    # UPDATE CALENDAR
    # =========================================================

    def update_calendar(
        self,
        organisation_id: uuid.UUID,
        data: OrganisationCalendarUpdate,
    ):
        calendar = self.repo.get_organisation_calendar_by_id(
            organisation_id
        )

        if not calendar:
            raise ValueError(
                "Organisation calendar not found"
            )

        return self.repo.update_organisation_calendar(
            calendar,
            data,
        )

    # =========================================================
    # CREATE HOLIDAY
    # =========================================================

    def create_holiday(
        self,
        calendar_id: uuid.UUID,
        data: HolidayCreate,
    ):

        holiday = Holidays(
            organisation_calender_id=calendar_id,
            holidays_date=data.holidays_date,
            name=data.name,
            description=data.description,
            type_of_holiday=data.type_of_holiday,
            status=data.status,
        )

        return self.repo.create_organisation_holiday_calender(
            holiday
        )

    # =========================================================
    # GET HOLIDAYS
    # =========================================================

    def get_holidays(
        self,
        query : HolidayQuery,
        organisation_id: uuid.UUID,
    ):

        return self.repo.get_holidays_by_month_and_year(
            year=query.year,
            month=query.month,
            page =query.page,
            limit=query.limit,
            organisation_id=organisation_id,
        )

    # =========================================================
    # UPDATE HOLIDAY
    # =========================================================

    def update_holiday(
        self,
        holiday_id: uuid.UUID,
        data: HolidayUpdate,
    ):

        holiday = self.repo.get_holiday_by_id(
            holiday_id
        )

        if not holiday:
            raise ValueError(
                "Holiday not found"
            )

        return self.repo.update_organisation_holiday_calendar(
            holiday,
            data,
        )

    # =========================================================
    # CREATE WORK SCHEDULE
    # =========================================================

    def create_work_schedule(
        self,
        calendar_id: uuid.UUID,
        data: OrganisationWorkScheduleCreate,
    ):

        work_schedule = OrganisationWorkSchedule(
            calendar_id=calendar_id,
            day_of_week=data.day_of_week,
            is_working_day=data.is_working_day,
        )

        return self.repo.create_organisation_work_schedule(
            work_schedule
        )

    # =========================================================
    # GET WORK SCHEDULE
    # =========================================================

    def get_work_schedule(
        self,
        organisation_id: uuid.UUID,
    ):

        return self.repo.get_organisation_work_schedule_by_id(
            organisation_id
        )

    # =========================================================
    # UPDATE WORK SCHEDULE
    # =========================================================

    def update_work_schedule(
        self,
        work_schedule_id: uuid.UUID,
        data: OrganisationWorkScheduleUpdate,
    ):

        work_schedule = self.repo.get_work_schedule_by_id(
            work_schedule_id
        )

        if not work_schedule:
            raise ValueError(
                "Work schedule not found"
            )

        return self.repo.update_organisation_work_schedule(
            work_schedule,
            data,
        )