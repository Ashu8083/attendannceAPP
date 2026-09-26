
import uuid
from operator import index

from sqlalchemy import Index
from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.dialects.postgresql import ENUM as SQLEnum
from sqlalchemy.orm import Mapped , mapped_column,relationship



from app.db.database import Base
from app.db.timestamp import TimestampMixin
from app.enums.departement_status import DepartmentStatusEnum


class DepartmentModel(Base,TimestampMixin):

    __tablename__ = "department"

    id : Mapped[int] = mapped_column(
        Integer,
        primary_key= True,
        autoincrement = True,
    )
    __table_args__ = (
        UniqueConstraint(
            "organisation_id",
            "name",
            name = "uq_department_org_name"
        ),
        Index(
            "organisation_id",
                "name",)
    )
    name : Mapped[str] = mapped_column(
        String(25)
    )
    department_head : Mapped[uuid.UUID] = mapped_column(
                    UUID(as_uuid=True),
                    ForeignKey("employees.id"),
                    nullable = False
    )

    organisation_id: Mapped[uuid.UUID] = mapped_column(
                                UUID(as_uuid=True),
                                ForeignKey("organisation.id"),
                                nullable=False
                                )

    branch_id : Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("branches.id"),
        nullable = True
    )
    department_status : Mapped[DepartmentStatusEnum]= mapped_column(
            SQLEnum(DepartmentStatusEnum)
    )

    organization = relationship(
    "Organisation",
    back_populates="departments"
    )

    team = relationship(
        "Team",
        back_populates="department",
        cascade="all, delete-orphan",
    )
    branch = relationship(
        "Branch",
        back_populates="department",
    )