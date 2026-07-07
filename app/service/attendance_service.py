import uuid
from datetime import date

from app.enums.work_mode import WorkMode
from app.repo import attendance_record_repo, employee_repo
from app.repo.attendance_record_repo import AttendanceRepo
from app.repo.employee_repo import EmployeeRepo
from app.schemas.attendance_schema import  PunchInSchema,PunchOutSchema,AttendanceUpdate
from app.service import organisation_service


class AttendanceService:
    def __init__(self,attendacnce_record_repo : AttendanceRepo,employee_repo : EmployeeRepo):
        self.attendacnce_record_repo = attendacnce_record_repo
        self.employee_repo = employee_repo


    def punch_in_attendance(self,  employee_id :uuid.UUID ,organisation_id : uuid.UUID):
        attendance = self.attendacnce_record_repo.today_attendance_employee_is_punch_in(organisation_id= organisation_id,employee_id = employee_id)
        if attendance:
            return attendance

        return self.attendacnce_record_repo.punch_in(employee_id,workMode= WorkMode.WFH,organisation_id=organisation_id)

    def punch_out_attendance(self,punch_out : PunchOutSchema , organisation_id : uuid.UUID):
        attendance = self.attendacnce_record_repo.today_attendacnce_employee_is_punch_out(organisation_id= organisation_id,employee_id = punch_out.employee_id)
        if attendance:
            return attendance
        return self.attendacnce_record_repo.punch_out(punch_out)

    def get_today_attendace(self,organisation_id : uuid.UUID):
        return self.attendacnce_record_repo.get_today_attendance(organisation_id)

    def get_employee_employee_attendance(self,organisation_id,employee__id : uuid.UUID):
        return  self.attendacnce_record_repo.get_employee_attendance(employee_id=employee__id , organisation_id=organisation_id)

    def get_month_attendance(self,month : int,organisation_id : uuid.UUID):
        return  self.attendacnce_record_repo.get_attendance_by_month(month,organisation_id)

    def get_today_employee_attendance(self,organisation_id : uuid.UUID,employee_id : uuid.UUID):
        return self.attendacnce_record_repo.get_employee_today_attendance(employee_id=employee_id , organisation_id=organisation_id)

    def update_employee_attendance(self,organisation_id : uuid.UUID, attendance : AttendanceUpdate ):
        employee_id = self.employee_repo.get_employee_id(organisation_id,employee_code=attendance.employee_code)

        return self.attendacnce_record_repo.update_attendance(organisation_id,employee_id=employee_id[0],update_attendacne= attendance)