import uuid
from datetime import date

from dateutil.utils import today

from app.enums.work_mode import WorkMode
from app.models import Employee
from app.repo import attendance_record_repo, employee_repo
from app.repo.attendance_record_repo import AttendanceRepo
from app.repo.employee_repo import EmployeeRepo
from app.schemas.attendance_schema import  AttendanceUpdate, PunchInOutSchema
from app.service import organisation_service
from app.core.logging_config import logger
from app.helperFunction.locationcheker import get_distance
from app.service.face_services.InsightFaceService import InsightFaceService

class AttendanceService:
    def __init__(self,attendacnce_record_repo : AttendanceRepo,employee_repo : EmployeeRepo, face_service : InsightFaceService):
        self.attendacnce_record_repo = attendacnce_record_repo
        self.employee_repo = employee_repo
        self.face_service = face_service


    def punch_in_attendance(self,punchInOutSchema: PunchInOutSchema  ,employee_id :uuid.UUID ,organisation_id : uuid.UUID,image : bytes):
        employee = self.employee_repo.get_employee_by_employee_id(employee_id=employee_id)
        if not employee:
            raise

        distance = get_distance(office_latitude=employee.organisation.office_latitude,
                                office_longitude=employee.organisation.office_longitude,
                                employee_latitude=punchInOutSchema.employee_latitude,
                                employee_longitude=punchInOutSchema.employee_longitude)
        
        if employee.work_mode == WorkMode.WFO :
            if distance > employee.organisation.allowed_rediuse:
                logger.info(f"Employee {employee.employee_code} is not in the office permisiess")
                raise

        attendance = self.attendacnce_record_repo.today_attendance_employee_is_punch_in(organisation_id= organisation_id,employee_id = employee_id)
        if attendance:
            logger.info("User Already Punched")
            raise
        face_embending = self.face_service.generate_embedding(image_bytes=image)

        if not employee.employee_face_embedding : 
            raise   
        face_check = self.face_service.verify_embedding(new_embedding=face_embending, stored_embedding= employee.employee_face_embedding)
        if face_check == False : 
            raise 
        attendance_record = self.attendacnce_record_repo.punch_in(employee_id,workMode= employee.work_mode,organisation_id=organisation_id)

        return attendance_record

    def punch_out_attendance(self,punch_out : PunchInOutSchema , organisation_id : uuid.UUID,employee_id : uuid.UUID,image : bytes):
        
        employee = self.employee_repo.get_employee_by_employee_id(employee_id=employee_id,organisation_id=organisation_id)

        if not employee:
            logger.error("employee %s of organisation %s is not found",employee_id ,organisation_id)
            raise
        attendance = self.attendacnce_record_repo.today_attendacnce_employee_is_punch_out(organisation_id= organisation_id,employee_id = punch_out.employee_id)
        if attendance:
            logger.info("Employee %s  of Organisation %s Already Punched ", employee_id,organisation_id)
            raise

        distance = get_distance(office_latitude=employee.organisation.office_latitude
                                ,office_longitude=employee.organisation.office_longitude
                                ,employee_longitude=punch_out.employee_longitude
                                ,employee_latitude=punch_out.employee_latitude)
        if employee.work_mode == WorkMode.WFO :
            if distance > employee.organisation.allowed_rediuse:
                logger.error("Employee %s is not in the office permisiess",employee_id)
                raise

        face_embending = self.face_service.generate_embedding(image_bytes=image)

        if not employee.employee_face_embedding : 
            raise   
        face_check = self.face_service.verify_embedding(new_embedding=face_embending, stored_embedding= employee.employee_face_embedding)

        if face_check == False : 
            raise 
        return self.attendacnce_record_repo.punch_out(employee_id=employee_id,organisation_id=organisation_id)


    def get_today_attendance(self,organisation_id : uuid.UUID):
        return self.attendacnce_record_repo.get_today_attendance(organisation_id)

    def get_employee_attendance(self,organisation_id,employee__id : uuid.UUID):
        return  self.attendacnce_record_repo.get_employee_attendance(employee_id=employee__id , organisation_id=organisation_id)

    # get
    def get_month_attendance(self,month : int,organisation_id : uuid.UUID):
        return  self.attendacnce_record_repo.get_attendance_by_month(month,organisation_id)

    def get_today_employee_attendance(self,organisation_id : uuid.UUID,employee_id : uuid.UUID):
        return self.attendacnce_record_repo.get_employee_today_attendance(employee_id=employee_id , organisation_id=organisation_id)

    def update_employee_attendance(self,organisation_id : uuid.UUID, attendance_update_schema : AttendanceUpdate ):
        employee_id = self.employee_repo.get_employee_id(organisation_id,employee_code=attendance_update_schema.employee_code)

        return self.attendacnce_record_repo.update_attendance(organisation_id,employee_id=employee_id[0],update_attendacne= attendance_update_schema)

    def absent_employee(self, organisation_id: uuid.UUID, attendance_date: date):
        employees = self.employee_repo.get_all_employee(organisation_id)
        present_employee_ids = self.attendacnce_record_repo.get_present_employee(
            organisation_id,
            attendance_date,
        )
        absent_employees = []
        for employee in employees:
            if employee.id not in present_employee_ids:
                absent_employees.append(employee.employee_code)

        return absent_employees
    def marked_absent_employee(self, organisation_id: uuid.UUID, attendance_date: date, employee_code: str):
        employee  =self.employee_repo.get_employee_by_employee_code(organisation_id,employee_code=employee_code)
        attendance_record_repo = self.attendacnce_record_repo.get_employee_attendance_by_date(employee_id=employee.id,organisation_id=organisation_id,attendance_date = attendance_date)
        if attendance_record_repo:
            raise ValueError("Attendance record already exists")
        self.attendacnce_record_repo.mark_absent(organisation_id=organisation_id,employee= employee,attedance_date= attendance_date)

    def get_employee_attendance_by_date(self,attendance_date : date,organisation_id : uuid.UUID,employee_id : uuid.UUID):
        return self.attendacnce_record_repo.get_employee_attendance_by_date(attendance_date=attendance_date,organisation_id=organisation_id,employee_id=employee_id)

