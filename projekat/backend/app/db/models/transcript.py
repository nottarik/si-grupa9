from sqlalchemy import BigInteger, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
import enum

from app.db.session import Base


class TranskStatusTip(str, enum.Enum):
    sirovi = "Sirovi"
    obradjeno = "Obradjeno"
    odbacen = "Odbacen"


class FormatTip(str, enum.Enum):
    audio = "audio"
    tekst = "tekst"


class KvalitetTip(str, enum.Enum):
    visok = "Visok"
    srednji = "Srednji"
    nizak = "Nizak"


class SegStatusTip(str, enum.Enum):
    validan = "Validan"
    nevalidan = "Nevalidan"
    na_cekanju = "NaCekanju"


class SegTip(str, enum.Enum):
    pitanje = "Pitanje"
    odgovor = "Odgovor"
    kontekst = "Kontekst"


class Transkript(Base):
    __tablename__ = "transkript"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    naziv = Column(String, nullable=False)
    datum_poziva = Column(DateTime(timezone=True), nullable=True)
    trajanje_sec = Column(Integer, nullable=True)
    format = Column(
        Enum("audio", "tekst", name="format_tip", create_type=False),
        nullable=False,
    )
    status = Column(
        Enum("Sirovi", "Obradjeno", "Odbacen", name="transk_status_tip", create_type=False),
        nullable=False,
        default="Sirovi",
    )
    id_korisnika_upload = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=False)
    datum_uploada = Column(DateTime(timezone=True), server_default=func.now())
    jezik = Column(String, nullable=True)
    kvalitet = Column(
        Enum("Visok", "Srednji", "Nizak", name="kvalitet_tip", create_type=False),
        nullable=True,
    )
    # Operational columns for the processing pipeline (add via ALTER TABLE in Supabase)
    file_path = Column(String, nullable=True)
    raw_text = Column(Text, nullable=True)
    processed_text = Column(Text, nullable=True)
    celery_task_id = Column(String, nullable=True)


class Segment(Base):
    __tablename__ = "segment"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tekst = Column(Text, nullable=False)
    tip_segmenta = Column(
        Enum("Pitanje", "Odgovor", "Kontekst", name="seg_tip", create_type=False),
        nullable=False,
    )
    pozicija_u_transkriptu = Column(Integer, nullable=True)
    id_transkripta = Column(BigInteger, ForeignKey("transkript.id"), nullable=False)
    status = Column(
        Enum("Validan", "Nevalidan", "NaCekanju", name="seg_status_tip", create_type=False),
        nullable=False,
        default="NaCekanju",
    )
    id_kategorije = Column(BigInteger, ForeignKey("kategorija.id"), nullable=True)
    pouzdanost_score = Column(Float, nullable=True)
    datum_ekstrakcije = Column(DateTime(timezone=True), server_default=func.now())
