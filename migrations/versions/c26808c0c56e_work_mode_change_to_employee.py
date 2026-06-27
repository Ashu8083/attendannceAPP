"""work mode change to employee

Revision ID: c26808c0c56e
Revises: 1cdba70abacd
Create Date: 2026-06-26 16:18:09.683158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c26808c0c56e'
down_revision: Union[str, Sequence[str], None] = '1cdba70abacd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    # Create the enum type first

    workmode = postgresql.ENUM(

        "WFH",

        "WFO",

        name="workmode"

    )

    workmode.create(op.get_bind(), checkfirst=True)

    # Drop old column

    op.drop_column("attendance_records", "work_mode")

    # Add new column

    op.add_column(

        "employees",

        sa.Column(

            "work_mode",

            workmode,

            nullable=False,

            server_default="WFO"   # Remove if employees table is empty

        )

    )

    # Optional: remove the default after existing rows are populated

    op.alter_column(

        "employees",

        "work_mode",

        server_default=None

    )

from sqlalchemy.dialects import postgresql

def downgrade() -> None:
    op.drop_column("employees", "work_mode")

    op.add_column(
        "attendance_records",
        sa.Column(
            "work_mode",
            sa.VARCHAR(length=3),
            nullable=False
        )
    )

    workmode = postgresql.ENUM(
        "WFH",
        "WFO",
        name="workmode"
    )

    workmode.drop(op.get_bind(), checkfirst=True)