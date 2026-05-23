"""feedback: make id_odgovora nullable, add id_sesije for session-level ratings

Revision ID: 004_session_feedback
Revises: 003_add_eksplicitan_zahtjev_anomalija
Create Date: 2026-05-23
"""
import sqlalchemy as sa
from alembic import op

revision = "004_session_feedback"
down_revision = "003_add_eksplicitan_zahtjev_anomalija"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.alter_column("feedback", "id_odgovora", existing_type=sa.BigInteger(), nullable=True)
    op.add_column(
        "feedback",
        sa.Column("id_sesije", sa.BigInteger(), sa.ForeignKey("chat_sesija.id"), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("feedback", "id_sesije")
    # Cannot restore NOT NULL if session-level rows (id_odgovora=NULL) exist
