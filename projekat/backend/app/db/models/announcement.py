from sqlalchemy import BigInteger, Boolean, Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base

_BigIntPK = BigInteger().with_variant(Integer, "sqlite")


class SistemskaPoruka(Base):
    __tablename__ = "sistemska_poruka"

    id = Column(_BigIntPK, primary_key=True, autoincrement=True)
    naslov = Column(String, nullable=True)
    tekst = Column(Text, nullable=False)
    aktivna = Column(Boolean, nullable=False, default=True, server_default="true")
    datum_kreiranja = Column(DateTime(timezone=True), server_default=func.now())
    datum_azuriranja = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    id_administratora = Column(UUID(as_uuid=True), ForeignKey("korisnik.id"), nullable=False)
