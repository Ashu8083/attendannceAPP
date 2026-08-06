
# import datetime
import uuid
from datetime import date

from dateutil.utils import today

from app.enums.work_mode import WorkMode

from app.repo.attendance_record_repo import AttendanceRepo
from app.repo.employee_repo import EmployeeRepo
from app.schemas.attendance_schema import  AttendanceUpdate, PunchInOutSchema
from app.core.logging_config import logger
from app.helperFunction.locationcheker import get_distance
from app.exceptions.custom_exception import (
    AttendanceNotFound,
    TodayAttendanceAlreadyTaken,
    EmployeeNotFound)
from app.repo.employee_face_repo import EmployeeFaceRepo
from app.face_model.face_embedding import extract_face_embedding_db
from app.face_model.face_matcher import arcface_match


class AttendanceService:
    def __init__(self,attendance_record_repo : AttendanceRepo,employee_repo : EmployeeRepo,employee_face_repo: EmployeeFaceRepo,):

        self.employee_repo = employee_repo
        self.attendance_record_repo = attendance_record_repo
        self.employee_face_repo = employee_face_repo


    async def punch_in_attendance(self,face_image : bytes
                                  ,punch_in_out_schema,
                                  employee_id :uuid.UUID ,
                                  organisation_id : uuid.UUID):
        employee = self.employee_repo.get_employee_by_employee_id(employee_id=employee_id,organisation_id=organisation_id)
        if not employee:
            raise EmployeeNotFound
        if employee.work_mode == WorkMode.WFO:
                     distance = get_distance(office_latitude=employee.organisation.latitude,
                                office_longitude=employee.organisation.longitude,
                                employee_latitude=punch_in_out_schema.employee_latitude,
                                employee_longitude=punch_in_out_schema.employee_longitude )

                     if distance > employee.organisation.allowed_radius:
                        logger.info(f"Employee {employee.employee_code} is not in the office permisies")
                        raise

        attendance = self.attendance_record_repo.today_attendance_employee_is_punch_in(organisation_id= organisation_id,employee_id = employee_id)
        if attendance:
            logger.info("User Already Punched")
            raise TodayAttendanceAlreadyTaken
        live_embedding = extract_face_embedding_db(face_image)
        store_embedding = self.employee_face_repo.get_employee_face_record(employee_id)
        THRESHOLD = 0.65
        face_similarity,face_confedence = arcface_match(
                                            live_embedding=live_embedding ,
                                            stored_embedding=store_embedding )

        if face_similarity > THRESHOLD:
            return self.attendance_record_repo.punch_in(employee_id, workMode= employee.work_mode,
                                                        organisation_id=organisation_id)
        else :
            raise



    def punch_out_attendance(self,face_image : bytes,punch_out : PunchInOutSchema , organisation_id : uuid.UUID,employee_id : uuid.UUID):
        employee = self.employee_repo.get_employee_by_employee_id(employee_id=employee_id,organisation_id=organisation_id)
        if not employee:
            logger.error("employee s% of organisation %s is not found",employee_id ,organisation_id)
            raise EmployeeNotFound
        attendance = self.attendance_record_repo.today_attendacnce_employee_is_punch_out(organisation_id= organisation_id,employee_id = employee_id)
        if attendance:
            logger.info("Employee %s  of Organisation % Attendance Already Taken", employee_id,organisation_id)
            raise TodayAttendanceAlreadyTaken

        if employee.work_mode == WorkMode.WFO :

                distance = get_distance(office_latitude=employee.organisation.latitude
                                     ,office_longitude=employee.organisation.longitude
                                     ,employee_longitude=punch_out.employee_longitude
                                     ,employee_latitude=punch_out.employee_latitude)

                if distance > employee.organisation.allowed_radius:
                    logger.error("Employee %s is not in the office permisiess",employee_id)
                    raise
        live_embedding = extract_face_embedding_db(face_image)
        store_embedding = self.employee_face_repo.get_employee_face_record(employee_id)
        THRESHOLD = 0.65
        face_similarity, face_confedence = arcface_match(
            live_embedding=live_embedding,
            stored_embedding=store_embedding)

        if face_similarity > THRESHOLD:
         return self.attendance_record_repo.punch_out(employee_id=employee_id,organisation_id=organisation_id)
        else:
            raise ValueError("FaceNotMatch")


    def get_today_attendance(self,organisation_id : uuid.UUID):
        attendance = self.attendance_record_repo.get_today_attendance(organisation_id)
        if not attendance:
            raise AttendanceNotFound
        return attendance

    def get_employee_attendance(self,organisation_id,employee__id : uuid.UUID):
        attendance_record = self.attendance_record_repo.get_employee_attendance(employee_id=employee__id , organisation_id=organisation_id)
        if not attendance_record:
            raise AttendanceNotFound
        return   attendance_record

    # get
    def get_month_attendance(self,month : int,organisation_id : uuid.UUID):
        attendacne_record =   self.attendance_record_repo.get_attendance_by_month(month,organisation_id)
        if not attendacne_record:
            raise AttendanceNotFound
        return attendacne_record

    def get_today_employee_attendance(self,organisation_id : uuid.UUID,employee_id : uuid.UUID):
        return self.attendance_record_repo.get_employee_today_attendance(employee_id=employee_id , organisation_id=organisation_id)

    def update_employee_attendance(self,organisation_id : uuid.UUID, attendance_update_schema : AttendanceUpdate ):
        employee_id = self.employee_repo.get_employee_id(organisation_id,employee_code=attendance_update_schema.employee_code)

        return self.attendance_record_repo.update_attendance(organisation_id,employee_id=employee_id,update_attendacne= attendance_update_schema)

    def absent_employee(self, organisation_id: uuid.UUID, attendance_date: date):
        employees = self.employee_repo.get_all_employee(organisation_id)
        present_employee_ids = self.attendance_record_repo.get_present_employee(
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
        attendance_record_repo = self.attendance_record_repo.get_employee_attendance_by_date(employee_id=employee.id,organisation_id=organisation_id,attendance_date = attendance_date)
        if attendance_record_repo:
            raise ValueError("Attendance record already exists")
        self.attendance_record_repo.mark_absent(organisation_id=organisation_id,employee= employee,attedance_date= attendance_date)

    def get_employee_attendance_by_date(self,attendance_date : date,organisation_id : uuid.UUID,employee_id : uuid.UUID):
        return self.attendance_record_repo.get_employee_attendance_by_date(attendance_date=attendance_date,organisation_id=organisation_id,employee_id=employee_id)


