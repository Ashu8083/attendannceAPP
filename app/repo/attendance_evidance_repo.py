from sqlalchemy.orm import Session
from uuid import UUID
from app.enums.attandance_status import TypeAttendance
from app.models import AttendanceEvidence


class AttendanceEvidenceRepo():
        def  __init__ (self, db:Session):
            self.db = db


        def create_attendance_evidence(self
                                        ,attendance_id : UUID
                                       ,face_match_score : float,
                                       type : TypeAttendance,
                                       face_profile_url : str):

            attendance_evidence = AttendanceEvidence(
                attendance_record_id = attendance_id,
                face_match_score = face_match_score,
                type = type,
                face_profile_url  = face_profile_url
            )
            self.db.add(attendance_evidence)
            self.db.flush()
            return attendance_evidence


        def get_attendance_evidence(self, attendance_evidence_id:UUID) -> AttendanceEvidence:
            attendance_evidence = self.db.query(AttendanceEvidence).filter(
                AttendanceEvidence.attendance_id == attendance_evidence_id
            )
