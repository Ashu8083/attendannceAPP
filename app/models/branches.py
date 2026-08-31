from sqlalchemy.orm import Mapped, mapped_column, Relationship
import uuid
from sqlalchemy import Integer, String, UUID, ForeignKey, Float, Boolean
from app.db.database import Base


class Branch(Base):
    __tablename__ = "branches"

    id :Mapped[uuid.UUID] = mapped_column(
                       UUID(as_uuid=True),
                        primary_key=True,
                       default=uuid.uuid4,
                            )
    branch_name: Mapped[str]=mapped_column(
         String(80),
    )
    organisation_id : Mapped[uuid.UUID] =  mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisation.id",ondelete="CASCADE"),
    )
    address:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    city:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    state:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    zip_code:Mapped[str] = mapped_column(
        String(80),
        nullable=False,
    )
    longitude:Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    latitude:Mapped[float] = mapped_column(
        Float,
        nullable=True,
    )
    geofencing : Mapped[int] = mapped_column(
        Integer,
        default=100,
    )
    grace_period : Mapped[int] = mapped_column(
        Integer,
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )
    organisation = Relationship(
                "Organisation",
                 back_populates="branch",
    )
