"""add escalation and agent_status tables

Revision ID: 002_escalation_tables
Revises: 001_add_token_map
Create Date: 2026-05-17

Adds the agent handoff workflow tables:
  - eskalacija: escalation queue entries
  - status_agenta: real-time agent availability
"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = "002_escalation_tables"
down_revision = "001_add_token_map"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE TYPE eskal_prioritet_tip AS ENUM ('Nizak', 'Normalan', 'Visok', 'Hitan')")
    op.execute("CREATE TYPE eskal_status_tip AS ENUM ('Cekanje', 'UToku', 'Rijesena', 'Napustena')")
    op.execute(
        "CREATE TYPE eskal_trigger_tip AS ENUM "
        "('NiskaPouz', 'EksplicitanZahtjev', 'PonovljeniNeuspjeh', 'OsjetljivaTema')"
    )
    op.execute("CREATE TYPE agent_status_tip AS ENUM ('Online', 'Zauzet', 'Offline')")

    op.create_table(
        "eskalacija",
        sa.Column("id", sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column("sesija_id", sa.BigInteger(), nullable=False),
        sa.Column("korisnik_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("dodjeljeni_agent_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "prioritet",
            postgresql.ENUM(
                "Nizak", "Normalan", "Visok", "Hitan",
                name="eskal_prioritet_tip", create_type=False,
            ),
            nullable=False,
            server_default="Normalan",
        ),
        sa.Column(
            "status",
            postgresql.ENUM(
                "Cekanje", "UToku", "Rijesena", "Napustena",
                name="eskal_status_tip", create_type=False,
            ),
            nullable=False,
            server_default="Cekanje",
        ),
        sa.Column(
            "trigger_tip",
            postgresql.ENUM(
                "NiskaPouz", "EksplicitanZahtjev", "PonovljeniNeuspjeh", "OsjetljivaTema",
                name="eskal_trigger_tip", create_type=False,
            ),
            nullable=True,
        ),
        sa.Column("tema", sa.String(), nullable=True),
        sa.Column("razgovor", postgresql.JSON(astext_type=sa.Text()), nullable=True),
        sa.Column(
            "datum_kreiranja",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column(
            "datum_azuriranja",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("datum_rjesavanja", sa.DateTime(timezone=True), nullable=True),
        sa.Column("napomena_rjesavanja", sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(["sesija_id"], ["chat_sesija.id"]),
        sa.ForeignKeyConstraint(["korisnik_id"], ["korisnik.id"]),
        sa.ForeignKeyConstraint(["dodjeljeni_agent_id"], ["korisnik.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "status_agenta",
        sa.Column("agent_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "status",
            postgresql.ENUM(
                "Online", "Zauzet", "Offline",
                name="agent_status_tip", create_type=False,
            ),
            nullable=False,
            server_default="Offline",
        ),
        sa.Column("trenutna_eskalacija_id", sa.BigInteger(), nullable=True),
        sa.Column(
            "zadnje_aktivno",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(["agent_id"], ["korisnik.id"]),
        sa.ForeignKeyConstraint(
            ["trenutna_eskalacija_id"],
            ["eskalacija.id"],
            use_alter=True,
            name="fk_status_agenta_eskalacija",
        ),
        sa.PrimaryKeyConstraint("agent_id"),
    )


def downgrade() -> None:
    op.drop_table("status_agenta")
    op.drop_table("eskalacija")
    op.execute("DROP TYPE IF EXISTS agent_status_tip")
    op.execute("DROP TYPE IF EXISTS eskal_trigger_tip")
    op.execute("DROP TYPE IF EXISTS eskal_status_tip")
    op.execute("DROP TYPE IF EXISTS eskal_prioritet_tip")
