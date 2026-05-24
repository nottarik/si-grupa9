from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class AnnouncementCreate(BaseModel):
    naslov: Optional[str] = None
    tekst: str


class AnnouncementUpdate(BaseModel):
    naslov: Optional[str] = None
    tekst: Optional[str] = None
    aktivna: Optional[bool] = None


class AnnouncementRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    naslov: Optional[str] = None
    tekst: str
    aktivna: bool
    datum_kreiranja: datetime
    datum_azuriranja: Optional[datetime] = None
    id_administratora: str
