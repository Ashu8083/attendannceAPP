from sqlalchemy import extract

from app.models.attendance_record_model import Attendance
from datetime import date,datetime
from sqlalchemy.orm import Session
from app.enums.attandance_status import AttendanceStatus
from app.schemas.attendance_schema import *

from app.models.attendance_record_model import Attendance


class AttendanceRepo:
    def __init__(self,db:Session):
            self.db = db


    def punch_in(self,punch_in_schema : PunchInSchema):
        today = date.today()
        Attendance_record = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                             Attendance.employee_id == punch_in_schema.employee_id,
                                                             Attendance.is_punchin == True).first()
        if  Attendance_record:
             raise ValueError("Already Punched IN ")

        Attendance_record = Attendance(employee_id = PunchInSchema.employee_id,
                                        workmode = PunchInSchema.work_mode,
                                        attendance_date = today,
                                        punch_in = datetime.now(),
                                        is_punchin = True,
                                        attendance_staus = AttendanceStatus.PRESENT
                                        )

        try:
            self.db.add(Attendance_record)
            self.db.commit()
            self.db.refresh(Attendance_record)
        except Exception:
            self.db.rollback()
            raise 
        return None

    def punch_out(self,punch_in_schema : PunchInSchema):
         today = datetime.today()
         attendance_record = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                             Attendance.employee_id == punch_in_schema.employee_id,
                                                             Attendance.is_punchout == True).first()
         if attendance_record :
              raise ValueError("employee already Punchout")
         
         attendance_record : Attendance = self.db.query(Attendance).filter(Attendance.attendance_date == today,
                                                              Attendance.employee_id == punch_in_schema.employee_id).first()
         
         if not attendance_record:
              raise ValueError(f"Attendance record not Found {today}")
         attendance_record.is_punchout = True
         attendance_record.punchout_time = datetime.now()

         self.db.commit()
         self.db.refresh(attendance_record)
         
         return attendance_record

    def get_today_attendance(self,organisation_id):
         
         today = date.today()
         attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              Attendance.attendance_date == today).all()
         if not attendance_record:
              raise ValueError(f"{today} :Attendacne record not found ")
         return attendance_record

    def get_employee_attendance(self,employee_id):
         employee_attendance_record = self.db.query(Attendance).filter(Attendance.employee_id == employee_id).all()
         if not employee_attendance_record:
              raise ValueError("employee attendance record not found")
         return None
    

    def update_attendance(self,employee_id : uuid ,Attendance_date :date, update_attendacne :AttendanceUpdate):
         attendance_record = self.db.query(Attendance).filter(Attendance.employee_id == employee_id,
                                                              Attendance.attendance_date == date).first()
         if not attendance_record: 
              raise ValueError("Attenadance Record not Found")
         
         for feild,value in update_attendacne.model_dump().items():
              setattr(attendance_record,feild,value)

         try :
            self.db.commit()
            self.db.refresh(attendance_record)
         except Exception:
            self.db.rollback()
            raise ValueError("unknow error found")

         return attendance_record

    def mark_absent(self,employee_id :uuid ,attedance_date : date):
         attedance_record = self.db.query(Attendance).filter(Attendance.attendance_date == attedance_date,
                                                             Attendance.employee_id == employee_id).first()
         
         if not attedance_record :
              raise ValueError(f"no record found on {attedance_date} for ")
         attedance_record.status = AttendanceStatus.ABSENT
         try :
              self.db.commit()
              self.db.refresh(attedance_record)
         except Exception:
              self.db.rollback()
         return attedance_record
    
    

    def get_attendance_by_date(self,date :date,organisation_id :uuid):
        attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              Attendance.attendance_date == date).all()
        if not attendance_record:
              raise ValueError(f"{date} :Attendacne record not found ")
        return attendance_record


    def get_attendance_by_month(self,month : int,organisation_id : uuid ):
         
         attendance_record = self.db.query(Attendance).filter(Attendance.organisation_id == organisation_id,
                                                              extract("month", Attendance.attendance_date) == month).all()# extract the month from the date 
         if not attendance_record:
              raise ValueError(f"{month} :Attendacne record not found ")
         return attendance_record


    def get_employee_today(self):
         return None

    def delete_attendance(self):
         return None