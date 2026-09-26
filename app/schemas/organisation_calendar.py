from datetime import date

from pydantic import BaseModel, ConfigDict, Field

from app.enums.calender_enums import HolidayType, HolidayStatus


# =========================================================
# CREATE
# =========================================================

class OrganisationCalendarCreate(BaseModel):
    name: str
    finance_year_start: date
    finance_year_end: date
    status: str

    model_config = ConfigDict(from_attributes=True)


class OrganisationWorkScheduleCreate(BaseModel):
    day_of_week: str
    is_working_day: bool = True

    model_config = ConfigDict(from_attributes=True)


class HolidayCreate(BaseModel):
    holidays_date: date
    name: str
    description: str | None = None
    type_of_holiday: HolidayType
    status: HolidayStatus

    model_config = ConfigDict(from_attributes=True)


# =========================================================
# UPDATE
# =========================================================

class OrganisationCalendarUpdate(BaseModel):
    name: str | None = None
    finance_year_start: date | None = None
    finance_year_end: date | None = None
    status: str | None = None

    model_config = ConfigDict(from_attributes=True)


class OrganisationWorkScheduleUpdate(BaseModel):
    day_of_week: str | None = None
    is_working_day: bool | None = None

    model_config = ConfigDict(from_attributes=True)


class HolidayUpdate(BaseModel):
    holidays_date: date | None = None
    name: str | None = None
    description: str | None = None
    type_of_holiday: HolidayType | None = None
    status: HolidayStatus | None = None

    model_config = ConfigDict(from_attributes=True)


class HolidayQuery(BaseModel):
    year: int = Field(..., ge=2000)
    month: int | None = Field(
        default=None,
        ge=1,
        le=12
    )
    page: int = Field(
        default=1,
        ge=1
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100
    )