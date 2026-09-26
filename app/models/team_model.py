import uuid
from datetime import datetime

from sqlalchemy import ForeignKey, String, Integer, UUID, DateTime, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.db.timestamp import TimestampMixin


class Team(Base, TimestampMixin):
    __tablename__ = "teams"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("department.id"),
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    team_head: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("employees.id"),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    is_activated: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    delete_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    department = relationship(
        "DepartmentModel",
        back_populates="team",
    )

    # head = relationship(
    #     "Employee",
    #     foreign_keys=[team_head],
    # )