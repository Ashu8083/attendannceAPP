from dateutil.relativedelta import relativedelta
from sqlalchemy.orm import Session
from app.models import OrganisationCalendar, Holidays, OrganisationWorkSchedule
from uuid import UUID


from datetime import date,time,datetime
from uuid import UUID
from sqlalchemy.orm import Session

from app.models import (
    OrganisationCalendar,
    Holidays,
    OrganisationWorkSchedule,
)
from app.schemas.organisation_calendar import (
    OrganisationCalendarUpdate,
    HolidayUpdate,
    OrganisationWorkScheduleUpdate, HolidayQuery,
)


class OrganisationCalendarRepo:

    def __init__(self, db: Session):
        self.db = db

    # -------------------------
    # CREATE
    # -------------------------

    def create_organisation_calendar(
        self,
        organisation: OrganisationCalendar
    ):
        self.db.add(organisation)
        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    def create_organisation_holiday_calendar(
        self,
        holiday: Holidays
    ):
        self.db.add(holiday)
        self.db.commit()
        self.db.refresh(holiday)

        return holiday

    def create_organisation_work_schedule(
        self,
        work_schedule: OrganisationWorkSchedule
    ):
        self.db.add(work_schedule)
        self.db.commit()
        self.db.refresh(work_schedule)

        return work_schedule

    # -------------------------
    # GET
    # -------------------------

    def get_organisation_calendar_by_id(
        self,
        organisation_id: UUID
    ):
        return (
            self.db.query(OrganisationCalendar)
            .filter(
                OrganisationCalendar.organisation_id == organisation_id
            )
            .first()
        )

    def get_organisation_holiday_calendar_by_id(
        self,
        organisation_id: UUID
    ):
        return (
            self.db.query(Holidays)
            .join(
                OrganisationCalendar,
                Holidays.organisation_calender_id ==
                OrganisationCalendar.id
            )
            .filter(
                OrganisationCalendar.organisation_id == organisation_id
            )
            .all()
        )

    def get_organisation_work_schedule_by_id(
        self,
        organisation_id: UUID
    ):
        return (
            self.db.query(OrganisationWorkSchedule)
            .join(
                OrganisationCalendar,
                OrganisationWorkSchedule.calendar_id ==
                OrganisationCalendar.id
            )
            .filter(
                OrganisationCalendar.organisation_id == organisation_id
            )
            .all()
        )

    def get_holidays_by_month_and_year(
            self,
            year: int,
            month: int | None,
            page: int,
            limit: int,
            organisation_id: UUID,
    ):
         query_for_holidays = (self.db.query(Holidays).filter(Holidays).join(
            OrganisationCalendar,
            Holidays.organisation_calender_id == OrganisationCalendar.id)
            .filter(OrganisationCalendar.organisation_id == organisation_id))

         year = date.today().year

         if month:

            start_date = date(year,month,1)
            if month == 12:
                end_date = date(year + 1, 1, 1)
            else:
                end_date = date(year,month, 2)
            query_for_holidays = query_for_holidays.filter(
                Holidays.holidays_date >= start_date,
                Holidays.holidays_date <= end_date
            )
         else:
             # Entire year
             start_date = date(year, 1, 1)
             end_date = date(year + 1, 1)

             query_for_holidays = query_for_holidays.filter(
                 Holidays.holidays_date >= start_date,
                 Holidays.holidays_date < end_date
             )

         total = query_for_holidays.count()
         offset = (page - 1) * limit

         holidays = (
             query_for_holidays
             .order_by(Holidays.holidays_date.asc())
             .offset(offset)
             .limit(limit)
             .all()
         )

         return holidays,total

    # -------------------------
    # UPDATE CALENDAR
    # -------------------------

    def update_organisation_calendar(
        self,
        organisation: OrganisationCalendar,
        update_data: OrganisationCalendarUpdate
    ):
        data = update_data.model_dump(
            exclude_unset=True
        )

        for field, value in data.items():
            setattr(organisation, field, value)

        self.db.commit()
        self.db.refresh(organisation)

        return organisation

    # -------------------------
    # UPDATE HOLIDAY
    # -------------------------

    def update_organisation_holiday_calendar(
        self,
        holiday: Holidays,
        update_data: HolidayUpdate
    ):
        data = update_data.model_dump(
            exclude_unset=True
        )

        for field, value in data.items():
            setattr(holiday, field, value)

        self.db.commit()
        self.db.refresh(holiday)

        return holiday

    # -------------------------
    # UPDATE WORK SCHEDULE
    # -------------------------

    def update_organisation_work_schedule(
        self,
        work_schedule: OrganisationWorkSchedule,
        update_data: OrganisationWorkScheduleUpdate
    ):
        data = update_data.model_dump(
            exclude_unset=True
        )

        for field, value in data.items():
            setattr(work_schedule, field, value)

        self.db.commit()
        self.db.refresh(work_schedule)

        return work_schedule