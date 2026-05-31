"""drive_sync_schedule: admin-controlled schedule for the automatic Drive import

Revision ID: 005_drive_sync_schedule
Revises: 004_session_feedback
Create Date: 2026-05-31
"""
import sqlalchemy as sa
from alembic import op

revision = "005_drive_sync_schedule"
down_revision = "004_session_feedback"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "drive_sync_schedule",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("frequency", sa.String(), nullable=False, server_default="daily"),
        sa.Column("hour", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("minute", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("day_of_week", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_run_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    # Seed the singleton config row (disabled by default).
    op.execute("INSERT INTO drive_sync_schedule (id, enabled) VALUES (1, false)")


def downgrade() -> None:
    op.drop_table("drive_sync_schedule")
