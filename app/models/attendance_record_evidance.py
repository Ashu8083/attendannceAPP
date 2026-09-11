import uuid

from sqlalchemy import UUID, ForeignKey, Float,String ,Enum
from sqlalchemy.orm import Mapped,relationship
from sqlalchemy.testing.schema import mapped_column
from app.db.database import Base

from app.db.timestamp import TimestampMixin
from app.enums.attandance_status import TypeAttendance


class AttendanceEvidence(Base,TimestampMixin):
    __tablename__ = "attendance_record_evidence"
    id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    attendance_record_id : Mapped[uuid.UUID]\
        = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("attendance_record.id"),
        primary_key=True,
        nullable=False,
    )
    face_match_score: Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    type : Mapped[uuid.UUID] = mapped_column(
        Enum(TypeAttendance),
        nullable=True,
    )
    face_profile_url : Mapped[str] = mapped_column(
        String,
    )
    attendance_record = relationship(
        "Attendance",
    back_populates="attendance_evidence",)
