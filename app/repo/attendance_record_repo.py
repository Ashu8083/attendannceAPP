from calendar import monthrange
from uuid import UUID

from sqlalchemy import extract, func

from app.models import Attendance, Employee
from app.models.attendance_record_model import Attendance
from datetime import date,datetime
from sqlalchemy.orm import Session, InstrumentedAttribute
from app.enums.attandance_status import AttendanceStatus
from app.schemas.attendance_schema import *
from app.core.logging_config import logger
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from datetime import date

from app.models.attendance_record_model import Attendance


class AttendanceRepo:
    def __init__(self,db:Session):
            self.db = db

    # To get employee Attendance  
    def get_employee_attendance_by_date(self, attendance_date: date, employee_id : uuid.UUID , organisation_id : uuid.UUID) -> type[Attendance] | None:
        attendance_record = self.db.query(Attendance).filter(Attendance.employee_id == employee_id,
                                                                Attendance.organisation_id == organisation_id,
                                                              Attendance.attendance_date == attendance_date
                                                              ).first()
        return attendance_record

    def today_attendance_employee_is_punch_in(self,organisation_id,employee_id)->type[Attendance] | None:
        today = date.today()
        attendance_record = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                             Attendance.employee_id == employee_id,
                                                             Attendance.organisation_id == organisation_id,
                                                             Attendance.is_punchin == True).first()

        return attendance_record
    def today_attendacnce_employee_is_punch_out(self,organisation_id,employee_id)->type[Attendance] | None:
        today = date.today()
        attendace_record = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                            Attendance.employee_id == employee_id,
                                                            Attendance.organisation_id == organisation_id,
                                                            Attendance.is_punchout == True).first()
        return attendace_record

    def punch_in(self,employee_id : uuid.UUID, workMode : WorkMode,organisation_id : uuid.UUID):
        today = date.today()
        logger.info(
            "Employee %s is attempting to check in for attendance in organization %s.",
            employee_id,
            organisation_id,
        )
        attendance_record = Attendance(
                                        organisation_id = organisation_id,
                                        employee_id=employee_id,
                                        work_mode = workMode,
                                        attendance_date = today,
                                        punchin_time = datetime.now().time(),
                                        is_punchin = True,
                                        status = AttendanceStatus.PRESENT
                                        )

        try:
            self.db.add(attendance_record)
            self.db.flush()
            self.db.refresh(attendance_record)
            logger.info("Attendance record for employee %s in organisation  %s is created ", employee_id,organisation_id)
        except Exception:
            logger.exception("Error while creating attendance record for employee %s in organisation  %s", employee_id, organisation_id)
            self.db.rollback()
            raise
        logger.info( attendance_record.is_punchin, attendance_record.punchin_time)
        return attendance_record

    def punch_out(self,employee_id:uuid.UUID,organisation_id : uuid.UUID):
         today = date.today()
         attendance_record = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                             Attendance.employee_id == employee_id,
                                                             Attendance.organisation_id == organisation_id,
                                                             Attendance.is_punchout == True).first()
         if attendance_record :
              logger.error("Employee already Punchout")
              raise ValueError("employee already Punchout")

         
         attendance_record  = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                              Attendance.employee_id ==employee_id).first()
         
         if not attendance_record:
              logger.error("Employee attendance record not found")
              raise ValueError(f"Attendance record not Found {today}")
         attendance_record.is_punchout = True
         attendance_record.punchout_time = datetime.now().time()

         try:
            self.db.commit()
            self.db.refresh(attendance_record)
         except Exception:
             logger.exception("Employee attendance record can't created %s", attendance_record)
             self.db.rollback()
             raise
         return attendance_record

    def get_today_attendance(self,organisation_id)->list[type[Attendance]]:
         
         today = date.today()
         attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              Attendance.attendance_date == today).all()

         return attendance_record

    def get_employee_attendance(self,employee_id : uuid.UUID,organisation_id)->list[type[Attendance]]:
         employee_attendance_record = self.db.query(Attendance).filter(Attendance.employee_id == employee_id).where(Attendance.organisation_id == organisation_id).all()
         if not employee_attendance_record:
              logger.error("Employee attendance record not found")
              raise ValueError("employee attendance record not found")
         return employee_attendance_record

    

    def update_attendance(self,organisation_id : uuid.UUID ,employee_id : uuid.UUID, update_attendacne :AttendanceUpdate):


         attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              Attendance.employee_id == employee_id,
                                                              Attendance.attendance_date == update_attendacne.date).first()

         if attendance_record is None:
             return None
         # setattr() built-in function for  python to set the attribute manually
         for feld,value in update_attendacne.model_dump().items():
              setattr(attendance_record,feld,value)

         try :
            self.db.commit()
            self.db.refresh(attendance_record)
         except Exception:
            self.db.rollback()
            logger.error("Employee attendance record can't update %s", attendance_record)
            raise


         return attendance_record

    def mark_absent(self,organisation_id : uuid.UUID,attedance_date : date , employee : Employee ) -> Attendance:

        attendance_record = Attendance(
                                        organisation_id = organisation_id,
                                        employee_id=employee.id,
                                        work_mode = employee.work_mode ,
                                        attendance_date = attedance_date,
                                        punchin_time = None,
                                        punchout_time = None,
                                        is_punchin = False,
                                        is_punchout = False,
                                        status = AttendanceStatus.ABSENT
                                        )

        try  :
            self.db.add(attendance_record)
            self.db.commit()
            self.db.refresh(attendance_record)
        except Exception:
            self.db.rollback()
            raise
        return attendance_record

    def get_attendance_by_date(self,date :date,organisation_id :uuid.UUID ) -> list[type[Attendance]]:
        attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              Attendance.attendance_date == date).all()
        if not attendance_record:
              raise ValueError(f"{date} :Attendacne record not found ")
        return attendance_record


    def get_attendance_by_month(self,month : int,organisation_id : uuid.UUID ) -> list[type[Attendance]]:
         
         attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              extract("month", Attendance.attendance_date) == month).all()# extract the month from the date 
         # if not attendance_record:
         #      raise ValueError(f"{month} :Attendacne record not found ")
         return attendance_record


    def get_employee_today_attendance(self,organisation_id : uuid.UUID ,employee_id : uuid.UUID ) :
         today = date.today()
         today_attendace = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                          Attendance.attendance_date == today,
                                          Attendance.employee_id== employee_id).first()
         return today_attendace

    def delete_attendance(self):
         return None

    def get_present_employee(
            self,
            organisation_id: uuid.UUID,
            attendance_date: date
    ) -> set[uuid.UUID]:
        result = (
            self.db.query(Attendance.employee_id)
            .filter(
                Attendance.organisation_id == organisation_id,
                Attendance.attendance_date == attendance_date,
                Attendance.status == AttendanceStatus.PRESENT,
            )
            .all()
        )

        return {row.employee_id for row in result}

    def get_employee_month_attendance(
            self,
            month: int,
            year: int,
            organisation_id: uuid.UUID,
            employee_id: uuid.UUID,
            page: int | None = None,
            page_size: int | None = None,
    ):
        start_date = date(year, month, 1)

        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        stmt = (
            select(Attendance)
            .where(
                Attendance.organisation_id == organisation_id,
                Attendance.employee_id == employee_id,
                Attendance.attendance_date >= start_date,
                Attendance.attendance_date < end_date,
            )
            .options(
                selectinload(Attendance.employee),
                selectinload(Attendance.attendance_evidence),
            )
            .order_by(Attendance.attendance_date)
        )

        if page_size is not None and page_size > 0:
            eff_page = page or 1
            offset = (eff_page - 1) * page_size
            stmt = stmt.offset(offset).limit(page_size)

        records = self.db.scalars(stmt).all()

        # Count total records for pagination
        count_stmt = (
            select(func.count())
            .select_from(Attendance)
            .where(
                Attendance.organisation_id == organisation_id,
                Attendance.employee_id == employee_id,
                Attendance.attendance_date >= start_date,
                Attendance.attendance_date < end_date,
            )
        )

        total = self.db.scalar(count_stmt)

        return records, total