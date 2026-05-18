"""add EksplicitanZahtjev to anomalija_tip enum

Revision ID: 003_add_eksplicitan_zahtjev_anomalija
Revises: 002_escalation_tables
Create Date: 2026-05-18
"""
from alembic import op

revision = "003_add_eksplicitan_zahtjev_anomalija"
down_revision = "002_escalation_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TYPE anomalija_tip ADD VALUE IF NOT EXISTS 'EksplicitanZahtjev'")


def downgrade() -> None:
    # PostgreSQL does not support removing enum values; downgrade is a no-op
    pass
