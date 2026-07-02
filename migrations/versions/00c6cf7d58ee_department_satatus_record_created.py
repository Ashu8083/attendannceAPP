"""department satatus record created

Revision ID: 00c6cf7d58ee
Revises: 9393994c3496
Create Date: 2026-07-02 10:07:58.619006

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from app.enums.departement_status import DepartmentStatusEnum

# revision identifiers, used by Alembic.
revision: str = '00c6cf7d58ee'
down_revision: Union[str, Sequence[str], None] = '9393994c3496'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

department_status = sa.Enum(DepartmentStatusEnum, name="department_status")

department_status_enum = postgresql.ENUM(

    "ACTIVATE",
    "DEACTIVATE",
    "DELETED",
    name="departmentstatusenum",
)

def upgrade():
    department_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column(
        "department",
        sa.Column(
            "department_status",
            department_status_enum,
            nullable=False,
            server_default="ACTIVATE",
        ),
    )

    op.drop_constraint(
        op.f("department_shift_time_fkey"),
        "department",
        type_="foreignkey",
    )

    op.drop_column("department", "shift_time")

def downgrade():

    op.add_column(

        "department",

        sa.Column("shift_time", sa.Integer(), nullable=False),

    )

    op.create_foreign_key(

        op.f("department_shift_time_fkey"),

        "department",

        "shift",

        ["shift_time"],

        ["id"],

    )

    op.drop_column("department", "department_status")

    department_status_enum.drop(op.get_bind(), checkfirst=True)