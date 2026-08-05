
from uuid import UUID
import uuid
from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey,Index
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy.orm import mapped_column

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class EmployeeFaceModel(Base,TimestampMixin):
    __tablename__ = "employee_face"
    __table_args__ = (
         Index('idx_employee_face_id',
               'employee_id',
               'id'),
     )

    id : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default = uuid.uuid4
    )
    employee_id  : Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey( "employees.id"),
    )
    embedding: Mapped[list[float]] = mapped_column(
        JSONB,
        nullable=False,

    )

    employee = relationship("Employee",
                            back_populates="employee_face",
                          )
