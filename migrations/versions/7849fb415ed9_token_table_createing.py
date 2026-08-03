"""token table createing

Revision ID: 7849fb415ed9
Revises: 2f15795b7609
Create Date: 2026-08-03 11:33:07.748282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7849fb415ed9'
down_revision: Union[str, Sequence[str], None] = '2f15795b7609'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.create_table(
        "token",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False),
        sa.Column("expires_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["userdevice.id"],
            ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id")
    )

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "token",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("device_id", sa.UUID(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column("is_revoked", sa.Boolean(), nullable=False),
        sa.Column("expires_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("created_at", postgresql.TIMESTAMP(), nullable=False),
        sa.Column("updated_at", postgresql.TIMESTAMP(), nullable=False),
        sa.ForeignKeyConstraint(
            ["device_id"],
            ["userdevice.id"],
            name=op.f("token_device_id_fkey"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("token_pkey")),
    )
