from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSON, UUID

from app.db.session import Base

_BigIntPK = BigInteger().with_variant(Integer, "sqlite")


class Eskalacija(Base):
    __tablename__ = "eskalacija"

    id = Column(_BigIntPK, primary_key=True, autoincrement=True)
    sesija_id = Column(BigInteger, ForeignKey("chat_sesija.id"), nullable=False)
    korisnik_id = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=False)
    dodjeljeni_agent_id = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=True)
    prioritet = Column(
        Enum("Nizak", "Normalan", "Visok", "Hitan", name="eskal_prioritet_tip", create_type=False),
        nullable=False,
        default="Normalan",
    )
    status = Column(
        Enum("Cekanje", "UToku", "Rijesena", "Napustena", name="eskal_status_tip", create_type=False),
        nullable=False,
        default="Cekanje",
    )
    trigger_tip = Column(
        Enum(
            "NiskaPouz", "EksplicitanZahtjev", "PonovljeniNeuspjeh", "OsjetljivaTema",
            name="eskal_trigger_tip",
            create_type=False,
        ),
        nullable=True,
    )
    tema = Column(String, nullable=True)
    razgovor = Column(JSON, nullable=True)
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    datum_azuriranja = Column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    datum_rjesavanja = Column(DateTime(timezone=True), nullable=True)
    napomena_rjesavanja = Column(Text, nullable=True)


class StatusAgenta(Base):
    __tablename__ = "status_agenta"

    agent_id = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), primary_key=True)
    status = Column(
        Enum("Online", "Zauzet", "Offline", name="agent_status_tip", create_type=False),
        nullable=False,
        default="Offline",
    )
    trenutna_eskalacija_id = Column(
        BigInteger,
        ForeignKey("eskalacija.id", use_alter=True, name="fk_status_agenta_eskalacija"),
        nullable=True,
    )
    zadnje_aktivno = Column(DateTime(timezone=True), server_default=func.now())
