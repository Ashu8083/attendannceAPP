import uuid

from sqlalchemy import ForeignKey, String,Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class EmployeeDocuments(Base, TimestampMixin):
    __tablename__ = "employee_documents"
    __table_args__ = (
        Index("employee_id_idx", "employee_id", unique=True),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employees.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One document record per employee
    )

    photo_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    aadhaar_document_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    pan_document_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    resume_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    employee = relationship(
        "Employee",
        back_populates="documents",
    )