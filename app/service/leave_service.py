import uuid
from typing import List

from app.enums.employee_status import EmployeeStatus
from app.models import LeaveRequest, Employee
from app.repo import employee_repo
from app.repo.employee_repo import EmployeeRepo
from app.repo.leave_repo import LeaveRepo
from app.schemas.leave_request_schema import LeaveCreate, LeaveApproval, LeaveResponse, LeaveRecordResponseList, \
    LeaveRecordResponse, LeaveResponseWithEmployeeCode


class LeaveService:
    def __init__(self, leave_repo : LeaveRepo, employee_repo : EmployeeRepo):
        self.leave_repo = leave_repo
        self.employee_repo = employee_repo

    def apply_leave(self, leave_schema : LeaveCreate,employee_id : uuid.UUID,) -> LeaveResponse:
        return self.leave_repo.apply_leave(leave_schema,employee_id)

    def get_leave_by_id(self, leave_id : int) -> LeaveRequest:
        leave_record = self.leave_repo.get_leave(leave_id)
        if leave_record is None:
            raise ValueError(f"Leave with id {leave_id} does not exist")
        return leave_record

    def get_employee_leave(self,employee_code : str, organisation_id : uuid.UUID) -> LeaveRecordResponseList:
        employee = self.employee_repo.get_employee_by_employee_code(employee_code= employee_code,organisation_id = organisation_id)
        if employee is None:
            raise ValueError(f"Employee with id {employee_code} does not exist")
        leave_record = self.leave_repo.get_employee_leaves(employee.id,organisation_id=organisation_id)

        if leave_record is None:
            raise ValueError(f" Leaves with for {employee_code} does not exist")
        return LeaveRecordResponseList(
            employee_code = employee_code,
            employee_name=employee.user.full_name,
            leave_response = leave_record
        )

    def get_pending_leave_by_department(self,department_name : str, organisation_id : uuid.UUID ) -> set[type[LeaveResponseWithEmployeeCode]] :
            employee = self.employee_repo.get_employee_by_department_name(department_name= department_name,organisation_id= organisation_id)
            leave_records = set()
            for leave_record in self.leave_repo.get_pending_employees_leaves(employee_id= employee.id,organisation_id = organisation_id):
                leave_records.add(leave_record)

            return leave_records

    def get_pending_leave(self,organisation_id : uuid.UUID ) -> List[type[LeaveResponseWithEmployeeCode]] :
        leave_record = self.leave_repo.get_pending_leaves(organisation_id= organisation_id)
        if leave_record is None:
            raise ValueError(f"No leave record found ")
        return leave_record


    def get_employee_pending_leave(self,employee_code : str,organisation_id :uuid.UUID) -> LeaveRecordResponseList:
        employee = self.employee_repo.get_employee_by_employee_code(employee_code= employee_code,organisation_id= organisation_id)
        leave_record = self.leave_repo.get_pending_employee_leaves(employee_id= employee.id,organisation_id= organisation_id)
        return LeaveRecordResponseList(
            emploiye_name = employee.user.full_name,
            employee_code  = employee.code,
            leave_response = leave_record
        )


    def approve_leave(self,organisation_id : uuid.UUID, leave_approve_schema : LeaveApproval, approved_by : uuid.UUID,employee_code :str) -> LeaveResponseWithEmployeeCode:
        employee  = self.employee_repo.get_employee_by_employee_code(employee_code= employee_code,organisation_id= organisation_id)
        if employee is None:
            raise ValueError(f"Employee with id {employee_code} does not exist")
        leave_record = self.leave_repo.approve_leave(leave_id= leave_approve_schema.leave_id, approver_by=approved_by ,employee_id= employee.id)
        if leave_record is None:
            raise ValueError(f"Leaves with for {employee.employee_code} does not exist")
        return leave_record

    def reject_leaves(self,organisation_id : uuid.UUID, leave_approve_schema : LeaveApproval, approved_by : uuid.UUID,employee_code :str) -> LeaveResponseWithEmployeeCode:
        employee  = self.employee_repo.get_employee_by_employee_code(employee_code= employee_code,organisation_id= organisation_id)
        if employee is None:
            raise ValueError(f"Employee with id {employee_code} does not exist")
        leave_record = self.leave_repo.rejecte_leave(leave_id= leave_approve_schema.leave_id,employee_id= employee.id)
        if leave_record is None:
            raise ValueError(f"Leaves with for {employee.employee_code} does not exist")
        return leave_record

    def cancel_leave(self,organisation_id : uuid.UUID, leave_approve_schema : LeaveApproval ,employee_code :str) -> LeaveResponseWithEmployeeCode:
        employee  = self.employee_repo.get_employee_by_employee_code(employee_code= employee_code,organisation_id= organisation_id)
        if employee is None:
            raise ValueError(f"Employee with id {employee_code} does not exist")
        leave_record = self.leave_repo.cancel_leave(leave_id= leave_approve_schema.leave_id ,employee_id= employee.id)
        if leave_record is None:
            raise ValueError(f"Leaves with for {employee.employee_code} does not exist")
        return leave_record