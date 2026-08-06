import uuid
from typing import List
from uuid import UUID
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Employee
from app.models.leave_record_model import LeaveRequest
from app.schemas import organisation_schema
from app.schemas.leave_request_schema import *
from app.enums.leave_status import LeaveStatus


class LeaveRepo:

    def __init__(self, db: Session):
        self.db = db

    def apply_leave(self, leave: LeaveCreate,employee_id : UUID,organisation_id : UUID) -> LeaveResponse:
        leave_request = LeaveRequest(
            employee_id=employee_id,
            organisation_id = organisation_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            status=LeaveStatus.PENDING,
            reason=leave.reason,
        )

        try:
            self.db.add(leave_request)
            self.db.commit()
            self.db.refresh(leave_request)
        except Exception:
            self.db.rollback()
            raise

        return leave_request
    def get_all_employees_leaves(self,organisation_id : uuid.UUID)-> List[type[LeaveResponseWithEmployeeCode]]:
        leave_record = self.db.query(LeaveRequest).filter(LeaveRequest.organisation_id == organisation_id).all()
        return leave_record
    def get_leave_by_leaveID(self, leave_id: uuid.UUID):
        leave = (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.id == leave_id)
            .first()
        )

        if not leave:
            raise ValueError("Leave request not found")

        return leave

    def get_employee_leaves(self, employee_id: uuid.UUID,organisation_id :uuid.UUID) -> List[type[LeaveResponse]]:
        leaves_records = (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.employee_id == employee_id,
                     LeaveRequest.organisation_id == organisation_id)
            .all()
        )

        if not leaves_records:
            raise ValueError("No leave requests found")

        return leaves_records

    def get_pending_employee_leaves(self,organisation_id :uuid.UUID,employee_id :uuid.UUID)-> List[type[LeaveResponse]]:
        return (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.organisation_id == organisation_id,
                    LeaveRequest.employee_id == employee_id,
                    LeaveRequest.status == LeaveStatus.PENDING)
            .all()
        )
    def get_pending_leaves(self,organisation_id :uuid.UUID) -> List[type[LeaveResponseWithEmployeeCode]]:
        leaves_records = self.db.query(LeaveRequest).filter(LeaveRequest.organisation_id == organisation_id,
                                                            LeaveRequest.status == LeaveStatus.PENDING).all()
        return leaves_records

    def approve_leave(
        self,
        leave_id: uuid.UUID,
        approver_by: uuid.UUID,
        employee_id: UUID,
    )-> type[LeaveResponseWithEmployeeCode]:
        leave = self.db.query(LeaveRequest).filter(LeaveRequest.id == leave_id,
                                                   LeaveRequest.employee_id == employee_id
                                                   ).first()

        if leave.status != LeaveStatus.PENDING:
            raise ValueError("Leave request already processed")

        leave.status = LeaveStatus.APPROVED
        leave.approved_by = approver_by
        leave.approved_at = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(leave)
        except Exception:
            self.db.rollback()
            raise

        return leave

    def rejecte_leave(
        self,
        leave_id: uuid.UUID,
        employee_id: uuid.UUID,
    )-> type[LeaveResponseWithEmployeeCode]:
        leave = self.db.query(LeaveRequest).filter(LeaveRequest.id == leave_id,
                                                   LeaveRequest.employee_id == employee_id
                                                   ).first()

        if leave.status != LeaveStatus.PENDING:
            raise ValueError("Leave request already processed")

        leave.status = LeaveStatus.REJECTED
        leave.approved_at = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(leave)
        except Exception:
            self.db.rollback()
            raise

        return leave

    def canceled_leave(self, leave_id: uuid.UUID,employee_id: uuid.UUID):
        leave = self.db.query(LeaveRequest).filter(LeaveRequest.id == leave_id,
                                                   LeaveRequest.employee_id == employee_id
                                                   ).first()

        if leave.status == LeaveStatus.APPROVED:
            raise ValueError("Approved leave cannot be cancelled")

        leave.status = LeaveStatus.CANCELLED

        try:
            self.db.commit()
            self.db.refresh(leave)
        except Exception:
            self.db.rollback()
            raise

        return leave

    def delete_leave(self, leave_id: uuid.UUID):
        leave = self.get_leave(leave_id)

        try:
            self.db.delete(leave)
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise
    def employees_on_leaves(self, employee_id: uuid.UUID , organisation_id: uuid.UUID)-> List[type[LeaveResponseWithEmployeeCode]]:
        leaves = self.db.query(LeaveRequest).filter(LeaveRequest.employee_id == employee_id,
                                                    LeaveRequest.organisation_id == organisation_id,
                                                    LeaveRequest.status == LeaveStatus.APPROVED).all()
        return leaves