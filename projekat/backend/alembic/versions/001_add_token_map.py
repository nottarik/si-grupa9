"""add token_map table

Revision ID: 001_add_token_map
Revises:
Create Date: 2026-05-10

Stores encrypted PII placeholder→original mappings per transcript.
Raw values are never stored in plaintext; encryption uses Fernet (TOKEN_MAP_KEY env var).
"""
from alembic import op
import sqlalchemy as sa

revision = "001_add_token_map"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "token_map",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("transkript_id", sa.BigInteger(), nullable=False),
        sa.Column("encrypted_blob", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["transkript_id"], ["transkript.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("transkript_id", name="uq_token_map_transkript"),
    )


def downgrade() -> None:
    op.drop_table("token_map")
