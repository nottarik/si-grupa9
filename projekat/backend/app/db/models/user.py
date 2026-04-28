from sqlalchemy import Boolean, Column, DateTime, Enum, String, func
from sqlalchemy.dialects.postgresql import UUID
import uuid
import enum

from app.db.session import Base


class UlogaTip(str, enum.Enum):
    administrator = "Administrator"
    supervizor = "Supervizor"
    call_centar_agent = "CallCentarAgent"
    krajnji_korisnik = "KrajnjiKorisnik"


class Korisnik(Base):
    __tablename__ = "korisnik"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    ime = Column(String, nullable=False)
    prezime = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False, index=True)
    uloga = Column(
        Enum("Administrator", "Supervizor", "CallCentarAgent", "KrajnjiKorisnik",
             name="uloga_tip", create_type=False),
        nullable=False,
        default="KrajnjiKorisnik",
    )
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    aktivan = Column(Boolean, default=True)
    auth_user_id = Column(UUID(as_uuid=True), nullable=True)
    hashed_password = Column(String, nullable=True)
