import uuid
from datetime import datetime

from sqlalchemy.orm import Session

from app.models.leave_record_model import LeaveRequest
from app.schemas.leave_request_schema import LeaveCreate, LeaveUpdate
from app.enums.leave_status import LeaveStatus


class LeaveRepo:

    def __init__(self, db: Session):
        self.db = db

    def apply_leave(self, leave: LeaveCreate):
        leave_request = LeaveRequest(
            employee_id=leave.employee_id,
            start_date=leave.start_date,
            end_date=leave.end_date,
            status=LeaveStatus.PENDING
        )

        try:
            self.db.add(leave_request)
            self.db.commit()
            self.db.refresh(leave_request)
        except Exception:
            self.db.rollback()
            raise

        return leave_request

    def get_leave(self, leave_id: uuid.UUID):
        leave = (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.id == leave_id)
            .first()
        )

        if not leave:
            raise ValueError("Leave request not found")

        return leave

    def get_employee_leaves(self, employee_id: uuid.UUID):
        leaves = (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.employee_id == employee_id)
            .all()
        )

        if not leaves:
            raise ValueError("No leave requests found")

        return leaves

    def get_pending_leaves(self):
        return (
            self.db.query(LeaveRequest)
            .filter(LeaveRequest.status == LeaveStatus.PENDING)
            .all()
        )

    def approve_leave(
        self,
        leave_id: uuid.UUID,
        approver_id: uuid.UUID
    ):
        leave = self.get_leave(leave_id)

        if leave.status != LeaveStatus.PENDING:
            raise ValueError("Leave request already processed")

        leave.status = LeaveStatus.APPROVED
        leave.approved_by = approver_id
        leave.approved_at = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(leave)
        except Exception:
            self.db.rollback()
            raise

        return leave

    def reject_leave(
        self,
        leave_id: uuid.UUID,
        approver_id: uuid.UUID
    ):
        leave = self.get_leave(leave_id)

        if leave.status != LeaveStatus.PENDING:
            raise ValueError("Leave request already processed")

        leave.status = LeaveStatus.REJECTED
        leave.approved_by = approver_id
        leave.approved_at = datetime.now()

        try:
            self.db.commit()
            self.db.refresh(leave)
        except Exception:
            self.db.rollback()
            raise

        return leave

    def cancel_leave(self, leave_id: uuid.UUID):
        leave = self.get_leave(leave_id)

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