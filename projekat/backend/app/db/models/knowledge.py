from sqlalchemy import Boolean, Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.session import Base


class AprovStatusTip(str, enum.Enum):
    odobren = "Odobren"
    odbijen = "Odbijen"
    na_cekanju = "NaCekanju"


class BzStatusTip(str, enum.Enum):
    aktivna = "Aktivna"
    arhivirana = "Arhivirana"
    na_cekanju = "NaCekanju"


class SesijaStatusTip(str, enum.Enum):
    aktivna = "Aktivna"
    zatvorena = "Zatvorena"


class PorukaТip(str, enum.Enum):
    korisnicko_pitanje = "KorisnickoP"
    chatbot_odgovor = "ChatbotOdgovor"


class MetodaTip(str, enum.Enum):
    retrieval = "Retrieval"
    generativno = "Generativno"
    fallback = "Fallback"


class FeedbackTip(str, enum.Enum):
    korisnik_ocjena = "KorisnikOcjena"
    admin_review = "AdminReview"


class AnomalijaTip(str, enum.Enum):
    niska_pouzdanost = "NiskaPouzdanost"
    bez_odgovora = "BezOdgovora"
    kontradiktorni_odgovor = "KontradiktoranOdgovor"
    nevalidan_podatak = "NevalidanPodatak"


class OzbiljnostTip(str, enum.Enum):
    kriticna = "Kriticna"
    visoka = "Visoka"
    niska = "Niska"


class AnomalijаStatus(str, enum.Enum):
    otvorena = "Otvorena"
    rijesena = "Rijesena"
    ignorisana = "Ignorisana"


class Kategorija(Base):
    __tablename__ = "kategorija"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    naziv = Column(String, nullable=False)
    opis = Column(Text, nullable=True)
    nadredjena_kategorija_id = Column(UUID(as_uuid=True), ForeignKey("kategorija.id"), nullable=True)
    aktivan = Column(Boolean, default=True)


class BazaZnanja(Base):
    __tablename__ = "baza_znanja"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    naziv = Column(String, nullable=False)
    verzija = Column(String, nullable=True)
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(
        Enum("Aktivna", "Arhivirana", "NaCekanju", name="bz_status_tip", create_type=False),
        nullable=False,
        default="NaCekanju",
    )
    id_administratora = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=True)
    broj_unosa = Column(Integer, default=0)


class UnosBazeZnanja(Base):
    """Main RAG table — replaces KnowledgeItem."""
    __tablename__ = "unos_baze_znanja"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pitanje = Column(Text, nullable=False)
    odgovor = Column(Text, nullable=False)
    id_baze_znanja = Column(UUID(as_uuid=True), ForeignKey("baza_znanja.id"), nullable=True)
    id_kategorije = Column(UUID(as_uuid=True), ForeignKey("kategorija.id"), nullable=True)
    id_segmenta = Column(UUID(as_uuid=True), ForeignKey("segment.id"), nullable=True)
    status_aprovacije = Column(
        Enum("Odobren", "Odbijen", "NaCekanju", name="aprov_status_tip", create_type=False),
        nullable=False,
        default="NaCekanju",
    )
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    datum_azuriranja = Column(DateTime(timezone=True), onupdate=func.now())
    tezina_pouzdanosti = Column(Float, nullable=True)
    aktivan = Column(Boolean, default=True)
    verzija_broj = Column(Integer, default=1)
    prethodna_verzija_id = Column(UUID(as_uuid=True), ForeignKey("unos_baze_znanja.id"), nullable=True)
    vector_id = Column(String, nullable=True)


class ChatSesija(Base):
    __tablename__ = "chat_sesija"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    datum_pocetka = Column(DateTime(timezone=True), server_default=func.now())
    datum_zavrsetka = Column(DateTime(timezone=True), nullable=True)
    id_korisnika = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=False)
    kanal_pristupa = Column(
        Enum("web", "mobile", "API", name="kanal_tip", create_type=False),
        nullable=False,
        default="web",
    )
    status = Column(
        Enum("Aktivna", "Zatvorena", name="sesija_status_tip", create_type=False),
        nullable=False,
        default="Aktivna",
    )
    broj_poruka = Column(Integer, default=0)


class Poruka(Base):
    __tablename__ = "poruka"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tekst = Column(Text, nullable=False)
    tip = Column(
        Enum("KorisnickoP", "ChatbotOdgovor", name="poruka_tip", create_type=False),
        nullable=False,
    )
    timestamp_msg = Column(DateTime(timezone=True), server_default=func.now())
    id_sesije = Column(UUID(as_uuid=True), ForeignKey("chat_sesija.id"), nullable=False)
    # Set after Odgovor is created; use_alter avoids circular DDL dependency
    id_odgovora = Column(
        UUID(as_uuid=True),
        ForeignKey("odgovor.id", use_alter=True, name="fk_poruka_odgovor"),
        nullable=True,
    )


class Odgovor(Base):
    __tablename__ = "odgovor"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tekst_odgovora = Column(Text, nullable=False)
    id_unosa_baze_znanja = Column(UUID(as_uuid=True), ForeignKey("unos_baze_znanja.id"), nullable=True)
    metoda_generisanja = Column(
        Enum("Retrieval", "Generativno", "Fallback", name="metoda_tip", create_type=False),
        nullable=False,
        default="Fallback",
    )
    skor_pouzdanosti = Column(Float, nullable=True)
    latencija_ms = Column(Integer, nullable=True)
    id_poruke = Column(UUID(as_uuid=True), ForeignKey("poruka.id"), nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ocjena = Column(Float, nullable=True)
    komentar = Column(Text, nullable=True)
    tip = Column(
        Enum("KorisnikOcjena", "AdminReview", name="feedback_tip", create_type=False),
        nullable=False,
        default="KorisnikOcjena",
    )
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    id_odgovora = Column(UUID(as_uuid=True), ForeignKey("odgovor.id"), nullable=False)
    id_korisnika = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=True)


class Anomalija(Base):
    __tablename__ = "anomalija"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    opis = Column(Text, nullable=True)
    tip = Column(
        Enum("NiskaPouzdanost", "BezOdgovora", "KontradiktoranOdgovor", "NevalidanPodatak",
             name="anomalija_tip", create_type=False),
        nullable=True,
    )
    nivo_ozbiljnosti = Column(
        Enum("Kriticna", "Visoka", "Niska", name="ozbiljnost_tip", create_type=False),
        nullable=True,
    )
    status = Column(
        Enum("Otvorena", "Rijesena", "Ignorisana", name="anomalija_status", create_type=False),
        nullable=False,
        default="Otvorena",
    )
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    id_poruke = Column(UUID(as_uuid=True), ForeignKey("poruka.id"), nullable=True)
    id_odgovora = Column(UUID(as_uuid=True), ForeignKey("odgovor.id"), nullable=True)
