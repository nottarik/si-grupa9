"""drive_sync_schedule: add language column for the scheduled import

Revision ID: 006_drive_schedule_language
Revises: 005_drive_sync_schedule
Create Date: 2026-06-08
"""
import sqlalchemy as sa
from alembic import op

revision = "006_drive_schedule_language"
down_revision = "005_drive_sync_schedule"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "drive_sync_schedule",
        sa.Column("language", sa.String(), nullable=False, server_default="en"),
    )


def downgrade() -> None:
    op.drop_column("drive_sync_schedule", "language")
